# I/O: Runner File Handling

When you're using Styx wrapper functions with the default runners, you won't have to worry too much about I/O since a lot of it gets handled automatically for you.

## Basic File Access

Take this example:

```python
outputs = fsl.bet(infile="brain.nii", fractional_intensity=0.5)

outputs.mask_file  # File path to an individual output
```

The `outputs` object gives you structured access to generated files through properties that support autocompletion and include helpful documentation.

## Dynamic File Access

Sometimes though, either when a descriptor hasn't been fully implemented or if the output structure is more complex, there may not be an output property available. For these cases, you can use the `outputs.root` property, which always points to the output directory:

```python
outputs.root / "my_special_file.ext"

# Dynamic file access
for number in [1, 2, 3]:
    f = outputs.root / f"my_file_with_a_{number}.ext"
```

## Default Runner Behavior

While custom Styx runners let you implement file I/O handling however you want, the default runners (`LocalRunner`, `DockerRunner`, and `SingularityRunner`) all work pretty similarly by default. They create a working directory (defaults to `styx_temp/` in your current working directory) with individual folders for each Styx function call you make.

### Directory Structure

```
79474bd248c4b2f1_5_bet/
^^^^^^^^^^^^^^^^ ^ ^^^
|                | |
|                | `-- Interface name (FSL BET)
|                `---- Execution number (5th call)
`--------------------- Unique session hash
```

**Components:**
- **Session hash**: A unique random identifier generated per runner instance, preventing conflicts between pipeline executions
- **Execution number**: Sequential counter for chronological ordering of function calls
- **Interface name**: Human-readable identifier for the Styx function

This naming convention ensures unique, sortable, and identifiable output directories.

> [!WARNING]
> You can clean up outputs using `shutil.rmtree(outputs.root)` for individual function outputs, or `shutil.rmtree(get_global_runner().data_dir)` to remove all outputs from the current session. **Be careful** - make sure you're not deleting any important data this way!

> [!NOTE]
> For advanced runner configuration and custom I/O behavior, see [Subcommands](./runners.md) and [Writing Custom Runners](../advanced_concepts/custom_runners.md).