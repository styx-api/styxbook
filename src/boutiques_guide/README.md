# Boutiques Format in the Styx Ecosystem

## What is Boutiques?

Boutiques is a JSON-based descriptive standard for command-line tools. It provides a structured way to specify:

- Command-line arguments and their types
- Input and output files
- Dependencies between parameters
- Container configurations
- And much more

In the Styx ecosystem, Boutiques descriptors serve as the "source of truth" that defines how each tool works and how users can interact with it.

## Role in the Styx Ecosystem

Styx is a general-purpose compiler that transforms structured tool descriptions (currently using Boutiques format) into type-safe language bindings for Python, TypeScript, and R. While NiWrap focuses specifically on neuroimaging tools, Styx itself works with any command-line tool that can be described in a structured format.

The workflow is:

1. Tool interfaces are defined in Boutiques descriptors
2. Styx processes these descriptors to generate language bindings
3. Users access the tools through type-safe interfaces in their preferred language

This approach allows you to:
- Define a tool interface once and use it in multiple languages
- Leverage type-checking to catch errors at compile time
- Focus on your work instead of wrestling with command-line arguments

## Extensions to the Standard

While Styx is compatible with the core Boutiques format, we've added several extensions to better support complex tools:

- **Subcommands:** Hierarchical command structures with different parameter sets
- **Stdout/Stderr as outputs:** Capturing command output as structured data
- **Enhanced parameter types:** Additional validation and type information
- **Path extension handling:** Smart handling of file extensions

These extensions are being proposed for inclusion in the core Boutiques standard.

## Guide Structure

This guide is organized into several sections:

1. [Basic Structure](./basic_structure.md) - Core fields, parameter types, and command-line formation
2. [Subcommands](./subcommands.md) - Detailed explanation of the subcommand extension
3. [File Handling](./file_handling.md) - Input/output file handling, path templates, extensions
4. [Advanced Features](./advanced_features.md) - Additional fields, extensions, and configuration options
5. [Examples](./examples.md) - Complete examples showing different patterns

## Quick Example

Here's a simplified example of a Boutiques descriptor:

```json
{
  "name": "example_tool",
  "description": "An example tool",
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
      "value-key": "[OPTIONS]",
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

## Next Steps

Start with the [Basic Structure](./basic_structure.md) section to learn the core concepts of the Boutiques format as used in the Styx ecosystem.