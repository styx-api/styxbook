# Tips & best practices

## Managing runner output

You may only want to keep certain outputs generated from your workflow. One strategy is to set the runner's output directory to temporary storage, copying only what should be saved to a more permanent location.

```Python
import shutil
from styxdefs import set_global_runner, LocalRunner

my_runner = LocalRunner()
my_runner.data_dir = "/some/temp/folder"
set_global_runner(my_runner)

# Perform some task
# ...

shutil.copy2(task_output.out_files, "/some/permanent/output/folder")

# Remove temporary directory for cleanup
shutil.rmtree(runner.data_dir) 
```

## Workflow logging

All official runners have a logger available. To avoid having to setup a new (custom)
logger, the runner's logger can be used.

```Python
import logging

from styxdefs import set_global_runner, LocalRunner

my_runner = LocalRunner()
set_global_runner(my_runner)

# Get and use the logger
logger = logging.getLogger(my_runner.logger_name)
```

## Environment variables in runners

Environment variables can be passed onto the runners. These can be passed to via
the `environ` attribute as a dictionary.

```Python
my_runner.environ = {"VARIABLE": str(variable_value)}
```
