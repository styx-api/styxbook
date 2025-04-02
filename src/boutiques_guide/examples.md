different types of tools, showcasing various features of the format.

## Basic Tool Example

A simple tool with input file, output file, and a few parameters:

```json
{
  "name": "image_converter",
  "description": "Converts between image formats with optional compression",
  "tool-version": "1.0.0",
  "schema-version": "0.5",
  "author": "Example Author",
  "url": "https://example.org/tool",
  "command-line": "convert_image [INPUT] [OUTPUT] [COMPRESSION] [VERBOSE]",
  "container-image": {
    "type": "docker",
    "image": "example/image_converter:1.0.0"
  }

## Real-World Example: MRTrix3 5ttgen

This example shows the 5ttgen tool from MRTrix3, which demonstrates subcommand usage:

```json
{
  "name": "5ttgen",
  "description": "Generate a 5TT image suitable for ACT",
  "author": "MRTrix3 Developers",
  "tool-version": "3.0.4",
  "schema-version": "0.5",
  "container-image": {
    "image": "mrtrix3/mrtrix3:3.0.4",
    "type": "docker"
  },
  "command-line": "5ttgen [ALGORITHM] [NOCROP] [OPTIONS]",
  "inputs": [
    {
      "id": "algorithm",
      "name": "algorithm",
      "value-key": "[ALGORITHM]",
      "description": "Select the algorithm to be used; additional details and options become available once an algorithm is nominated",
      "type": [  // The type is an array of objects = Selection from multiple algorithms
        {
          "id": "freesurfer",
          "name": "freesurfer",
          "description": "Generate the 5TT image based on a FreeSurfer parcellation image",
          "command-line": "freesurfer [INPUT] [OUTPUT] [OPTIONS_LUT]",
          "inputs": [  // Each algorithm has its own parameter set
            {
              "id": "input",
              "name": "input",
              "value-key": "[INPUT]",
              "description": "The input FreeSurfer parcellation image (any image containing 'aseg' in its name)",
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
              "description": "Manually provide path to the lookup table on which the input parcellation image is based",
              "type": "File",
              "optional": true
            }
          ],
          "output-files": [  // Each algorithm can have its own outputs
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
          "description": "Use FSL commands to generate the 5TT image based on a T1-weighted image",
          "command-line": "fsl [INPUT] [OUTPUT] [OPTIONS_T2] [OPTIONS_MASK]",
          "inputs": [  // FSL algorithm has different parameter requirements
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
              "value-key": "[OPTIONS_T2]",
              "description": "Provide a T2-weighted image in addition to the default T1-weighted image",
              "type": "File",
              "optional": true
            },
            {
              "id": "mask",
              "name": "mask",
              "command-line-flag": "-mask",
              "value-key": "[OPTIONS_MASK]",
              "description": "Manually provide a brain mask, rather than deriving one in the script",
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
      "value-key": "[NOCROP]",
      "command-line-flag": "-nocrop",
      "description": "Do NOT crop the resulting 5TT image to reduce its size",
      "type": "Flag",
      "optional": true
    },
    {
      "id": "nthreads",
      "name": "nthreads",
      "command-line-flag": "-nthreads",
      "value-key": "[OPTIONS]",
      "description": "Use this number of threads in multi-threaded applications",
      "type": "Number",
      "optional": true,
      "integer": true
    }
  ]
}
```

## Example with Stdout and Stderr Capture

This example demonstrates capturing command output:

```json
{
  "name": "data_finder",
  "description": "Search for patterns in data files and extract statistics",
  "tool-version": "1.0.0",
  "schema-version": "0.5",
  "command-line": "find_patterns [INPUT] [PATTERN] [OPTIONS]",
  "inputs": [
    {
      "id": "input_file",
      "name": "Input File",
      "description": "Data file to search",
      "type": "File",
      "value-key": "[INPUT]",
      "optional": false
    },
    {
      "id": "pattern",
      "name": "Search Pattern",
      "description": "Pattern to search for",
      "type": "String",
      "value-key": "[PATTERN]",
      "optional": false
    },
    {
      "id": "max_matches",
      "name": "Maximum Matches",
      "description": "Maximum number of matches to return",
      "type": "Number",
      "integer": true,
      "minimum": 1,
      "command-line-flag": "--max",
      "value-key": "[OPTIONS]",
      "optional": true,
      "default-value": 100
    },
    {
      "id": "output_format",
      "name": "Output Format",
      "description": "Format for the output results",
      "type": "String",
      "command-line-flag": "--format",
      "value-key": "[OPTIONS]",
      "value-choices": ["csv", "json", "xml", "txt"],
      "optional": true,
      "default-value": "txt"
    }
  ],
  "stdout-output": {
    "id": "matches",
    "name": "Found Matches",
    "description": "Matching patterns found in the data"
  },
  "stderr-output": {
    "id": "warnings",
    "name": "Warning Messages",
    "description": "Warning messages generated during pattern search"
  }
}
```

## Application to Generated Bindings

When Styx processes these descriptors, it creates type-safe bindings. For example, the MRTrix3 5ttgen tool in Python might look like:

```python
from niwrap.mrtrix3 import generate_5tt

# Using FreeSurfer algorithm
generate_5tt.freesurfer(
    input="subject01/mri/aseg.mgz",
    output="subject01/5tt.mif"
)

# Using FSL algorithm with T2 image
generate_5tt.fsl(
    input="subject01/T1.nii.gz",
    output="subject01/5tt.mif",
    t2="subject01/T2.nii.gz"
)
```

Or the brain segmentation tool in TypeScript:

```typescript
import { brainSegmentation } from 'niwrap';

// Using atlas-based algorithm
await brainSegmentation.atlas({
  input: 'subject01/T1.nii.gz',
  output: 'subject01/atlas_output',
  atlas_file: 'templates/standard_atlas.nii.gz',
  non_linear: true
});

// Using deep learning algorithm
await brainSegmentation.deep({
  input: 'subject01/T1.nii.gz',
  output: 'subject01/deep_output',
  model: 'unet',
  batch_size: 16,
  device: 'cuda'
});
```

These examples demonstrate how the hierarchical structure in Boutiques descriptors translates to clean, type-safe APIs in the target languages.
,
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
      "optional": true,
      "default-value": 5
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
  "tool-version": "2.1.0",
  "schema-version": "0.5",
  "author": "Neuroimaging Lab",
  "url": "https://example.org/brain_segmentation",
  "command-line": "segment_brain [ALGORITHM] [GLOBAL_OPTIONS]",
  "container-image": {
    "type": "docker",
    "image": "neuroimaging/segmentation:2.1.0"
  },
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
              "optional": true,
              "default-value": 8
            },
            {
              "id": "device",
              "name": "Computing Device",
              "description": "Device for computation",
              "type": "String",
              "command-line-flag": "--device",
              "value-key": "[DEEP_OPTIONS]",
              "value-choices": ["cpu", "cuda"],
              "optional": true,
              "default-value": "cpu"
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
      "optional": true,
      "default-value": 4
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
  "tool-version": "1.2.0",
  "schema-version": "0.5",
  "command-line": "process_image [INPUT] [OUTPUT] [OPERATIONS]",
  "container-image": {
    "type": "docker",
    "image": "example/image_processor:1.2.0"
  },
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
  "tool-version": "3.0.0",
  "schema-version": "0.5",
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
                      "optional": true,
                      "default-value": 0.05
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
              "optional": true,
              "default-value": "viridis"
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
              "optional": true,
              "default-value": 300
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

## Real-World Example: FSL BET

Here's a simplified version of the FSL BET (Brain Extraction Tool) descriptor:

```json
{
  "tool-version": "6.0.4",
  "name": "bet",
  "author": "FMRIB Analysis Group, University of Oxford",
  "description": "Automated brain extraction tool for FSL",
  "url": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki",
  "command-line": "bet [INFILE] [MASKFILE] [FRACTIONAL_INTENSITY] [VG_FRACTIONAL_INTENSITY] [CENTER_OF_GRAVITY] [OVERLAY] [BINARY_MASK] [APPROX_SKULL] [NO_SEG_OUTPUT] [VTK_MESH] [HEAD_RADIUS] [THRESHOLDING] [VERBOSE]",
  "container-image": {
    "type": "docker",
    "image": "brainlife/fsl:6.0.4-patched2"
  },
  "inputs": [
    {
      "description": "Input image (e.g. img.nii.gz)",
      "value-key": "[INFILE]",
      "type": "File",
      "optional": false,
      "id": "infile",
      "name": "Input file"
    },
    {
      "description": "Output brain mask (e.g. img_bet.nii.gz)",
      "value-key": "[MASKFILE]",
      "type": "String",
      "optional": false,
      "id": "maskfile",
      "name": "Mask file",
      "default-value": "img_bet"
    },
    {
      "command-line-flag": "-f",
      "description": "Fractional intensity threshold (0->1); default=0.5; smaller values give larger brain outline estimates",
      "value-key": "[FRACTIONAL_INTENSITY]",
      "type": "Number",
      "maximum": 1,
      "minimum": 0,
      "integer": false,
      "optional": true,
      "id": "fractional_intensity",
      "name": "Fractional intensity threshold"
    },
    {
      "command-line-flag": "-g",
      "description": "Vertical gradient in fractional intensity threshold (-1->1); default=0; positive values give larger brain outline at bottom, smaller at top",
      "value-key": "[VG_FRACTIONAL_INTENSITY]",
      "type": "Number",
      "maximum": 1,
      "minimum": -1,
      "integer": false,
      "optional": true,
      "id": "vg_fractional_intensity",
      "name": "Vertical gradient fractional intensity threshold"
    },
    {
      "command-line-flag": "-c",
      "description": "The xyz coordinates of the center of gravity (voxels, not mm) of initial mesh surface.",
      "value-key": "[CENTER_OF_GRAVITY]",
      "type": "Number",
      "list": true,
      "max-list-entries": 3,
      "min-list-entries": 3,
      "optional": true,
      "id": "center_of_gravity",
      "name": "Center of gravity vector"
    },
    {
      "command-line-flag": "-o",
      "description": "Generate brain surface outline overlaid onto original image",
      "value-key": "[OVERLAY]",
      "type": "Flag",
      "optional": true,
      "id": "overlay",
      "name": "Overlay flag"
    },
    {
      "command-line-flag": "-m",
      "description": "Generate binary brain mask",
      "value-key": "[BINARY_MASK]",
      "type": "Flag",
      "optional": true,
      "id": "binary_mask",
      "name": "Binary mask flag"
    },
    {
      "command-line-flag": "-s",
      "description": "Generate rough skull image (not as clean as betsurf)",
      "value-key": "[APPROX_SKULL]",
      "type": "Flag",
      "optional": true,
      "id": "approx_skull",
      "name": "Approximate skull flag"
    },
    {
      "command-line-flag": "-n",
      "description": "Don't generate segmented brain image output",
      "value-key": "[NO_SEG_OUTPUT]",
      "type": "Flag",
      "optional": true,
      "id": "no_seg_output",
      "name": "No segmented brain image flag"
    },
    {
      "command-line-flag": "-e",
      "description": "Generate brain surface as mesh in .vtk format",
      "value-key": "[VTK_MESH]",
      "type": "Flag",
      "optional": true,
      "id": "vtk_mesh",
      "name": "VTK format brain surface mesh flag"
    },
    {
      "command-line-flag": "-r",
      "description": "head radius (mm not voxels); initial surface sphere is set to half of this",
      "value-key": "[HEAD_RADIUS]",
      "type": "Number",
      "optional": true,
      "id": "head_radius",
      "name": "Head Radius"
    },
    {
      "command-line-flag": "-t",
      "description": "Apply thresholding to segmented brain image and mask",
      "value-key": "[THRESHOLDING]",
      "type": "Flag",
      "optional": true,
      "id": "thresholding",
      "name": "Threshold segmented image flag"
    },
    {
      "command-line-flag": "-v",
      "description": "Switch on diagnostic messages",
      "value-key": "[VERBOSE]",
      "type": "Flag",
      "optional": true,
      "id": "verbose",
      "name": "Verbose Flag"
    }
  ],
  "schema-version": "0.5",
  "output-files": [
    {
      "path-template": "[MASKFILE].nii.gz",
      "description": "Main default mask output of BET",
      "optional": true,
      "id": "outfile",
      "name": "Output mask file"
    },
    {
      "path-template": "[MASKFILE]_mask.nii.gz",
      "description": "Binary mask file (from -m option)",
      "optional": true,
      "id": "binary_mask",
      "name": "Output binary mask file"
    },
    {
      "path-template": "[MASKFILE]_overlay.nii.gz",
      "description": "Overlaid brain surface onto original image",
      "optional": true,
      "id": "overlay_file",
      "name": "Surface overlay file"
    },
    {
      "path-template": "[MASKFILE]_skull.nii.gz",
      "description": "Approximate skull image file",
      "optional": true,
      "id": "approx_skull_img",
      "name": "Approximate skull file"
    }
  ]
}