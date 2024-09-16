# I/O: Runner file handling

TODO:
- Explain output tuple, root attribute, and maybe strategies on how to clean up.

## _Default_ runner behaviour

While custom Styx runners in allows users to implement file I/O handling any way they want, the 'default' runners (`LocalRunner` as well as `DockerRunner` and `SingularityRunner`) work very similarly by default.

They create a directory (default path `styx_temp/` in the current working directory) in which a folder gets created for every Styx function call. These will look like this:

```
79474bd248c4b2f1_5_bet/
^^^^^^^^^^^^^^^^ ^ ^^^
|                | |
|                | `-- interface name (FSL BET)
|                `---- number of execution (5th)
`--------------------- unique random hash
```

Every time you create a new runner a new random hash will be generated. This ensures there will be no paths created which conflict with previous executions of your pipeline. The hash is followed by a counting number which chronologically will count up by one for every Styx function call. This makes the folder sortable. Lastly they contain the Styx function name to be humanly readable. 