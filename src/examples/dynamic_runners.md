# Example: Dynamic runners

A common pattern in processing pipelines with Styx is dynamically choosing what runner Styx should use. This allows the same pipeline to run e.g. both on your local machine for testing as well as on your HPC cluster. 

```Python
{{#include pysrc/dynamic_runners.py:5:}}
```
[Full source.](pysrc/dynamic_runners.py)