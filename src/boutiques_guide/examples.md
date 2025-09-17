# Boutiques Descriptor Examples

This page provides complete examples of Boutiques descriptors for different types of tools, showcasing various features of the format.

## Basic Tool Example

A simple tool with input file, output file, and a few parameters:

```json
{
  "name": "image_converter",
  "description": "Converts between image formats with optional compression",
  "schema-version": "0.5+styx",
  "author": "Example Author",
  "url": "https://example.org/tool",
  "command-line": "convert_image [INPUT] [OUTPUT] [COMPRESSION] [VERBOSE]",
  "inputs": [
    {
      "id": "input_file",
      "name": "Input Image",
      "description": "The input image file to convert",
      "type": "File",
      "value-key": "[INPUT]",
      "optional": false
    },
    {
      "id": "output_file",
      "name": "Output Image",
      "description": "The output image file path",
      "type": "String",
      "value-key": "[OUTPUT]",
      "optional": false
    },
    {
      "id": "compression_level",
      "name": "Compression Level",
      "description": "Level of compression (0-9)",
      "type": "Number",
      "integer": true,
      "minimum": 0,
      "maximum": 9,
      "command-line-flag": "-c",
      "value-key": "[COMPRESSION]",
      "optional": true
    },
    {
      "id": "verbose",
      "name": "Verbose Output",
      "description": "Enable verbose logging",
      "type": "Flag",
      "command-line-flag": "-v",
      "value-key": "[VERBOSE]",
      "optional": true
    }
  ],
  "output-files": [
    {
      "id": "converted_image",
      "name": "Converted Image",
      "description": "The output converted image",
      "path-template": "[OUTPUT]",
      "optional": false
    }
  ],
  "stdout-output": {
    "id": "conversion_log",
    "name": "Conversion Log",
    "description": "Log of the conversion process"
  }
}
```

## Tool with Subcommands

A more complex tool with different algorithms, each having specific parameters:

```json
{
  "name": "brain_segmentation",
  "description": "Performs brain segmentation using different algorithms",
  "schema-version": "0.5+styx",
  "author": "Neuroimaging Lab",
  "url": "https://example.org/brain_segmentation",
  "command-line": "segment_brain [ALGORITHM] [GLOBAL_OPTIONS]",
  "inputs": [
    {
      "id": "algorithm",
      "name": "Algorithm",
      "description": "Segmentation algorithm to use",
      "value-key": "[ALGORITHM]",
      "optional": false,
      "type": [
        {
          "id": "atlas",
          "name": "Atlas-Based",
          "description": "Atlas-based segmentation",
          "command-line": "atlas [INPUT] [OUTPUT] [ATLAS_FILE] [ATLAS_OPTIONS]",
          "inputs": [
            {
              "id": "input",
              "name": "Input Image",
              "description": "Input brain image to segment",
              "type": "File",
              "value-key": "[INPUT]",
              "optional": false
            },
            {
              "id": "output",
              "name": "Output Directory",
              "description": "Output directory for segmentation results",
              "type": "String",
              "value-key": "[OUTPUT]",
              "optional": false
            },
            {
              "id": "atlas_file",
              "name": "Atlas File",
              "description": "Reference atlas file",
              "type": "File",
              "value-key": "[ATLAS_FILE]",
              "optional": false
            },
            {
              "id": "non_linear",
              "name": "Non-linear Registration",
              "description": "Use non-linear registration",
              "type": "Flag",
              "command-line-flag": "--nonlinear",
              "value-key": "[ATLAS_OPTIONS]",
              "optional": true
            }
          ],
          "output-files": [
            {
              "id": "segmentation",
              "name": "Segmentation Result",
              "description": "Segmented brain regions",
              "path-template": "[OUTPUT]/segmentation.nii.gz",
              "optional": false
            },
            {
              "id": "labels",
              "name": "Label Map",
              "description": "Label map for the segmentation",
              "path-template": "[OUTPUT]/labels.csv",
              "optional": false
            }
          ]
        },
        {
          "id": "deep",
          "name": "Deep Learning",
          "description": "Deep learning-based segmentation",
          "command-line": "deep [INPUT] [OUTPUT] [MODEL] [DEEP_OPTIONS]",
          "inputs": [
            {
              "id": "input",
              "name": "Input Image",
              "description": "Input brain image to segment",
              "type": "File",
              "value-key": "[INPUT]",
              "optional": false
            },
            {
              "id": "output",
              "name": "Output Directory",
              "description": "Output directory for segmentation results",
              "type": "String",
              "value-key": "[OUTPUT]",
              "optional": false
            },
            {
              "id": "model",
              "name": "Model Type",
              "description": "Deep learning model to use",
              "type": "String",
              "value-key": "[MODEL]",
              "value-choices": ["unet", "segnet", "densenet"],
              "optional": false
            },
            {
              "id": "batch_size",
              "name": "Batch Size",
              "description": "Processing batch size",
              "type": "Number",
              "integer": true,
              "minimum": 1,
              "maximum": 64,
              "command-line-flag": "--batch",
              "value-key": "[DEEP_OPTIONS]",
              "optional": true
            },
            {
              "id": "device",
              "name": "Computing Device",
              "description": "Device for computation",
              "type": "String",
              "command-line-flag": "--device",
              "value-key": "[DEEP_OPTIONS]",
              "value-choices": ["cpu", "cuda"],
              "optional": true
            }
          ],
          "output-files": [
            {
              "id": "segmentation",
              "name": "Segmentation Result",
              "description": "Segmented brain regions",
              "path-template": "[OUTPUT]/segmentation.nii.gz",
              "optional": false
            },
            {
              "id": "probability_maps",
              "name": "Probability Maps",
              "description": "Probability maps for each region",
              "path-template": "[OUTPUT]/probabilities.nii.gz",
              "optional": false
            },
            {
              "id": "metrics",
              "name": "Performance Metrics",
              "description": "Model performance metrics",
              "path-template": "[OUTPUT]/metrics.json",
              "optional": false
            }
          ]
        }
      ]
    },
    {
      "id": "threads",
      "name": "Number of Threads",
      "description": "Number of CPU threads to use",
      "type": "Number",
      "integer": true,
      "minimum": 1,
      "command-line-flag": "--threads",
      "value-key": "[GLOBAL_OPTIONS]",
      "optional": true
    },
    {
      "id": "verbose",
      "name": "Verbose Output",
      "description": "Enable verbose logging",
      "type": "Flag",
      "command-line-flag": "--verbose",
      "value-key": "[GLOBAL_OPTIONS]",
      "optional": true
    }
  ]
}
```

## Tool with Repeatable Subcommand

A tool where a subcommand can be repeated multiple times:

```json
{
  "name": "image_processor",
  "description": "Apply multiple image processing operations sequentially",
  "schema-version": "0.5+styx",
  "command-line": "process_image [INPUT] [OUTPUT] [OPERATIONS]",
  "inputs": [
    {
      "id": "input_file",
      "name": "Input Image",
      "description": "Input image to process",
      "type": "File",
      "value-key": "[INPUT]",
      "optional": false
    },
    {
      "id": "output_file",
      "name": "Output Image",
      "description": "Output processed image",
      "type": "String",
      "value-key": "[OUTPUT]",
      "optional": false
    },
    {
      "id": "operations",
      "name": "Processing Operations",
      "description": "Operations to apply (in order)",
      "type": {
        "id": "operation",
        "command-line": "--op [OPERATION] [PARAMS]",
        "inputs": [
          {
            "id": "operation_type",
            "name": "Operation Type",
            "description": "Type of image operation",
            "type": "String",
            "value-key": "[OPERATION]",
            "value-choices": ["blur", "sharpen", "resize", "rotate", "contrast"],
            "optional": false
          },
          {
            "id": "parameters",
            "name": "Operation Parameters",
            "description": "Parameters for the operation",
            "type": "Number",
            "list": true,
            "list-separator": ",",
            "value-key": "[PARAMS]",
            "optional": false
          }
        ]
      },
      "value-key": "[OPERATIONS]",
      "list": true,
      "optional": true
    }
  ],
  "output-files": [
    {
      "id": "processed_image",
      "name": "Processed Image",
      "description": "The output processed image",
      "path-template": "[OUTPUT]",
      "optional": false
    }
  ]
}
```

In this example, multiple operations can be specified:
```
process_image input.jpg output.jpg --op blur 3,3 --op rotate 90
```

## Tool with Nested Subcommands

Example with deeply nested subcommands:

```json
{
  "name": "data_analyzer",
  "description": "Analyze data with multiple methods and options",
  "schema-version": "0.5+styx",
  "command-line": "analyze [MODE] [GLOBAL_OPTIONS]",
  "inputs": [
    {
      "id": "mode",
      "name": "Analysis Mode",
      "description": "The type of analysis to perform",
      "value-key": "[MODE]",
      "optional": false,
      "type": [
        {
          "id": "statistical",
          "name": "Statistical Analysis",
          "description": "Perform statistical analysis",
          "command-line": "statistical [DATA] [STATS_OUTPUT] [STATS_METHOD]",
          "inputs": [
            {
              "id": "data_file",
              "name": "Data File",
              "description": "Input data file",
              "type": "File",
              "value-key": "[DATA]",
              "optional": false
            },
            {
              "id": "output_dir",
              "name": "Output Directory",
              "description": "Directory for output files",
              "type": "String",
              "value-key": "[STATS_OUTPUT]",
              "optional": false
            },
            {
              "id": "method",
              "name": "Statistical Method",
              "description": "Method for statistical analysis",
              "value-key": "[STATS_METHOD]",
              "optional": false,
              "type": [
                {
                  "id": "parametric",
                  "name": "Parametric Tests",
                  "description": "Parametric statistical tests",
                  "command-line": "parametric [PARAM_TEST] [PARAM_OPTIONS]",
                  "inputs": [
                    {
                      "id": "test_type",
                      "name": "Test Type",
                      "description": "Type of parametric test",
                      "type": "String",
                      "value-key": "[PARAM_TEST]",
                      "value-choices": ["ttest", "anova", "regression"],
                      "optional": false
                    },
                    {
                      "id": "alpha",
                      "name": "Alpha Level",
                      "description": "Significance level",
                      "type": "Number",
                      "integer": false,
                      "minimum": 0.001,
                      "maximum": 0.1,
                      "command-line-flag": "--alpha",
                      "value-key": "[PARAM_OPTIONS]",
                      "optional": true
                    }
                  ],
                  "output-files": [
                    {
                      "id": "parametric_results",
                      "name": "Parametric Test Results",
                      "description": "Results of the parametric test",
                      "path-template": "[STATS_OUTPUT]/parametric_results.csv",
                      "optional": false
                    }
                  ]
                },
                {
                  "id": "nonparametric",
                  "name": "Non-parametric Tests",
                  "description": "Non-parametric statistical tests",
                  "command-line": "nonparametric [NONPARAM_TEST] [NONPARAM_OPTIONS]",
                  "inputs": [
                    {
                      "id": "test_type",
                      "name": "Test Type",
                      "description": "Type of non-parametric test",
                      "type": "String",
                      "value-key": "[NONPARAM_TEST]",
                      "value-choices": ["wilcoxon", "kruskal", "friedman"],
                      "optional": false
                    },
                    {
                      "id": "exact",
                      "name": "Exact Test",
                      "description": "Use exact test calculations",
                      "type": "Flag",
                      "command-line-flag": "--exact",
                      "value-key": "[NONPARAM_OPTIONS]",
                      "optional": true
                    }
                  ],
                  "output-files": [
                    {
                      "id": "nonparametric_results",
                      "name": "Non-parametric Test Results",
                      "description": "Results of the non-parametric test",
                      "path-template": "[STATS_OUTPUT]/nonparametric_results.csv",
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
          "name": "Data Visualization",
          "description": "Create data visualizations",
          "command-line": "visualization [DATA] [VIZ_OUTPUT] [VIZ_TYPE] [VIZ_OPTIONS]",
          "inputs": [
            {
              "id": "data_file",
              "name": "Data File",
              "description": "Input data file",
              "type": "File",
              "value-key": "[DATA]",
              "optional": false
            },
            {
              "id": "output_dir",
              "name": "Output Directory",
              "description": "Directory for output files",
              "type": "String",
              "value-key": "[VIZ_OUTPUT]",
              "optional": false
            },
            {
              "id": "viz_type",
              "name": "Visualization Type",
              "description": "Type of visualization",
              "type": "String",
              "value-key": "[VIZ_TYPE]",
              "value-choices": ["boxplot", "histogram", "scatterplot", "heatmap"],
              "optional": false
            },
            {
              "id": "colormap",
              "name": "Color Map",
              "description": "Color map for the visualization",
              "type": "String",
              "command-line-flag": "--colormap",
              "value-key": "[VIZ_OPTIONS]",
              "value-choices": ["viridis", "plasma", "inferno", "magma", "cividis"],
              "optional": true
            },
            {
              "id": "dpi",
              "name": "DPI",
              "description": "Resolution in dots per inch",
              "type": "Number",
              "integer": true,
              "minimum": 72,
              "maximum": 1200,
              "command-line-flag": "--dpi",
              "value-key": "[VIZ_OPTIONS]",
              "optional": true
            }
          ],
          "output-files": [
            {
              "id": "visualization_file",
              "name": "Visualization File",
              "description": "Output visualization image",
              "path-template": "[VIZ_OUTPUT]/plot.png",
              "optional": false
            }
          ]
        }
      ]
    },
    {
      "id": "verbose",
      "name": "Verbose Output",
      "description": "Enable verbose output",
      "type": "Flag",
      "command-line-flag": "--verbose",
      "value-key": "[GLOBAL_OPTIONS]",
      "optional": true
    }
  ]
}
```

## Real-World Examples

For real-world examples check out the [descriptors in NiWrap](https://github.com/styx-api/niwrap/tree/main/descriptors).
