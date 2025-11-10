# Styx on HPC clusters

Styx runners can also be used on High-Performance Computing (HPC) environments. The
default `LocalRunner` can be used if the required software is available. However, in
most cases, software will need to be installed or made available via container. In most
HPC environments, Apptainer (formerly Singularity), is the container system of choice
(in place of Docker). Styx provides an [official Apptainer/Singularity runner](https://github.com/styx-api/styxsingularity),
`SingularityRunner`, that can be used in HPC environments.

## Local scratch storage

On HPC environments, local scratch storage is often made available on computing
nodes. These often provide superior performance by using a locally-connected SSD instead
of processing over network-attached storage. While not strictly necessary, runners can
benefit by redirecting the temporary output to the local storage and copying the final
outputs to the desired location. Take a look at the
[tips](tips_best_practices.md#managing-runner-output) page for how to manage the
runner output.
