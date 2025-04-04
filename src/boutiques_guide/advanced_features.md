# Advanced Features in Boutiques

This page covers advanced features and extensions of the Boutiques format in the Styx ecosystem.

> **Cross-reference**: For the core structure and basic fields, see [Basic Structure](./basic_structure.md).  
> **Cross-reference**: For subcommand hierarchies, see [Subcommands](./subcommands.md).  
> **Cross-reference**: For file input/output handling, see [File Handling](./file_handling.md).

## Package Configuration Files

NiWrap uses separate package configuration files to organize tools by suite:

```json
{
  "name": "FSL",
  "author": "FMRIB Analysis Group, University of Oxford",
  "url": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki",
  "approach": "Manual",
  "status": "Experimental",
  "container": "brainlife/fsl:6.0.4-patched2",
  "version": "6.0.5",
  "description": "FSL is a comprehensive library of analysis tools for FMRI, MRI and diffusion brain imaging data.",
  "id": "fsl",
  "api": {
    "endpoints": [
      {
        "target": "AnatomicalAverage",
        "status": "done",
        "descriptor": "descriptors/fsl/AnatomicalAverage.json"
      },
      {
        "target": "Text2Vest",
        "status": "missing"
      },
      {
        "target": "Runtcl",
        "status": "ignore"
      }
    ]
  }
}
```

### Package Configuration Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Human-readable package name | `"FSL"` |
| `author` | Author or organization | `"FMRIB Analysis Group, University of Oxford"` |
| `url` | Documentation URL | `"https://fsl.fmrib.ox.ac.uk/fslwiki"` |
| `approach` | How interfaces were created | `"Manual"` or `"Extracted"` |
| `status` | Overall package status | `"Experimental"` or `"Stable"` |
| `container` | Default container image | `"brainlife/fsl:6.0.4-patched2"` |
| `version` | Package version | `"6.0.5"` |
| `description` | Package description | `"FSL is a comprehensive library..."` |
| `id` | Unique package identifier | `"fsl"` |
| `api.endpoints` | Tool definitions | Array of endpoint objects |

### Endpoint Status Values

The `status` field in each endpoint tracks implementation:

- `"done"`: Descriptor is complete and ready to use
- `"missing"`: Tool is identified but descriptor not yet created
- `"ignore"`: Tool should be deliberately excluded from the API

While these files are primarily used for tracking coverage and generating documentation, some metadata (name, author, description) is used in the generated language bindings.

## Command Output Capture

For tools that output important data to stdout or stderr, the Styx ecosystem extends Boutiques with special fields:

```json
"stdout-output": {
  "id": "calculation_results",
  "name": "Calculation Results", 
  "description": "Output of the numerical calculation"
},
"stderr-output": {
  "id": "warning_messages",
  "name": "Warning Messages",
  "description": "Warnings and errors during processing"
}
```

These fields make the command output available as strings in the generated bindings, useful for tools that:

- Output data tables to the terminal
- Provide processing statistics on stderr
- Generate simple text outputs without writing files

## Groups

While the standard Boutiques format uses `groups` to organize related parameters, the Styx ecosystem generally favors subcommands for this purpose. However, the `groups` field is still part of the schema:

```json
"groups": [
  {
    "id": "required_params",
    "name": "Required Parameters",
    "description": "Parameters that must be specified",
    "members": ["input_file", "output_prefix"]
  },
  {
    "id": "exclusive_options",
    "name": "Processing Options",
    "description": "Choose only one processing option",
    "members": ["fast_mode", "accurate_mode", "balanced_mode"],
    "mutually-exclusive": true
  },
  {
    "id": "debug_options",
    "name": "Debug Options",
    "description": "Debugging parameters",
    "members": ["verbose", "debug", "trace"],
    "one-is-required": false
  }
]
```

### Group Properties

| Property | Description | Example |
|----------|-------------|---------|
| `id` | Unique identifier | `"required_params"` |
| `name` | Human-readable name | `"Required Parameters"` |
| `description` | Detailed description | `"Parameters that must be specified"` |
| `members` | Array of parameter IDs | `["input_file", "output_prefix"]` |
| `mutually-exclusive` | Only one member can be used | `true` |
| `all-or-none` | Either all or no members must be used | `true` |
| `one-is-required` | At least one member must be specified | `true` |

## Command-Line Flag Separators

By default, command-line flags and their values are separated by a space. You can change this with the `command-line-flag-separator` field:

```json
{
  "id": "threshold",
  "name": "Threshold",
  "command-line-flag": "--threshold",
  "command-line-flag-separator": "=",
  "value-key": "[THRESHOLD]",
  "type": "Number"
}
```

This would produce `--threshold=0.5` instead of `--threshold 0.5`.

## List Separators

For list parameters, you can control how the values are joined with the `list-separator` field:

```json
{
  "id": "coordinates",
  "name": "Coordinates",
  "type": "Number",
  "list": true,
  "list-separator": ",",
  "value-key": "[COORDS]"
}
```

With values `[1, 2, 3]`, this would produce `1,2,3` instead of the default `1 2 3`.

## Container Configurations

The `container-image` field defines container information:

```json
"container-image": {
  "type": "docker",
  "image": "brainlife/fsl:6.0.4-patched2",
  "index": "docker.io"
}
```

In the Styx ecosystem, primarily the `type` and `image` fields are used, with Docker as the main container type.

## Value Constraints

Several fields help constrain parameter values:

### For Numeric Values

```json
{
  "id": "threshold",
  "type": "Number",
  "integer": false,
  "minimum": 0,
  "maximum": 1,
  "exclusive-minimum": false,
  "exclusive-maximum": false
}
```

### For String Values with Fixed Choices

```json
{
  "id": "mode",
  "type": "String",
  "value-choices": ["fast", "balanced", "accurate"]
}
```

### For Files with Pattern Matching

```json
{
  "id": "image",
  "type": "File",
  "value-choices": ["*.nii", "*.nii.gz"]
}
```

## Validation and Testing

When creating or modifying descriptors, use these validation methods:

1. JSON Schema validation:

   ```bash
   # In NiWrap repository
   python -m pytest tests/test_descriptors.py::test_descriptor_validity
   ```

2. Visual Studio Code validation:
   Add this to `.vscode/settings.json`:

   ```json
   {
     "json.schemas": [
       {
         "fileMatch": ["descriptors/**/*.json"],
         "url": "./schemas/descriptor.schema.json"
       }
     ]
   }
   ```

3. Build testing:

   ```bash
   # Test if Styx can process your descriptor
   python build.py
   ```

## Future Extensions

The Styx ecosystem continues to evolve, with several planned extensions:

- Additional parameter types for more complex data structures
- Enhanced dependency modeling between parameters
- Improved container configuration options
- Custom frontend formats beyond Boutiques

NiWrap extensions are being proposed for inclusion in the core Boutiques standard, helping to standardize these improvements across the community.

## Cross-References

Now that you've explored advanced features, you might find these pages helpful:

- [Examples](./examples.md) - Complete descriptors demonstrating these concepts in action
- [Troubleshooting](./troubleshooting.md) - Solutions to common problems with descriptors
- [Subcommands](./subcommands.md) - More on hierarchical command structures
