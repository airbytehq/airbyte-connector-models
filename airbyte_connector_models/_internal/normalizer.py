"""Field name normalization utilities."""

import keyword
import re


def normalize_field_name(field_name: str) -> str:
    """Normalize a field name to be a valid Python identifier.

    This performs minimal normalization:
    - Replaces hyphens with underscores
    - Replaces spaces with underscores
    - Replaces other illegal characters with underscores
    - Preserves original casing (MyKey stays MyKey, not my_key)
    - Handles Python keywords by appending underscore
    - Handles leading digits by prepending underscore

    Examples:
        >>> normalize_field_name("User-ID")
        'User_ID'
        >>> normalize_field_name("First Name")
        'First_Name'
        >>> normalize_field_name("my-key")
        'my_key'
        >>> normalize_field_name("MyKey")
        'MyKey'
        >>> normalize_field_name("class")
        'class_'
        >>> normalize_field_name("123abc")
        '_123abc'

    Args:
        field_name: The original field name from the schema

    Returns:
        A valid Python identifier with minimal normalization
    """
    if not field_name:
        return "_"

    normalized = field_name.replace("-", "_").replace(" ", "_")

    normalized = re.sub(r"[^\w]", "_", normalized)

    if normalized[0].isdigit():
        normalized = f"_{normalized}"

    if keyword.iskeyword(normalized):
        normalized = f"{normalized}_"

    normalized = re.sub(r"_+", "_", normalized)

    if not keyword.iskeyword(field_name):
        normalized = normalized.rstrip("_")

    return normalized or "_"


def needs_normalization(field_name: str) -> bool:
    """Check if a field name needs normalization.

    Args:
        field_name: The field name to check

    Returns:
        True if the field name needs normalization, False otherwise
    """
    return normalize_field_name(field_name) != field_name
