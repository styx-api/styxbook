# File Handling in Boutiques

Handling input and output files is a core part of the Boutiques descriptor format. This page explains how to properly define file inputs and outputs in your descriptors.

> **Cross-reference**: For the basics of descriptor structure and parameters, see [Basic Structure](./basic_structure.md).  
> **Cross-reference**: For examples of file handling in complete descriptors, see [Examples](./examples.md).

## Input Files

Input files are specified using the `File` type in the `inputs` array:

```json
{
  "id": "image",
  "name": "Input Image",
  "description": "The input neuroimaging file",
  "type": "File",
  "value-key": "[INPUT]",
  "optional": false
}
```

### Key Considerations for Input Files

1. Always use `"type": "File"` for actual file paths
2. File inputs will be validated to ensure they exist when the tool is called
3. In containerized environments, file paths are automatically mapped to the container's filesystem

### Optional File Fields

Some additional fields that can be used with file inputs:

- `optional`: Whether the file is required
- `value-choices`: A list of predefined file options
- `default-value`: Default file path if not specified
- `list`: Whether multiple files can be provided (creates a file list)

## Output Files

Unlike inputs, output files are not parameters passed to the command line. Rather, they're specifications of what files will be produced by the tool. They're defined in the `output-files` array:

```json
"output-files": [
  {
    "id": "brain_mask",
    "name": "Brain Mask Image",
    "description": "Binary mask of the brain",
    "path-template": "[OUTPUT].mask.nii.gz",
    "optional": false
  }
]
```

### Path Templates

The `path-template` field defines where the output file will be created. It can use `value-key` placeholders from the inputs to construct dynamic paths:

```json
"inputs": [
  {
    "id": "output_dir",
    "name": "Output Directory",
    "type": "String",
    "value-key": "[OUTDIR]"
  },
  {
    "id": "subject_id",
    "name": "Subject ID",
    "type": "String",
    "value-key": "[SUBJECT]"
  }
],
"output-files": [
  {
    "id": "processed_image",
    "name": "Processed Image",
    "path-template": "[OUTDIR]/sub-[SUBJECT]/anat/image.nii.gz"
  }
]
```

### Extension Handling with path-template-stripped-extensions

A common pattern is to produce output files that have a similar name to input files but with different extensions. The `path-template-stripped-extensions` field helps with this:

```json
"inputs": [
  {
    "id": "input_image",
    "name": "Input Image",
    "type": "File",
    "value-key": "[INPUT]"
  }
],
"output-files": [
  {
    "id": "output_mask",
    "name": "Output Mask",
    "path-template": "[INPUT]_mask.nii.gz",
    "path-template-stripped-extensions": [".nii.gz", ".nii", ".img", ".hdr"]
  }
]
```

If the input is `subject1.nii.gz`, this would produce `subject1_mask.nii.gz` (not `subject1.nii.gz_mask.nii.gz`).

### Output File Fields

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `id` | Unique identifier | Yes | `"brain_mask"` |
| `name` | Human-readable name | Yes | `"Brain Mask Image"` |
| `description` | Detailed description | No | `"Binary mask of the brain"` |
| `path-template` | Template for output file path | Yes | `"[PREFIX]_mask.nii.gz"` |
| `optional` | Whether file might not be produced | No | `true` |
| `path-template-stripped-extensions` | Extensions to remove from input paths | No | `[".nii.gz", ".nii"]` |

## Subcommand Output Files

Each subcommand can have its own set of output files, which is particularly useful when different algorithms produce different outputs:

```json
{
  "id": "algorithm",
  "type": [
    {
      "id": "standard",
      "inputs": [...],
      "output-files": [
        {
          "id": "standard_output",
          "path-template": "[OUTPUT].nii.gz"
        }
      ]
    },
    {
      "id": "advanced",
      "inputs": [...],
      "output-files": [
        {
          "id": "advanced_output",
          "path-template": "[OUTPUT].nii.gz"
        },
        {
          "id": "quality_metrics",
          "path-template": "[OUTPUT]_qc.json"
        }
      ]
    }
  ]
}
```

## Capture Command Output

Sometimes tools output important data to stdout or stderr instead of files. The Styx ecosystem extends Boutiques with `stdout-output` and `stderr-output` fields to capture this data:

```json
"stdout-output": {
  "id": "coordinates",
  "name": "Extracted Coordinates", 
  "description": "Tab-separated coordinate values"
}
```

This is useful for tools that output structured data to stdout rather than files. The captured output is made available as a string in the generated bindings.

## Best Practices for File Handling

1. **Use `File` type for input files** and `String` type for output file paths
2. **Keep output paths flexible** by using placeholders from inputs
3. **Use `path-template-stripped-extensions`** to handle file extension changes
4. **Consider subcommand-specific outputs** when different modes produce different files
5. **Use `stdout-output` and `stderr-output`** for tools that output data to the terminal
6. **Make output files `optional: true`** if they might not be produced in all cases

## Container Considerations

When a tool runs in a container:

1. Input file paths are automatically mapped from the host to the container
2. Output files are mapped back from the container to the host
3. Relative paths are resolved relative to the working directory

The Styx execution environment handles these mappings transparently, but it's important to be aware of them when designing descriptors.

## Example: Complete File Handling

```json
{
  "name": "image_processor",
  "description": "Process neuroimaging files",
  "command-line": "process_image [INPUT] [OUTPUT] [OPTIONS]",
  "inputs": [
    {
      "id": "input_file",
      "name": "Input File",
      "description": "Input neuroimaging file",
      "type": "File",
      "value-key": "[INPUT]",
      "optional": false
    },
    {
      "id": "output_prefix",
      "name": "Output Prefix",
      "description": "Prefix for output files",
      "type": "String",
      "value-key": "[OUTPUT]",
      "optional": false
    },
    {
      "id": "verbose",
      "name": "Verbose Output",
      "description": "Enable detailed log messages",
      "type": "Flag",
      "command-line-flag": "-v",
      "value-key": "[OPTIONS]",
      "optional": true
    }
  ],
  "output-files": [
    {
      "id": "main_output",
      "name": "Processed Image",
      "description": "The main processed output image",
      "path-template": "[OUTPUT].nii.gz",
      "optional": false
    },
    {
      "id": "mask",
      "name": "Binary Mask",
      "description": "Binary mask from the processing",
      "path-template": "[OUTPUT]_mask.nii.gz",
      "optional": true
    },
    {
      "id": "report",
      "name": "Processing Report",
      "description": "HTML report with quality metrics",
      "path-template": "[OUTPUT]_report.html",
      "optional": true
    }
  ],
  "stdout-output": {
    "id": "processing_log",
    "name": "Processing Log",
    "description": "Detailed log of the processing steps"
  }
}
