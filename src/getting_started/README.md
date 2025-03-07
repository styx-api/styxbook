# Getting started

<!-- > [!NOTE]  
> The examples in this book uses Styx wrappers from the NiWrap package.
> Styx wrappers will work the same way for other (custom) wrappers. -->

To get started install the [NiWrap](https://github.com/styx-api/niwrap/tree/main) Python package. Let's also install the Docker integration so you don't have to worry about installing any software dependencies.

```sh
pip install niwrap styxdocker
```

Running commands is then as easy as calling the method from the appropriate module.
For example, to call FSL `bet`:

```Python
from niwrap import fsl

# # If you want to use Docker:
# import niwrap
# niwrap.use_docker()

bet_output = fsl.bet(
    infile="my_file.nii.gz",
    binary_mask=True,
)
```

This runs the command

```sh
bet my_file.nii.gz -m
```

and stores all available output files for easy access in `bet_output`.

These can then be used as an input to another Styx wrapper or with any other Python package like `nilearn`:

```Python
from nilearn.plotting import plot_anat

plot_anat(bet_output.outfile)
```

> [!TIP]  
> Styx includes detailed documentation about every command, argument, and output file. You should be able to just hover over any of them in your editor to view its documentation.

The next chapter will explain how to use *Runners* to control how the commands get executed and intermediate files get stored.
