# Contributing to NiWrap

Thank you for your interest in contributing to NiWrap! This guide will help you understand how NiWrap works and how you can contribute to make it even better.

## Overview

NiWrap is a collection of Boutiques descriptors for neuroimaging tools. If you've found a bug in one of the interfaces or you're missing an interface, you can either report it in the [NiWrap issue tracker](https://github.com/styx-api/niwrap/issues) or attempt to fix it yourself by following this guide.

## Table of Contents

1. [Understanding NiWrap and Boutiques](#understanding-niwrap-and-boutiques)
2. [Repository Structure](#repository-structure)
3. [Development Environment Setup](#development-environment-setup)
4. [Contributing Descriptors](#contributing-descriptors)
5. [Working with Package Configurations](#working-with-package-configurations)
6. [Source Extraction](#source-extraction)
7. [Testing Your Changes](#testing-your-changes)
8. [Contribution Workflow](#contribution-workflow)
9. [Advanced Topics](#advanced-topics)
10. [Getting Help](#getting-help)

## Understanding NiWrap and Boutiques

NiWrap is a collection of Boutiques descriptors for neuroimaging tools. These descriptors are used by the [Styx](https://github.com/styx-api/styx) compiler to generate type-safe language bindings in Python, TypeScript, and R.

### What is Boutiques?

[Boutiques](https://boutiques.github.io/) is a JSON-based descriptive standard for command-line tools. It allows you to specify:

- Command-line arguments and their types
- Input and output files
- Dependencies between parameters
- Container configurations
- And much more

Boutiques descriptors serve as the "source of truth" for NiWrap, defining how each neuroimaging tool works and how users can interact with it.

> **Note:** For a comprehensive guide to Boutiques concepts and advanced usage, see the [Boutiques Guide](../boutiques_guide/README.md) section of this documentation.

Here's a simplified example of a Boutiques descriptor:

```json
{
  "name": "example_tool",
  "description": "An example neuroimaging tool",
  "tool-version": "1.0.0",
  "command-line": "example_tool [INPUT] [OUTPUT] [OPTIONS]",
  "inputs": [
    {
      "id": "input_file",
      "name": "Input file",
      "type": "File",
      "value-key": "[INPUT]",
      "optional": false
    },
    {
      "id": "output_file",
      "name": "Output file",
      "type": "String",
      "value-key": "[OUTPUT]",
      "optional": false
    },
    {
      "id": "verbose",
      "name": "Verbose output",
      "type": "Flag",
      "command-line-flag": "-v",
      "optional": true
    }
  ],
  "output-files": [
    {
      "id": "output",
      "name": "Output file",
      "path-template": "[OUTPUT]"
    }
  ]
}
```

This descriptor defines a tool with an input file, output file, and a verbose flag. The Styx compiler transforms this into type-safe language bindings that users can call from their preferred programming language.

## Repository Structure

The NiWrap repository is organized as follows:

```
niwrap/
├── build-templates/      # Templates used during the build process
├── build.py              # Main build script for generating language bindings
├── descriptors/          # Boutiques descriptors for each tool
│   ├── afni/             # AFNI tools
│   ├── ants/             # ANTs tools
│   ├── fsl/              # FSL tools
│   └── ...
├── extraction/           # Tools for extracting parameter information
├── packages/             # Package configuration files
├── schemas/              # JSON schemas for validation
├── scripts/              # Utility scripts for maintaining descriptors
├── tests/                # Tests for descriptors
└── update_readme.py      # Script to update the README with current tool coverage
```

## Development Environment Setup

Setting up a proper development environment will make contributing to NiWrap more efficient.

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/styx-api/niwrap.git
cd niwrap

# Install required dependencies using pip
pip install pytest
pip install git+https://github.com/styx-api/styx.git
```

> **Note:** A formal `requirements.txt` file may be added in the future. For now, installing pytest and the Styx compiler from GitHub should be sufficient for most development tasks.

### VSCode JSON Schema Validation

Visual Studio Code users can enable automatic validation and autocompletion for Boutiques descriptors by configuring JSON schema validation:

1. Create or open `.vscode/settings.json` in your NiWrap repository
2. Add the following configuration:

```json
{
    "json.schemas": [
        {
            "fileMatch": [
                "descriptors/**/*.json"
            ],
            "url": "./schemas/descriptor.schema.json"
        }
    ]
}
```

This setup provides real-time feedback as you edit descriptor files, highlighting potential errors and offering suggestions based on the Boutiques schema.

## Contributing Descriptors

The most common contribution to NiWrap is adding or improving Boutiques descriptors for neuroimaging tools.

### Finding the Right Location

Descriptors are organized by tool suite in the `descriptors/` directory:

```
descriptors/
├── afni/        # AFNI tools
├── ants/        # ANTs tools
├── fsl/         # FSL tools
├── mrtrix3/     # MRTrix3 tools
└── ...
```

Place your descriptor in the appropriate directory, or create a new directory if you're adding a tool from a new suite.

### Fixing an Existing Descriptor

If you've found a bug in an existing tool interface, you'll need to modify its descriptor.

#### Example: Fixing a Parameter Type

Let's say you discovered that the `fractional_intensity` parameter in FSL's BET tool should be a floating-point number between 0 and 1, but it's currently defined as an integer:

```json
// Original descriptor (simplified)
{
  "name": "bet",
  "inputs": [
    {
      "id": "fractional_intensity",
      "name": "Fractional intensity threshold",
      "type": "Number",
      "integer": true,
      "minimum": 0,
      "maximum": 1
    }
  ]
}
```

To fix this, you'd change the descriptor to:

```json
// Fixed descriptor
{
  "name": "bet",
  "inputs": [
    {
      "id": "fractional_intensity",
      "name": "Fractional intensity threshold",
      "type": "Number",
      "integer": false,
      "minimum": 0,
      "maximum": 1
    }
  ]
}
```

### Adding a Missing Parameter

If a tool has a parameter that isn't exposed in NiWrap, you can add it to the descriptor.

#### Example: Adding a Missing Flag

Suppose FSL's FAST tool has a `-N` flag for no bias field correction, but it's missing from the descriptor:

```json
// Original descriptor (simplified)
{
  "name": "fast",
  "inputs": [
    // existing parameters
  ]
}
```

You would add the new parameter:

```json
// Updated descriptor
{
  "name": "fast",
  "inputs": [
    // existing parameters
    {
      "id": "no_bias_field_correction",
      "name": "No bias field correction",
      "type": "Flag",
      "command-line-flag": "-N",
      "description": "Turns off bias field correction"
    }
  ]
}
```

### Creating a New Descriptor

If you want to add support for a completely new tool, you'll need to create a new descriptor from scratch.

#### Example: Creating a New Descriptor

Here's a simplified example of creating a descriptor for a fictional tool called `brainanalyze`:

```json
{
  "name": "brainanalyze",
  "tool-version": "1.0.0",
  "description": "Analyzes brain structures in neuroimaging data",
  "command-line": "brainanalyze [INPUT] [OUTPUT] [OPTIONS]",
  "container-image": {
    "image": "neuroimaging/brainanalyze:1.0.0",
    "type": "docker"
  },
  "inputs": [
    {
      "id": "input_file",
      "name": "Input file",
      "type": "File",
      "value-key": "[INPUT]",
      "description": "Input neuroimaging file (NIFTI format)",
      "optional": false
    },
    {
      "id": "output_file",
      "name": "Output file",
      "type": "String",
      "value-key": "[OUTPUT]",
      "description": "Output file path",
      "optional": false
    },
    {
      "id": "smoothing",
      "name": "Smoothing factor",
      "type": "Number",
      "value-key": "[OPTIONS]",
      "command-line-flag": "-s",
      "integer": false,
      "minimum": 0,
      "maximum": 10,
      "description": "Smoothing factor (0-10)",
      "optional": true,
      "default-value": 2.5
    }
  ],
  "output-files": [
    {
      "id": "output",
      "name": "Output file",
      "path-template": "[OUTPUT]",
      "description": "Output analysis file"
    }
  ]
}
```

## Working with Package Configurations

The `packages/` directory contains package-level configuration files that define metadata for each neuroimaging tool suite.

### Package Configuration Structure

A typical package configuration file looks like this:

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
      // More endpoints...
    ]
  }
}
```

The `status` field in each endpoint entry can have one of three values:
- `"done"`: The descriptor is complete and ready for use
- `"missing"`: The tool is identified but the descriptor is not yet created
- `"ignore"`: The tool should be deliberately excluded from the API

### Updating Package Configurations

When adding or modifying descriptors, remember to update the corresponding package configuration:

1. For a new tool, add a new endpoint entry in the appropriate package file
2. When updating a tool descriptor, ensure its status is set to `"done"`
3. If adding a new tool suite, create a new package configuration file

## Source Extraction

NiWrap's `extraction` directory contains specialized code that modifies the source code of neuroimaging toolboxes to programmatically extract tool information.

### How Source Extraction Works

Source extraction involves:

1. Modifying the original source code of a neuroimaging tool
2. Adding instrumentation to dump tool information during compilation or runtime
3. Capturing this information in a structured format that can be transformed into Boutiques descriptors

This is an advanced contribution area that typically requires:
- Understanding of the tool's source code and architecture
- Programming skills in the language the tool is written in
- Familiarity with the tool's command-line interface

### Using LLM Prompts for Initial Descriptor Creation

The `extraction` directory also contains LLM (Large Language Model) prompts that can help bootstrap the creation of descriptors:

1. Capture the help text of a neuroimaging tool:
   ```bash
   mytool --help > tool_help.txt
   ```

2. Use the provided LLM prompts with a model like Claude or GPT to generate an initial Boutiques descriptor:
   ```
   # Example prompt structure (check extraction directory for specifics)
   Given the following help text for a neuroimaging tool, create a Boutiques descriptor:
   
   [Paste help text]
   ```

3. Review and refine the generated descriptor to ensure accuracy
4. Place the final descriptor in the appropriate directory under `descriptors/`

This approach is particularly useful for tools without structured extraction capabilities and can significantly speed up the initial descriptor creation process.

### For Tool Maintainers

If you're a maintainer of a neuroimaging tool and would like to collaborate on better integration with NiWrap:

- We welcome direct collaboration on source extraction
- This can ensure that your tool's interface is accurately represented in NiWrap
- Contact the NiWrap team through GitHub issues to discuss collaboration opportunities

## Testing Your Changes

After modifying or creating descriptors, you should test them to ensure they work correctly:

1. Use the NiWrap test suite:
   ```bash
   # Run tests for a specific tool
   python -m pytest tests/test_descriptors.py::test_descriptor_validity::test_tool_descriptor
   ```

2. Build the project to check if your descriptors can be processed by Styx:
   ```bash
   python build.py
   ```

> **Note:** NiWrap does not use the original Boutiques runtime (`bosh`). All testing and validation should be done using NiWrap's own build and test utilities.

## Contribution Workflow

Here's a step-by-step guide to contributing to NiWrap:

1. **Fork the repository**: Create your own fork of NiWrap on GitHub
2. **Clone your fork**: 
   ```bash
   git clone https://github.com/your-username/niwrap.git
   cd niwrap
   ```
3. **Create a branch**: 
   ```bash
   git checkout -b fix-fsl-bet-descriptor
   ```
4. **Make changes**: Modify or add descriptors in the appropriate directory
5. **Update package configuration**: If necessary, update the corresponding package configuration file
6. **Test**: Ensure your changes work correctly using the testing methods described above
7. **Commit your changes**:
   ```bash
   git add descriptors/fsl/bet.json packages/fsl.json
   git commit -m "Fix: Update FSL BET fractional intensity parameter type"
   ```
8. **Push your changes**:
   ```bash
   git push origin fix-fsl-bet-descriptor
   ```
9. **Submit a PR**: Create a pull request on GitHub with a clear description of your changes

## Advanced Topics

### Adding a New Tool Suite

If you want to add support for an entirely new neuroimaging tool suite (e.g., adding a new package like SPM or BrainSuite):

1. Create a new directory in `descriptors/` for the tool suite
2. Create descriptors for each tool you want to support
3. Create a new package configuration file in `packages/`
4. Consider creating extraction scripts in the `extraction/` directory

### Creating Helper Scripts

For complex tools, you might need to create helper scripts to streamline the creation of descriptors:

1. Add your script to the `scripts/` directory
2. Document its usage in a comment at the top of the script
3. Reference it in your pull request to help maintainers understand its purpose

## Getting Help

If you're unsure about anything or need guidance, you can:

- Open an issue in the [NiWrap issue tracker](https://github.com/styx-api/niwrap/issues)
- Check the [Boutiques documentation](https://boutiques.github.io/doc/)
- Consult the [Styx Book](https://styx-api.github.io/styxbook/)
- Review existing descriptors for similar tools as examples

Feel free to ask specific questions in your issue or pull request. The maintainers are happy to help guide you through the process.

Thank you for contributing to NiWrap and helping make neuroimaging analysis more accessible across multiple programming languages!