# Getting started

> [!NOTE]  
> This book uses Styx wrappers from the NiWrap package, but any Styx wrapper will work the same way.

To get started install the [NiWrap](https://github.com/childmindresearch/niwrap/tree/main) Python package. Let's also install the Docker integration (this way you dont need to worry about manually installing any Neuroscience packages):

```sh
pip install niwrap styxdocker
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

> [!NOTE]
> *But wait! I dont have that software installed!* - No need to worry: We can set up the Docker integration with just a few lines of code at the top of your script:
> 
> ```Python
> from styxdefs import set_global_runner
> from styxdocker import DockerRunner
> 
> set_global_runner(DockerRunner())
> ```
> 
> What exactly this does will be explained in more detail in the next section of this book. For now this just lets docker handle providing the software package. You will notice that the first execution will be very slow because it needs to download the Docker image.

These can then be used as an input to another Styx wrapper or with any other Python package like Nilearn:

```Python
from nilearn.plotting import plot_anat

plot_anat(bet_output.outfile)
```

> [!TIP]  
> Styx includes detailed documentation about every command, argument, and output file. You should be able to just hover over any of them in your editor to view its documentation.

The next chapter will explain how to use _Runners_ to control how the commands get executed and intermediate files get stored. 