# Contributing to the Book

This guide explains how to contribute to the Styx Book documentation. Good documentation is essential for making neuroimaging tools accessible to researchers, so your contributions here are highly valuable.

## Documentation Style Guide

### Friendly and Accessible Tone

The Styx Book aims to be approachable for all users, including those without extensive technical backgrounds. When writing:

- **Use a conversational, friendly tone** - Write as if you're explaining concepts to a colleague
- **Avoid unnecessary jargon** - When technical terms are needed, explain them
- **Consider the audience** - Remember that many readers will be neuroscientists, not software developers
- **Use examples** - Concrete examples help clarify abstract concepts

### Technical Level by Section

Different sections of the book target different technical levels:

- **Getting Started & Examples**: Written for neuroscientists with basic programming knowledge
- **Contributing to NiWrap**: Accessible to researchers with minimal software development experience
- **Advanced Concepts & Styx Compiler**: Can assume more technical background, but still aim for clarity

## Book Structure

The Styx Book is built using [mdBook](https://rust-lang.github.io/mdBook/), a tool for creating online books from Markdown files.

### Repository Structure

```
book/
├── src/
│   ├── SUMMARY.md            # Book structure/table of contents
│   ├── README.md             # Book landing page
│   ├── getting_started/      # Getting started guides
│   ├── contributing/         # Contribution guides
│   ├── examples/             # Example workflows
│   ├── advanced_concepts/    # More technical topics
│   └── boutiques_guide/      # Boutiques reference
├── theme/                    # Custom styling (if applicable)
└── book.toml                 # Configuration file
```

## Making Changes to the Book

### Local Development

1. Install mdBook (if not already installed):
   ```bash
   cargo install mdbook
   # Or use your system's package manager
   ```

   ```bash
   # Optional: Mermaid diagram rendering
   # cargo install mdbook-mermaid
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/styx-api/styxbook.git
   cd styxbook
   ```

3. Serve the book locally to see changes in real-time:
   ```bash
   mdbook serve
   # Open http://localhost:3000 in your browser
   ```

4. Edit Markdown files in the `src/` directory
   - Changes will automatically reload in your browser

### Contributing Changes

1. Create a branch for your changes:
   ```bash
   git checkout -b improve-getting-started
   ```

2. Make your edits to the relevant Markdown files

3. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Improve getting started documentation"
   git push origin improve-getting-started
   ```

4. Open a pull request on GitHub

## Writing Guidelines

### Content Structure

- Use clear headings and subheadings
- Break long sections into digestible chunks
- Include a brief introduction at the beginning of each page
- End complex sections with a summary or key takeaways

### Code Examples

- Always include complete, runnable examples when possible
- Explain what the code does, not just show it
- Use syntax highlighting for code blocks (e.g., ```python)
- Include expected output where helpful

### Images and Diagrams

- Use screenshots or diagrams to illustrate complex concepts
- Ensure images have alt text for accessibility
- Keep diagrams simple and focused on the key point

## Example Improvement

### Less Helpful:
```markdown
## Command Execution
The execute_command function runs commands with appropriate argument handling.
```

### More Helpful:
````markdown
## Running Neuroimaging Tools

When you call a function like `fsl.bet()`, NiWrap handles all the complex command-line arguments for you behind the scenes. 

For example, this simple Python code:

```python
from niwrap import fsl

fsl.bet(infile="T1.nii.gz", outfile="brain.nii.gz", fractional_intensity=0.5)
```

Gets translated into the equivalent command-line call:

```bash
bet T1.nii.gz brain.nii.gz -f 0.5
```

This conversion happens automatically, saving you from remembering the exact command syntax.
````

## Getting Help

If you're unsure about how to document something or have questions about the book structure:

1. Open an issue in the [Styx Book repository](https://github.com/styx-api/styxbook/issues)
2. Ask for guidance in your pull request
3. Look at existing documentation for similar features as a reference

Thank you for helping improve the Styx Book! Your contributions make these tools more accessible to the neuroimaging community.