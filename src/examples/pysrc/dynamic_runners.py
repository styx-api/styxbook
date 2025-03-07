from styxdefs import set_global_runner, LocalRunner
from styxdocker import DockerRunner
from styxsingularity import SingularityRunner

runner_type = "docker"  # You could read this from a CLI argument,
                        # config file, or check what system you are
                        # running on.

if runner_type == "docker":
    print("Using docker runner.")
    runner = DockerRunner()

elif runner_type == "singularity":
    print("Using singularity runner.")
    runner = SingularityRunner()

else:
    print("Using local runner.")
    runner = LocalRunner()

set_global_runner(runner)
