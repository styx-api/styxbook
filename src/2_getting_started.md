# Getting started

> [!NOTE]  
> This book uses Styx wrappers from the NiWrap package, but any Styx wrapper will work the same way.

To get started install the [NiWrap](https://github.com/childmindresearch/niwrap/tree/main) Python package:

```sh
pip install niwrap
```

From there on running commands will be as easy as:

```Python
from niwrap import fsl

bet_output = fsl.bet(
    infile="my_file.nii.gz",
    binary_mask=True,
)
```

This runs the command

```sh
bet my_file.nii.gz -m
```

and stores all the output files for easy access in `bet_output`.

These can then be used as an input to another Styx wrapper or with any other Python package like nilearn:

```Python
from nilearn.plotting import plot_anat

plot_anat(bet_output.outfile)
```

> [!TIP]  
> Styx includes detailed documentation about every command, argument, and output file. You should be able to just hover over any of them in your editor to view its documentation.

The next chapter will explain how to use _Runners_ to control how the commands get executed and intermediate files get stored. 