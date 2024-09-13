# Runners

_Runners_ define how commands will be executed and how output files will be stored.

By default they will be executed with the system shell and outputs will be stored in a folder named `styx_temp/` in the current working directory.

While this might be good for debugging, other users might want to control where data gets stored and might not have all the software packages installed so the first step before packaging and deploying a pipeline will be to modify this behaviour.

## Official Runners

There are a of number official runners:

- `styxdefs.LocalRunner` - This is the default Runner. It executes commands locally.
- `styxdefs.DummyRunner` - ?
- [`styxdocker.DockerRunner`](https://github.com/childmindresearch/styxdocker) - This Runner executes every command in a Docker container.
- [`styxsingularity.SingularityRunner`](https://github.com/childmindresearch/styxsingularity) - This Runner executes every command in an Apptainer/Singularity container.
- [`styxgraph.GraphRunner`](https://github.com/childmindresearch/styxgraph) - This is a special Runner - it captures information about how your commands are connected and returns a diagram.

## Setting up a Runner

If you for example want to change where the LocalRunner stores data, we create a new instance of it and set it to be used globally:

```Python
from styxdefs import set_global_runner, LocalRunner

set_global_runner(LocalRunner(
    data_dir="some/folder/",
))

# Now you can use any Styx functions as usual
```

The same way we can set up any other Runner:

```Python
from styxdefs import set_global_runner
from styxdocker import DockerRunner

set_global_runner(DockerRunner())

# Now you can use any Styx functions as usual
```

> [!IMPORTANT]  
> Look at the individual Runners documentation to learn more about how they can be configured.

> [!TIP]  
> For most users, configuring the global Runner once at the beginning of their script should be all they ever need.

Alternatively, if, for some reason, we want one specific function to be executed with a different Runner and not modify the global one, we just pass it as an argument:

```Python
my_special_runner = DockerRunner()

fsl.bet(
    infile="my_file.nii.gz",
    runner=my_special_runner,
)

# Now you can use any Styx functions as usual
```

## Middleware Runners

Middleware Runners are special runners that can be used on top of other runners. So far there is one official runner, the GraphRunner, which captures how commands are connected to create a diagram:

```Python
from styxdefs import set_global_runner, get_global_runner
from styxgraph import GraphRunner

set_global_runner(DockerRunner())  # (Optional) Use any Styx runner like usual
set_global_runner(GraphRunner(get_global_runner()))  # Use GraphRunner middleware

# Use any Styx functions as usual
# ...

print(get_global_runner().mermaid())  # Print mermaid diagram
```