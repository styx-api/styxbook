# Contributing to the Styx Compiler

The Styx compiler is the core technology that transforms Boutiques descriptors into type-safe language bindings. This guide provides a basic overview of the compiler architecture and how to contribute to its development.

## Repository Structure

The Styx compiler is organized into several key components:

```
styx/
├── src/
│   └── styx/
│       ├── frontend/       # Parses input formats into IR
│       │   └── boutiques/  # Boutiques-specific frontend
│       ├── ir/             # Intermediate Representation
│       └── backend/        # Code generation for target languages
│           ├── generic/    # Language-agnostic utilities
│           ├── python/     # Python-specific code generation
│           ├── typescript/ # TypeScript-specific code generation
│           └── r/          # R-specific code generation
├── tests/                  # Unit and integration tests
└── docs/                   # Documentation
```

## Compiler Architecture

The Styx compiler follows a traditional compiler design with three main phases:

1. **Frontend**: Parses input formats (e.g., Boutiques descriptors) into an Intermediate Representation (IR)
2. **IR**: A language-agnostic representation of the tool interface
3. **Backend**: Generates code for target languages (Python, TypeScript, R) from the IR

## Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/styx-api/styx.git
cd styx

# Install development dependencies using uv
uv pip install -e .

# Run tests
python -m pytest tests/
```

## Common Contribution Areas

### Adding Features to Existing Language Backends

If you want to improve code generation for a specific language:

1. Locate the language provider in `src/styx/backend/<language>/languageprovider.py`
2. Make your changes to the code generation logic
3. Add tests in the `tests/` directory
4. Run the test suite to ensure everything works as expected

### Adding Support for a New Language

To add support for a new target language:

1. Create a new directory in `src/styx/backend/` for your language
2. Implement a language provider that conforms to the interface in `backend/generic/languageprovider.py`
3. Add language-specific code generation logic
4. Add tests for your new language backend

### Improving the IR

If you want to enhance the Intermediate Representation:

1. Make changes to the IR structure in `src/styx/ir/core.py`
2. Update the normalization and optimization passes if necessary
3. Ensure all language backends can handle your IR changes
4. Add tests for your IR modifications

## Testing Your Changes

The Styx compiler has a comprehensive test suite:

```bash
# Run all tests
python -m pytest

# Run specific test files
python -m pytest tests/test_output_files.py

# Run with verbose output
python -m pytest -v
```

## Documentation

Styx uses [pdoc](https://pdoc.dev/) for API documentation:

```bash
# Install pdoc if needed
pip install pdoc

# Generate documentation
pdoc --html --output-dir docs/api src/styx
```

## Getting Help

The Styx compiler is a complex piece of software. If you're having trouble:

1. Check existing [issues on GitHub](https://github.com/styx-api/styx/issues)
2. Look at the test cases to understand how different components work
3. Reach out to the maintainers through GitHub issues

## Next Steps

While contributing to the Styx compiler requires more technical expertise than contributing to NiWrap descriptors, it's a rewarding way to improve the entire ecosystem. Start with small changes and work your way up to more complex features.

For most users interested in neuroimaging tools, [contributing to NiWrap](./niwrap.md) might be a more accessible starting point.