#!/usr/bin/env node

/**
 * Bundle JSON schemas using @apidevtools/json-schema-ref-parser
 * This script resolves all $ref references in the schema files and creates a single bundled schema.
 */

const $RefParser = require('@apidevtools/json-schema-ref-parser');
const fs = require('fs');
const path = require('path');

const YAML_DIR = 'src/metadata/v0';
const OUTPUT_DIR = 'models/metadata/v0';
const ENTRY_SCHEMA = path.join(YAML_DIR, 'ConnectorMetadataDefinitionV0.yaml');
const BUNDLE_OUTPUT = path.join(OUTPUT_DIR, 'ConnectorMetadataDefinitionV0.json');

const NEW_SCHEMA_ID = 'https://raw.githubusercontent.com/airbytehq/airbyte-connector-models/main/models/metadata/v0/ConnectorMetadataDefinitionV0.json';

async function bundleSchemas() {
  try {
    console.log('📦 Bundling JSON schemas...');
    console.log(`   Entry schema: ${ENTRY_SCHEMA}`);
    console.log(`   Output: ${BUNDLE_OUTPUT}`);

    if (!fs.existsSync(YAML_DIR)) {
      console.error(`❌ Error: The yaml directory does not exist: ${YAML_DIR}`);
      process.exit(1);
    }

    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const schema = await $RefParser.bundle(ENTRY_SCHEMA, {
      dereference: {
        circular: 'ignore' // Handle circular references gracefully
      }
    });

    schema.$id = NEW_SCHEMA_ID;

    fs.writeFileSync(BUNDLE_OUTPUT, JSON.stringify(schema, null, 2));

    console.log('✅ Successfully bundled schema to', BUNDLE_OUTPUT);
    console.log(`   Updated $id to: ${NEW_SCHEMA_ID}`);
    console.log('   This bundled schema can be used for IDE validation and other tools.');
  } catch (error) {
    console.error('❌ Error bundling schemas:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

bundleSchemas();
