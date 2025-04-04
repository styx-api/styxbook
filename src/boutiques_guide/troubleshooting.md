# Troubleshooting Boutiques Descriptors

This guide covers common issues when creating or modifying Boutiques descriptors and their solutions.

> **Cross-reference**: For the core structure of descriptors, see [Basic Structure](./basic_structure.md).  
> **Cross-reference**: For issues specific to subcommands, see [Subcommands](./subcommands.md).  
> **Cross-reference**: For file handling problems, see [File Handling](./file_handling.md).

## Schema Validation Errors

### Missing Required Fields

**Problem**: `ERROR: 'name' is a required property`

**Solution**: Ensure all required top-level fields are present:

```json
{
  "name": "tool_name",
  "description": "Tool description",
  "command-line": "command [ARGS]",
  "inputs": [...],
  "schema-version": "0.5",
  "tool-version": "1.0.0"
}
```

### Invalid Value Types

**Problem**: `ERROR: 'string' is not of type 'number'`

**Solution**: Check that values match their declared types. For numeric parameters:

```json
{
  "id": "threshold",
  "type": "Number",
  "default-value": 0.5  // Not "0.5" as a string
}
```

### Invalid IDs

**Problem**: `ERROR: 'input-file' does not match pattern '^[0-9,_,a-z,A-Z]*$'`

**Solution**: IDs must contain only alphanumeric characters and underscores:

```json
{
  "id": "input_file",  // Not "input-file"
  "name": "Input File"
}
```

## Command-Line Formation Issues

### Value-Key Placeholders Not Working

**Problem**: Value-key placeholders aren't replaced in the command line.

**Solution**:

1. Ensure the value-key in the parameter matches exactly what's in the command-line:

   ```json
   "command-line": "tool [INPUT_FILE]",
   "inputs": [
     {
       "id": "input",
       "value-key": "[INPUT_FILE]"  // Must match exactly, including case
     }
   ]
   ```

2. Verify that value-keys follow the formatting rules (uppercase, underscores, enclosed in square brackets).

### Command-Line Flags Not Appearing

**Problem**: Command-line flags aren't included in the generated command.

**Solution**: Make sure you're using the correct fields:

```json
{
  "id": "verbose",
  "command-line-flag": "-v",  // The flag itself
  "value-key": "[VERBOSE]"    // Where it appears in the command-line
}
```

### List Parameters Not Formatted Correctly

**Problem**: List values aren't formatted as expected in the command.

**Solution**: Use the `list-separator` field to control how values are joined:

```json
{
  "id": "coordinates",
  "type": "Number",
  "list": true,
  "list-separator": ",",  // Will join values with commas
  "value-key": "[COORDS]"
}
```

## Subcommand Issues

### Subcommand Parameters Not Available

**Problem**: Parameters inside subcommands aren't accessible in the generated bindings.

**Solution**: Check your subcommand structure:

```json
{
  "id": "algorithm",
  "type": [
    {
      "id": "method1",
      "inputs": [
        {
          "id": "param1",  // Make sure IDs are unique
          "type": "String"
        }
      ]
    }
  ]
}
```

### Mutually Exclusive Options Not Working

**Problem**: The descriptor doesn't enforce mutually exclusive options.

**Solution**: Instead of using `groups` with `mutually-exclusive`, use subcommands:

```json
{
  "id": "mode",
  "type": [
    { "id": "mode1", "inputs": [...] },
    { "id": "mode2", "inputs": [...] }
  ]
}
```

This creates a proper union type in the generated bindings.

## File Handling Issues

### Input Files Not Found

**Problem**: Input files are reported as not found even though they exist.

**Solution**:

1. Make sure you're using `"type": "File"` for input files
2. Check if paths are relative to the current working directory
3. For containerized runs, verify file paths are accessible in the container

### Output Files Not Created Where Expected

**Problem**: Output files appear in unexpected locations.

**Solution**: Check your `path-template` in output-files:

```json
"output-files": [
  {
    "id": "output",
    "path-template": "[OUTPUT_DIR]/[PREFIX].nii.gz"
  }
]
```

Ensure all value-keys (`[OUTPUT_DIR]`, `[PREFIX]`) are defined in your inputs.

### File Extensions Not Handled Correctly

**Problem**: Output files have double extensions like `file.nii.gz.nii.gz`.

**Solution**: Use `path-template-stripped-extensions`:

```json
"output-files": [
  {
    "id": "output",
    "path-template": "[INPUT]_processed.nii.gz",
    "path-template-stripped-extensions": [".nii.gz", ".nii"]
  }
]
```

## Container Issues

### Container Not Found

**Problem**: The container image cannot be pulled or found.

**Solution**:

1. Verify the container exists in the specified registry
2. Ensure the image name and tag are correct:

   ```json
   "container-image": {
     "type": "docker",
     "image": "organization/image:tag"
   }
   ```

### Missing Dependencies in Container

**Problem**: The tool reports missing dependencies inside the container.

**Solution**: Use a container that includes all required dependencies. You may need to build a custom container with a Dockerfile:

```dockerfile
FROM base/image:tag
RUN apt-get update && apt-get install -y additional-dependency
```

## Common Pitfalls

### Value-Keys vs. Command-Line-Flags

**Problem**: Confusion between value-keys and command-line-flags.

**Solution**:

- `value-key` is a placeholder in the command-line template
- `command-line-flag` is the actual flag used in the command (e.g., `-v`, `--verbose`)
- Both are often needed:

  ```json
  {
    "id": "threshold",
    "command-line-flag": "--threshold",
    "value-key": "[THRESHOLD]"
  }
  ```

### Input vs. Output File Types

**Problem**: Confusion about how to define input and output files.

**Solution**:

- Input files use `"type": "File"` in the inputs section
- Output files are defined in the `output-files` section with a `path-template`
- For parameters that specify output paths, use `"type": "String"` (not `"File"`)

### Inconsistent Naming

**Problem**: Similar parameters have inconsistent naming across descriptors.

**Solution**: Follow consistent naming conventions:

```json
// Good:
"id": "input_file"
"id": "output_dir"
"id": "threshold"

// Avoid mixing styles:
"id": "inputFile"
"id": "output-dir"
"id": "THRESHOLD"
```

## Debugging Techniques

### Validating Descriptors

Always validate your descriptors before using them:

```bash
# Using NiWrap validation
python -m pytest tests/test_descriptors.py::test_descriptor_validity

# Using VSCode with JSON schema
# Configure .vscode/settings.json as described in the docs
```

### Printing Command Line

When testing, print the full command line to see if it's formed correctly:

```python
# Python
from niwrap.tool import function
cmd = function.get_command(param1="value", param2=123)
print(cmd)
```

### Using Verbose Mode

Many tools have verbose or debug modes that can help identify issues:

```json
{
  "id": "verbose",
  "name": "Verbose",
  "type": "Flag",
  "command-line-flag": "-v",
  "value-key": "[VERBOSE]"
}
```

## Getting Help

If you're still having issues:

1. Check existing descriptors in the NiWrap repository for examples
2. Examine the [Boutiques documentation](https://boutiques.github.io/doc/)
3. Open an issue in the [NiWrap issue tracker](https://github.com/styx-api/niwrap/issues)
