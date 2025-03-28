# The Styx Book

Welcome to the Styx ecosystem - where command-line tools become type-safe programming interfaces.

## What is Styx?

Styx is a compiler that transforms structured tool descriptions into type-safe language bindings for Python, TypeScript, and R. While originally developed for neuroimaging research, Styx works with any command-line tool that can be described in a structured format.

At its core, Styx allows you to:

- **Write once, use anywhere** - Define tool interfaces once, use them in multiple languages
- **Catch errors early** - Leverage type checking to prevent runtime errors
- **Focus on your work** - Forget complex command-line arguments and focus on your actual research

## Quick Overview

The Styx ecosystem consists of:

- **Styx Compiler** - Generates language bindings from structured tool descriptions
- **NiWrap** - A collection of tool descriptions for popular neuroimaging software
- **Boutiques** - The current frontend format for describing tools

> [!NOTE]  
> Found a bug in a NiWrap interface? Report it at the [NiWrap issue tracker](https://github.com/styx-api/niwrap/issues).
>
> Interested in Styx compiler development? Visit the [Styx compiler repository](https://github.com/styx-api/styx).

## Getting Started

New to Styx? Head to the [Getting Started](./getting_started/README.md) section to learn the basics.

Already familiar and want to do more? Check out:

- [Examples](./examples/README.md) for real-world usage patterns
- [Advanced Concepts](./advanced_concepts/README.md) for custom deployment options
- [Contributing](./contributing/README.md) to help improve the ecosystem

## When to Use Styx

Styx is particularly valuable when:

- You're building reproducible research workflows
- You're developing tools that should be accessible across programming languages
- You want to provide consistent interfaces to complex command-line tools
- You need type safety when working with command-line utilities

## Citation

If Styx helps your research, please cite:

```
@software{styx,
  author = {The Styx Contributors},
  title = {Styx: Type-safe command-line tool bindings},
  url = {https://github.com/styx-api/styx},
  year = {2023}
}
```