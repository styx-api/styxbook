# Writing Custom Runners

While the official runners cover most common use cases, you might need to create your own custom runner for specific requirements - like running commands on a remote cluster, implementing custom logging, or handling specialized file systems.

## Understanding the Runner Protocol

Custom runners need to implement two main protocols: `Runner` and `Execution`. Think of the `Runner` as a factory that creates `Execution` objects, and each `Execution` handles a single command run.

### The Runner Protocol

Your runner class needs to implement just one method:

```python
def start_execution(self, metadata: Metadata) -> Execution:
    """Start an execution for a specific tool.
    
    Args:
        metadata: Information about the tool being executed (name, package, etc.)
        
    Returns:
        An Execution object that will handle the actual command execution
    """
```

### The Execution Protocol

The `Execution` object does the heavy lifting with four key methods:

```python
def input_file(self, host_file: InputPathType, resolve_parent: bool = False, mutable: bool = False) -> str:
    """Handle input files - return where the command should find them"""

def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
    """Handle output files - return where they'll be stored on the host"""

def params(self, params: dict) -> dict:
    """Process or modify command parameters if needed"""

def run(self, cargs: list[str], handle_stdout=None, handle_stderr=None) -> None:
    """Actually execute the command"""
```

## Example: Simple Custom Runner

Let's build a custom runner that adds some logging and stores outputs in timestamped directories:

```python
import pathlib
import subprocess
import logging
from datetime import datetime
from styxdefs import Runner, Execution, Metadata, InputPathType, OutputPathType

class TimestampedExecution(Execution):
    def __init__(self, output_dir: pathlib.Path, metadata: Metadata):
        self.output_dir = output_dir
        self.metadata = metadata
        self.logger = logging.getLogger(f"custom_runner.{metadata.name}")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def input_file(self, host_file: InputPathType, resolve_parent: bool = False, mutable: bool = False) -> str:
        # For simplicity, just return the absolute path
        return str(pathlib.Path(host_file).absolute())

    def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
        return self.output_dir / local_file

    def params(self, params: dict) -> dict:
        # Log parameters for debugging
        self.logger.info(f"Running {self.metadata.name} with params: {params}")
        return params

    def run(self, cargs: list[str], handle_stdout=None, handle_stderr=None) -> None:
        self.logger.info(f"Executing: {' '.join(cargs)}")
        
        # Run the command
        result = subprocess.run(
            cargs,
            cwd=self.output_dir,
            capture_output=True,
            text=True
        )
        
        # Handle output
        if handle_stdout and result.stdout:
            for line in result.stdout.splitlines():
                handle_stdout(line)
        if handle_stderr and result.stderr:
            for line in result.stderr.splitlines():
                handle_stderr(line)
                
        if result.returncode != 0:
            raise RuntimeError(f"Command failed with return code {result.returncode}")

class TimestampedRunner(Runner):
    def __init__(self, base_dir: str = "custom_outputs"):
        self.base_dir = pathlib.Path(base_dir)
        self.execution_counter = 0

    def start_execution(self, metadata: Metadata) -> Execution:
        # Create timestamped directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.base_dir / f"{timestamp}_{self.execution_counter}_{metadata.name}"
        self.execution_counter += 1
        
        return TimestampedExecution(output_dir, metadata)

# Usage
from styxdefs import set_global_runner

custom_runner = TimestampedRunner(base_dir="my_custom_outputs")
set_global_runner(custom_runner)
```

## Learning from Official Runners

The best way to understand custom runners is to look at how the official ones work:

### LocalRunner Pattern
The `LocalRunner` is the simplest - it just runs commands directly on the host system. Notice how it:
- Creates unique output directories using a hash and counter
- Uses `subprocess.Popen` with threading for real-time output handling
- Handles file paths by converting them to absolute paths

### DockerRunner Pattern
The `DockerRunner` shows more complex file handling:
- Maps host files to container paths using Docker mounts
- Creates a run script inside the container
- Handles the complexity of translating between host and container file systems

## Advanced Patterns

### Middleware Runners
You can create runners that wrap other runners to add functionality:

```python
class LoggingRunner(Runner):
    def __init__(self, wrapped_runner: Runner):
        self.wrapped_runner = wrapped_runner
        self.logger = logging.getLogger("logging_runner")

    def start_execution(self, metadata: Metadata) -> Execution:
        self.logger.info(f"Starting execution of {metadata.name}")
        execution = self.wrapped_runner.start_execution(metadata)
        return LoggingExecution(execution, self.logger)

class LoggingExecution(Execution):
    def __init__(self, wrapped_execution: Execution, logger):
        self.wrapped = wrapped_execution
        self.logger = logger

    def run(self, cargs: list[str], handle_stdout=None, handle_stderr=None) -> None:
        self.logger.info(f"Running command: {' '.join(cargs)}")
        start_time = datetime.now()
        
        try:
            self.wrapped.run(cargs, handle_stdout, handle_stderr)
            duration = datetime.now() - start_time
            self.logger.info(f"Command completed in {duration}")
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            raise

    # Forward other methods to wrapped execution
    def input_file(self, *args, **kwargs): return self.wrapped.input_file(*args, **kwargs)
    def output_file(self, *args, **kwargs): return self.wrapped.output_file(*args, **kwargs)
    def params(self, *args, **kwargs): return self.wrapped.params(*args, **kwargs)
```

### Remote Execution
For cluster or remote execution, you might implement SSH-based runners, SLURM job submission, or cloud-based execution.

## Tips for Custom Runners

**File Handling**: Think carefully about where files live and how paths get translated. Input files need to be accessible to your execution environment, and output files need to end up where the user expects them.

**Error Handling**: Always check return codes and provide meaningful error messages. Consider implementing custom exception types like `StyxDockerError` for better debugging.

**Logging**: Good logging makes debugging much easier. Use structured logging with appropriate levels.

**Threading**: If you need real-time output handling (like showing progress), consider using threading like the official runners do.

**Testing**: Test your runner with various tools and edge cases. The `DryRunner` pattern is useful for testing command generation without actual execution.

> [!TIP]
> Start simple! Create a basic working runner first, then add advanced features like custom file handling or remote execution once you have the basics working.

> [!TIP]
> Look at the source code of official runners for inspiration. They handle many edge cases you might not think of initially.