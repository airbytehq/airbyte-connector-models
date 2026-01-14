"""Functions for generating Pydantic models from metadata schemas."""

import json
import logging
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

from .utils import get_repo_root, to_snake_case_module

logger = logging.getLogger(__name__)


def _parse_classes(
    lines: list[str],
    class_pattern: re.Pattern[str],
) -> dict[str, tuple[int, int, str, str]]:
    """Parse class definitions from file lines.

    Returns a dict mapping class name to (start_line, end_line, class_text, base_classes).
    """
    classes: dict[str, tuple[int, int, str, str]] = {}
    i = 0
    while i < len(lines):
        match = class_pattern.match(lines[i])
        if match:
            class_name, base_classes, start_line = match.group(1), match.group(2), i
            j = i + 1
            while j < len(lines) and not class_pattern.match(lines[j]):
                j += 1
            classes[class_name] = (start_line, j, "\n".join(lines[start_line:j]), base_classes)
            i = j
        else:
            i += 1
    return classes


def _build_dependency_graph(
    classes: dict[str, tuple[int, int, str, str]],
) -> dict[str, set[str]]:
    """Build a dependency graph from class definitions."""
    dependencies: dict[str, set[str]] = {name: set() for name in classes}
    for class_name, (_, _, _, base_classes) in classes.items():
        for other_class in classes:
            if other_class != class_name and other_class in base_classes:
                dependencies[class_name].add(other_class)
    return dependencies


def _needs_reordering(
    classes: dict[str, tuple[int, int, str, str]],
    dependencies: dict[str, set[str]],
) -> bool:
    """Check if any class references a dependency defined after it."""
    class_order = list(classes.keys())
    for i, class_name in enumerate(class_order):
        for dep in dependencies[class_name]:
            if dep in class_order and class_order.index(dep) > i:
                return True
    return False


def _topological_sort(
    classes: dict[str, tuple[int, int, str, str]],
    dependencies: dict[str, set[str]],
) -> list[str]:
    """Perform topological sort to get correct class order."""
    sorted_classes: list[str] = []
    visited: set[str] = set()
    temp_visited: set[str] = set()

    def visit(name: str) -> None:
        if name in temp_visited or name in visited:
            return
        temp_visited.add(name)
        for dep in dependencies.get(name, set()):
            if dep in classes:
                visit(dep)
        temp_visited.remove(name)
        visited.add(name)
        sorted_classes.append(name)

    for class_name in classes:
        visit(class_name)
    return sorted_classes


def _fix_forward_references(file_path: Path) -> None:
    """Fix forward reference issues in generated Pydantic models.

    datamodel-codegen may generate classes in an order where a class references
    another class (in its base class) before that class is defined. This function
    reorders classes to ensure dependencies are defined before their dependents.

    Args:
        file_path: Path to the generated Python file to fix
    """
    content = file_path.read_text()
    lines = content.split("\n")
    class_pattern = re.compile(r"^class (\w+)\(([^)]+)\):", re.MULTILINE)

    classes = _parse_classes(lines, class_pattern)
    if not classes:
        return

    dependencies = _build_dependency_graph(classes)
    if not _needs_reordering(classes, dependencies):
        return

    logger.info(f"Fixing forward references in {file_path}")
    sorted_classes = _topological_sort(classes, dependencies)

    # Build reverse dependency map: which classes depend on each class
    dependents: dict[str, set[str]] = {name: set() for name in classes}
    for class_name, deps in dependencies.items():
        for dep in deps:
            dependents[dep].add(class_name)

    # Find classes that were moved earlier due to dependencies
    original_order = list(classes.keys())
    moved_classes: dict[str, set[str]] = {}
    for i, class_name in enumerate(sorted_classes):
        original_idx = original_order.index(class_name)
        if original_idx > i and dependents[class_name]:
            moved_classes[class_name] = dependents[class_name]

    first_class_start = min(info[0] for info in classes.values())
    header = "\n".join(lines[:first_class_start])

    # Build new content with targeted comments on moved classes
    new_content = header.rstrip("\n") + "\n\n\n"
    for i, class_name in enumerate(sorted_classes):
        class_text = classes[class_name][2].strip("\n")
        if i > 0:
            new_content += "\n\n\n"  # Two blank lines between classes (PEP 8)
        if class_name in moved_classes:
            deps_list = ", ".join(sorted(moved_classes[class_name]))
            comment = f"# Defined above {deps_list} which depends on it.\n"
            new_content += comment
        new_content += class_text
    new_content += "\n"

    file_path.write_text(new_content)
    logger.info(f"Reordered {len(sorted_classes)} classes in {file_path}")


def generate_metadata_models() -> None:
    """Generate Pydantic models from metadata schemas.

    Reads all YAML schemas from src/metadata/v0/ and generates
    corresponding Pydantic models in models/metadata/v0/.
    """
    logger.info("Generating metadata models")

    repo_root = get_repo_root()
    schema_dir = repo_root / "src" / "metadata" / "v0"
    output_dir = repo_root / "models" / "metadata" / "v0"
    output_dir.mkdir(parents=True, exist_ok=True)

    header_path = repo_root / ".header.txt"

    schema_files = sorted(schema_dir.glob("*.yaml"))

    if not schema_files:
        logger.warning(f"No schema files found in {schema_dir}")
        return

    logger.info(f"Found {len(schema_files)} metadata schema files")

    for schema_file in schema_files:
        model_name = schema_file.stem  # e.g., "ConnectorMetadataDefinitionV0"
        module_name = to_snake_case_module(schema_file.stem)
        output_file = output_dir / f"{module_name}.py"

        logger.info(f"Generating model for {schema_file.name} -> {module_name}.py")

        try:
            with schema_file.open() as f:
                schema_data = yaml.safe_load(f)

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
                json.dump(schema_data, temp_file)
                temp_schema_path = temp_file.name

            try:
                subprocess.run(
                    [
                        "datamodel-codegen",
                        "--input",
                        temp_schema_path,
                        "--output",
                        str(output_file),
                        "--input-file-type",
                        "jsonschema",
                        "--output-model-type",
                        "pydantic_v2.BaseModel",
                        "--class-name",
                        model_name,
                        "--use-standard-collections",
                        "--use-union-operator",
                        "--field-constraints",
                        "--use-annotated",
                        "--keyword-only",
                        "--disable-timestamp",
                        "--use-exact-imports",
                        "--use-double-quotes",
                        "--keep-model-order",
                        "--use-schema-description",
                        "--parent-scoped-naming",
                        "--use-title-as-name",
                        "--target-python-version",
                        "3.10",
                        "--custom-file-header-path",
                        str(header_path),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                logger.info(f"Generated {output_file}")

            finally:
                Path(temp_schema_path).unlink(missing_ok=True)

        except Exception:
            logger.exception(f"Failed to generate model for {schema_file.name}")

    init_file = output_dir / "__init__.py"
    init_content = (
        "# Copyright (c) 2025 Airbyte, Inc., all rights reserved.\n\n"
        '"""Metadata models for Airbyte connectors."""\n'
    )
    init_file.write_text(init_content)

    logger.info(f"Generated {len(schema_files)} metadata models in {output_dir}")


def generate_consolidated_metadata_model() -> None:
    """Generate a single consolidated Pydantic model from bundled JSON schema.

    Reads the bundled ConnectorMetadataDefinitionV0.json and generates a single
    Python file containing all metadata model classes.
    """
    logger.info("Generating consolidated metadata model from bundled JSON")

    repo_root = get_repo_root()
    bundled_json = repo_root / "models" / "metadata" / "v0" / "ConnectorMetadataDefinitionV0.json"
    output_file = repo_root / "models" / "metadata" / "v0" / "connector_metadata_definition_v0.py"

    _generate_consolidated_model(bundled_json, output_file, "ConnectorMetadataDefinitionV0")


def generate_consolidated_registry_model() -> None:
    """Generate a single consolidated Pydantic model for registry from bundled JSON schema.

    Reads the bundled ConnectorRegistryV0.json and generates a single
    Python file containing all registry model classes.
    """
    logger.info("Generating consolidated registry model from bundled JSON")

    repo_root = get_repo_root()
    bundled_json = repo_root / "models" / "metadata" / "v0" / "ConnectorRegistryV0.json"
    output_file = repo_root / "models" / "metadata" / "v0" / "connector_registry_v0.py"

    _generate_consolidated_model(bundled_json, output_file, "ConnectorRegistryV0")


def _generate_consolidated_model(bundled_json: Path, output_file: Path, schema_name: str) -> None:
    """Internal helper to generate a consolidated model from bundled JSON.

    Args:
        bundled_json: Path to the bundled JSON schema
        output_file: Path to the output Python file
        schema_name: Name of the schema for logging
    """
    if not bundled_json.exists():
        logger.error(f"Bundled JSON not found: {bundled_json}")
        logger.error("Run 'npm run bundle-schemas' first to create the bundled JSON")
        return

    repo_root = get_repo_root()
    header_path = repo_root / ".header.txt"

    try:
        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                str(bundled_json),
                "--output",
                str(output_file),
                "--input-file-type",
                "jsonschema",
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--use-standard-collections",
                "--use-union-operator",
                "--field-constraints",
                "--use-annotated",
                "--keyword-only",
                "--disable-timestamp",
                "--use-exact-imports",
                "--use-double-quotes",
                "--keep-model-order",
                "--use-schema-description",
                "--parent-scoped-naming",
                "--use-title-as-name",
                "--target-python-version",
                "3.10",
                "--custom-file-header-path",
                str(header_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        logger.info(f"Generated consolidated model: {output_file}")

        # Fix forward reference issues in the generated code
        _fix_forward_references(output_file)

    except subprocess.CalledProcessError as e:
        logger.exception(f"Failed to generate consolidated model for {schema_name}")
        logger.info(f"stdout: {e.stdout}")
        logger.info(f"stderr: {e.stderr}")
