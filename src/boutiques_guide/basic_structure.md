# Basic Structure of Boutiques Descriptors

A Boutiques descriptor is a JSON file with a specific structure. This page explains the core components and how they fit together.

## Top-level Fields

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Short name of the tool | `"bet"` |
| `description` | Detailed description of what the tool does | `"Automated brain extraction tool for FSL"` |
| `tool-version` | Version of the tool being described | `"6.0.4"` |
| `schema-version` | Version of the Boutiques schema | `"0.5"` |
| `command-line` | Template for the command with placeholders | `"bet [INFILE] [MASKFILE] [OPTIONS]"` |
| `inputs` | Array of input parameters | `[{ "id": "infile", ... }]` |

### Common Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `author` | Author of the tool | `"FMRIB Analysis Group, University of Oxford"` |
| `url` | URL for the tool's documentation | `"https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"` |
| `container-image` | Container configuration | `{ "type": "docker", "image": "..." }` |
| `output-files` | Array of output files | `[{ "id": "outfile", ... }]` |
| `stdout-output` | Capture stdout as an output | `{ "id": "stdout_data", ... }` |
| `stderr-output` | Capture stderr as an output | `{ "id": "error_log", ... }` |

### Unused Boutiques Fields

The following standard Boutiques fields are not currently used in the Styx ecosystem:

- `environment-variables`: Environment variables to set
- `tests`: Sample invocations for testing
- `online-platform-urls`: URLs to platforms where tool is available
- `invocation-schema`: Custom schema for tool-specific invocation validation
- `suggested-resources`: Computational resources needed
- `tags`: Categorization tags
- `error-codes`: Tool-specific error codes
- `custom`: Custom tool-specific metadata

## Input Parameters

Input parameters define the arguments that can be passed to a tool. They're specified in the `inputs` array.

### Common Parameter Fields

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `id` | Unique identifier (alphanumeric + underscores) | Yes | `"input_file"` |
| `name` | Human-readable name | Yes | `"Input file"` |
| `description` | Detailed description | No | `"The input image in NIFTI format"` |
| `value-key` | Placeholder in command-line template | Yes | `"[INPUT_FILE]"` |
| `optional` | Whether parameter is required | Yes | `true` |
| `command-line-flag` | Command-line option prefix | No | `"-i"` |
| `default-value` | Default value if not specified | No | `"standard.nii.gz"` |
| `value-choices` | Array of allowed values | No | `["small", "medium", "large"]` |

### Parameter Types

#### Basic Types

| Type | Description | Attributes | Example |
|------|-------------|------------|---------|
| `File` | File path | N/A | `{ "type": "File", "id": "input_image" }` |
| `String` | Text string | N/A | `{ "type": "String", "id": "output_prefix" }` |
| `Number` | Numeric value | `integer`: boolean, `minimum`, `maximum` | `{ "type": "Number", "integer": false, "minimum": 0, "maximum": 1 }` |
| `Flag` | Boolean flag (no value) | N/A | `{ "type": "Flag", "id": "verbose" }` |

#### List Variants

Any basic type can be made into a list by adding `"list": true`:

```json
{
  "id": "coordinates", 
  "type": "Number",
  "list": true,
  "min-list-entries": 3,
  "max-list-entries": 3
}
```

Optional list-related fields:

- `min-list-entries`: Minimum number of elements required
- `max-list-entries`: Maximum number of elements allowed
- `list-separator`: Character(s) used to join list values (default is space)

Example with a custom separator:

```json
{
  "id": "tags",
  "type": "String",
  "list": true,
  "list-separator": ","
}
```

This would result in a command-line argument like: `--tags tag1,tag2,tag3`

## Command-Line Formation

The command-line is formed by replacing value-keys in the command-line template with actual parameter values.

### Value Keys

Value keys connect parameters to positions in the command line. In the Styx ecosystem, they should:

- Be enclosed in square brackets: `[LIKE_THIS]`
- Use only uppercase letters, numbers, and underscores
- Match exactly in the `command-line` template

Example:

```json
"command-line": "bet [INFILE] [OUTFILE] [OPTIONS]",
"inputs": [
  {
    "id": "infile",
    "value-key": "[INFILE]",
    "type": "File"
  }
]
```

This replaces `[INFILE]` in the command-line with the actual file path.

### Command-Line Flags

Command-line flags are specified with the `command-line-flag` field:

```json
{
  "id": "verbose",
  "command-line-flag": "-v",
  "value-key": "[VERBOSE]",
  "type": "Flag"
}
```

For flags with values, you can control the separator between the flag and value:

```json
{
  "id": "threshold",
  "command-line-flag": "--threshold",
  "command-line-flag-separator": "=",
  "value-key": "[THRESHOLD]",
  "type": "Number"
}
```

This would result in `--threshold=0.5` rather than `--threshold 0.5`.

## Output Files

Output files are defined in the `output-files` array. Unlike inputs, these aren't actually files passed to the command line but rather specifications of what files will be produced:

```json
"output-files": [
  {
    "id": "brain_mask",
    "name": "Brain Mask Image",
    "description": "Binary mask of the brain",
    "path-template": "[OUTDIR]/[PREFIX]_mask.nii.gz",
    "optional": false
  }
]
```

The `path-template` uses the same value keys from inputs to construct the output path.

Common output file fields:

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `id` | Unique identifier | Yes | `"brain_mask"` |
| `name` | Human-readable name | Yes | `"Brain Mask Image"` |
| `description` | Detailed description | No | `"Binary mask of the brain"` |
| `path-template` | Template for output file path | Yes | `"[OUTPUT_DIR]/[PREFIX]_mask.nii.gz"` |
| `optional` | Whether file might not be produced | No | `true` |

## Container Configuration

Container configurations help ensure reproducibility:

```json
"container-image": {
  "type": "docker",
  "image": "brainlife/fsl:6.0.4-patched2"
}
```

In the Styx ecosystem, primarily the `type` and `image` fields are used, with Docker as
the only container type.

## Cross-References

Now that you understand the basic structure, learn more about:

- [Subcommands](./subcommands.md) - For tools with complex structure and hierarchical parameters
- [File Handling](./file_handling.md) - For detailed file input/output, path templates, and extension handling
- [Advanced Features](./advanced_features.md) - For command output capture, package configuration, and more
- [Troubleshooting](./troubleshooting.md) - For common issues and their solutions
- [Examples](./examples.md) - For complete descriptor examples showing these concepts in action
