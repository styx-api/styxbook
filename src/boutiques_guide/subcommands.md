# Subcommands in Boutiques

Subcommands are a powerful extension to the Boutiques format in the Styx ecosystem. They allow describing tools with complex, hierarchical command structures where different "modes" or "algorithms" have different parameter sets.

## Basic Concept

A subcommand is specified by making the `type` field of a parameter either:

1. An object (for a single subcommand type)
2. An array of objects (for a union of subcommand types)

Each subcommand object defines its own set of inputs, command-line, and outputs.

## Subcommand vs. Groups

While standard Boutiques uses `groups` with options like `mutually-exclusive` to handle related parameters, the Styx ecosystem favors subcommands because they:

- Create proper type hierarchies in generated bindings
- Allow for nested parameter structures
- Enable clear validation at compile-time rather than runtime
- Support different output files per subcommand

## Subcommand Union (Selection)

The most common use of subcommands is to represent different "modes" or "algorithms" where the user must select exactly one option:

```json
{
  "id": "algorithm",
  "name": "Algorithm",
  "description": "Select processing algorithm",
  "value-key": "[ALGORITHM]",
  "type": [
    {
      "id": "fast",
      "name": "Fast Algorithm",
      "description": "Quick but less accurate",
      "command-line": "fast [FAST_INPUT] [FAST_OUTPUT]",
      "inputs": [
        {
          "id": "input",
          "name": "Input File",
          "value-key": "[FAST_INPUT]",
          "type": "File",
          "optional": false
        },
        {
          "id": "output",
          "name": "Output File",
          "value-key": "[FAST_OUTPUT]",
          "type": "String",
          "optional": false
        }
      ],
      "output-files": [
        {
          "id": "output",
          "name": "Output",
          "path-template": "[FAST_OUTPUT]"
        }
      ]
    },
    {
      "id": "accurate",
      "name": "Accurate Algorithm",
      "description": "Slower but more accurate",
      "command-line": "accurate [ACCURATE_INPUT] [ACCURATE_OUTPUT] [PRECISION]",
      "inputs": [
        {
          "id": "input",
          "name": "Input File",
          "value-key": "[ACCURATE_INPUT]",
          "type": "File",
          "optional": false
        },
        {
          "id": "output",
          "name": "Output File",
          "value-key": "[ACCURATE_OUTPUT]",
          "type": "String",
          "optional": false
        },
        {
          "id": "precision",
          "name": "Precision",
          "value-key": "[PRECISION]",
          "command-line-flag": "-p",
          "type": "Number",
          "integer": true,
          "minimum": 1,
          "maximum": 10,
          "optional": true,
          "default-value": 5
        }
      ],
      "output-files": [
        {
          "id": "output",
          "name": "Output",
          "path-template": "[ACCURATE_OUTPUT]"
        },
        {
          "id": "metrics",
          "name": "Performance Metrics",
          "path-template": "[ACCURATE_OUTPUT].metrics.json"
        }
      ]
    }
  ]
}
```

In this example:
- The user must choose either the "fast" or "accurate" algorithm
- Each algorithm has its own specific parameters
- The "accurate" algorithm produces an additional output file

## Single Subcommand (Configuration)

Sometimes you need a group of related parameters that are always used together. A single subcommand (where `type` is an object, not an array) can represent this configuration:

```json
{
  "id": "config",
  "name": "Configuration",
  "value-key": "[CONFIG]",
  "command-line-flag": "--config",
  "type": {
    "id": "config_options",
    "command-line": "[KEY] [VALUE]",
    "inputs": [
      {
        "id": "key",
        "name": "Key",
        "value-key": "[KEY]",
        "type": "String",
        "optional": false
      },
      {
        "id": "value",
        "name": "Value",
        "value-key": "[VALUE]",
        "type": "String",
        "optional": false
      }
    ]
  },
  "optional": true
}
```

## Repeatable Subcommands

Subcommands can be made repeatable by adding `"list": true`:

```json
{
  "id": "transformations",
  "name": "Transformations",
  "list": true,
  "type": {
    "id": "transform",
    "command-line": "--transform [TYPE] [PARAMETERS]",
    "inputs": [
      {
        "id": "type",
        "name": "Type",
        "value-key": "[TYPE]",
        "type": "String",
        "value-choices": ["rotate", "scale", "translate"],
        "optional": false
      },
      {
        "id": "parameters",
        "name": "Parameters",
        "value-key": "[PARAMETERS]",
        "type": "Number",
        "list": true,
        "optional": false
      }
    ]
  },
  "optional": true
}
```

This allows specifying multiple transformations with different parameters, which would result in something like:

```
--transform rotate 0 0 90 --transform scale 2 2 1
```

## Nested Subcommands

Subcommands can be nested multiple levels deep to represent complex tool hierarchies:

```json
{
  "id": "mode",
  "type": [
    {
      "id": "analysis",
      "command-line": "analysis [METHOD]",
      "inputs": [
        {
          "id": "method",
          "value-key": "[METHOD]",
          "type": [
            {
              "id": "parametric",
              "command-line": "parametric [MODEL]",
              "inputs": [
                {
                  "id": "model",
                  "value-key": "[MODEL]",
                  "type": "String",
                  "value-choices": ["linear", "quadratic", "exponential"],
                  "optional": false
                }
              ]
            },
            {
              "id": "nonparametric",
              "command-line": "nonparametric [KERNEL]",
              "inputs": [
                {
                  "id": "kernel",
                  "value-key": "[KERNEL]",
                  "type": "String",
                  "value-choices": ["gaussian", "uniform"],
                  "optional": false
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "visualization",
      "command-line": "visualization [VIZ_OPTIONS]",
      "inputs": [
        {
          "id": "type",
          "value-key": "[VIZ_OPTIONS]",
          "command-line-flag": "--type",
          "type": "String",
          "value-choices": ["2d", "3d", "interactive"],
          "optional": false
        }
      ]
    }
  ]
}
```

## Real-World Example: MRTrix3 5ttgen

Here's a simplified version of how MRTrix3's 5ttgen tool is described with subcommands:

```json
{
  "name": "5ttgen",
  "description": "Generate a 5TT image suitable for ACT.",
  "command-line": "5ttgen [ALGORITHM] [OPTIONS]",
  "inputs": [
    {
      "id": "algorithm",
      "name": "algorithm",
      "value-key": "[ALGORITHM]",
      "description": "Select the algorithm to be used",
      "type": [
        {
          "id": "freesurfer",
          "name": "freesurfer",
          "description": "Generate the 5TT image based on a FreeSurfer parcellation",
          "command-line": "freesurfer [INPUT] [OUTPUT] [OPTIONS_LUT]",
          "inputs": [
            {
              "id": "input",
              "name": "input",
              "value-key": "[INPUT]",
              "description": "The input FreeSurfer parcellation image",
              "type": "File",
              "optional": false
            },
            {
              "id": "output",
              "name": "output",
              "value-key": "[OUTPUT]",
              "description": "The output 5TT image",
              "type": "String",
              "optional": false
            },
            {
              "id": "lut",
              "name": "lut",
              "command-line-flag": "-lut",
              "value-key": "[OPTIONS_LUT]",
              "description": "Lookup table path",
              "type": "File",
              "optional": true
            }
          ],
          "output-files": [
            {
              "id": "output",
              "name": "output",
              "path-template": "[OUTPUT]",
              "description": "The output 5TT image"
            }
          ]
        },
        {
          "id": "fsl",
          "name": "fsl",
          "description": "Use FSL commands to generate the 5TT image",
          "command-line": "fsl [INPUT] [OUTPUT] [OPTIONS]",
          "inputs": [
            {
              "id": "input",
              "name": "input",
              "value-key": "[INPUT]",
              "description": "The input T1-weighted image",
              "type": "File",
              "optional": false
            },
            {
              "id": "output",
              "name": "output",
              "value-key": "[OUTPUT]",
              "description": "The output 5TT image",
              "type": "String",
              "optional": false
            },
            {
              "id": "t2",
              "name": "t2",
              "command-line-flag": "-t2",
              "value-key": "[OPTIONS]",
              "description": "Provide a T2-weighted image",
              "type": "File",
              "optional": true
            }
          ],
          "output-files": [
            {
              "id": "output",
              "name": "output",
              "path-template": "[OUTPUT]",
              "description": "The output 5TT image"
            }
          ]
        }
      ]
    },
    {
      "id": "nocrop",
      "name": "nocrop",
      "value-key": "[OPTIONS]",
      "command-line-flag": "-nocrop",
      "description": "Do NOT crop the resulting 5TT image",
      "type": "Flag",
      "optional": true
    }
  ]
}
```

## Generated Bindings

When Styx compiles a descriptor with subcommands, it creates type-safe bindings that reflect the hierarchical structure. For example, in TypeScript:

```typescript
// For the algorithm example
type AlgorithmOptions = 
  | { algorithm: "fast", input: string, output: string }
  | { algorithm: "accurate", input: string, output: string, precision?: number };

function processData(options: AlgorithmOptions): void {
  // Implementation
}
```

This ensures users can only provide valid parameter combinations.

## Best Practices for Subcommands

1. **Use subcommands for mutually exclusive options** instead of groups
2. **Keep subcommand IDs unique** across the entire descriptor
3. **Use descriptive names** for each subcommand option
4. **Consider output files carefully** - each subcommand can have different outputs
5. **Nest subcommands when it makes logical sense** for the tool's structure
6. **Use value-choices for fixed option sets** within subcommands
7. **Add list: true for repeatable elements** when the same subcommand can appear multiple times

## Next Steps

Now that you understand subcommands, learn about:
- [File Handling](./file_handling.md) - For detailed input/output file handling
- [Advanced Features](./advanced_features.md) - For additional capabilities