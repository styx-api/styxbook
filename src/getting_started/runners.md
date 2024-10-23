# Runners

_Runners_ define how commands will be executed and how output files will be stored.

By default they will be executed with the system shell and outputs will be stored in a folder named `styx_temp/` in the current working directory.

While this provides a good start, users may want more control where the data gets store or might not have all the software dependencies installed.
The first step before packaging and deploying a pipeline should be to modify this behavior.

## Official Runners

There are a of number official runners:

- `styxdefs.LocalRunner` - This is the default Runner. It executes commands locally using the system shell.
- `styxdefs.DryRunner` - This Runner dry-runs commands, useful when writing new wrappers to ensure commands are as expected.
- [`styxdocker.DockerRunner`](https://github.com/childmindresearch/styxdocker) - This Runner executes commands in a Docker container.
- [`styxsingularity.SingularityRunner`](https://github.com/childmindresearch/styxsingularity) - This Runner executes commands in an Apptainer/Singularity container.
- [`styxgraph.GraphRunner`](https://github.com/childmindresearch/styxgraph) - This is a special Runner, capturing information about how commands are connected, returning a diagram.

## Setting up a Runner

If you for example want to change where the LocalRunner stores data, we create a new instance of it and set it to be used globally:

```Python
from styxdefs import set_global_runner, LocalRunner

my_runner = LocalRunner()
my_runner.data_dir = "/some/folder"
set_global_runner(my_runner)

# Now you can use any Styx functions as usual
```

The same method can be used to set up other Runners:

```Python
from styxdefs import set_global_runner
from styxdocker import DockerRunner

my_runner = DockerRunner()
set_global_runner(my_runner)

# Now you can use any Styx functions as usual
```

> [!IMPORTANT]  
> Look at the individual Runners documentation to learn more about how they can be configured.

> [!TIP]  
> For most users, configuring the global Runner once at the beginning of their script should be all they ever need.

Alternatively, if a specific function should be executed with a different Runner without modifying the global Runner, we can pass it as an argument to the wrapped command:

```Python
my_other_runner = DockerRunner()

fsl.bet(
    infile="my_file.nii.gz",
    runner=my_other_runner,
)

# Now you can use any Styx functions as usual
```

## Middleware Runners

Middleware Runners are special runners that can be used on top of other runners. Currently, the GraphRunner, which creates a diagram by capturing how commands are connected, is the only official runner:

```Python
from styxdefs import set_global_runner, get_global_runner
from styxgraph import GraphRunner

my_runner = DockerRunner()
set_global_runner(GraphRunner(my_runner))  # Use GraphRunner middleware

# Use any Styx functions as usual
# ...

print(get_global_runner().mermaid())  # Print mermaid diagram
```
