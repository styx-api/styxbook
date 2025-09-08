# Example: Podman runner

[Podman](https://podman.io/) is an open-source container engine, similar to Docker for managing and running containers. Unlike Docker, Podman is **daemonless**, meaning it runs containers as child processes without the need for a persistent background service. It supports rootless containers for enhanced security and is largely compatible with Docker’s CLI commands. Given this, we can repurpose the `DockerRunner` for use with Podman.

```Python
{{#include pysrc/podman.py}}
```
[Full source.](pysrc/podman.py)

> [!NOTE]
> By default, Podman runs as the current user (i.e. rootless) - if root is necessary, the user id parameter can also be passed to the runner with `docker_user_id=0`