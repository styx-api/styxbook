# Styx on HPC clusters

Styx runners can also be used on High-Performance Computing (HPC) environments. The
default `LocalRunner` can be used if the required software is available. However, in
most cases, software will need to be installed or made available via container. In most
HPC environments, Apptainer (formerly Singularity), is the container system of choice
(in place of Docker). Styx provides an official Apptainer/Singularity runner,
`SingularityRunner`, that can be used in HPC environments.

To use the `SingularityRunner`, the containers must first be downloaded such that
they can be mapped for use. The key to map the container location to is the container
metadata for each wrapped command. Let's take a look at an example:

First, we'll note that `Mrtrix3` has the following container metadata:

```yaml
{
    "container-image": {
        "image": "mrtrix3/mrtrix3:3.0.4",
        "type": "docker"
    }
}
```

We'll also download the container and install package associated with the runner.

```bash
apptainer pull docker://mrtrix3/mrtrix3:3.0.4 /container/directory/mrtrix3_3.0.4.sif

pip install styxsingularity
```

Now to use our runner:

```Python
from styxdefs import set_global_runner
from styxsingularity import SingularityRunner

my_runner = SingularityRunner(
    images={
        "mrtrix3/mrtrix3:3.0.4": "/container/directory/mrtrix3_3.0.4.sif"
    }
)
set_global_runner(my_runner)

# Now you can use Styx functions as usual
```

> [!TIP]
> If you wish to use a different downloaded container, you can map the key to the path of the other container. Note, commands may not be all supported if non-listed container used.

## Local scratch storage

On HPC environments, local scratch storage is often made available on computing
nodes. These often provide superior performance by using a locally-connected SSD instead
of processing over network-attached storage. While not strictly necessary, runners can
benefit by redirecting the temporary output to the local storage and copying the final
outputs to the desired location. Take a look at the
[tips](tips_best_practices.md#managing-runner-output) page for how to manage the
runner output.
