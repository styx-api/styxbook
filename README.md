# The Styx Book

The official documentation for the Styx ecosystem - a system for generating type-safe neuroimaging tool bindings.

## About This Book

This repository contains the source for [The Styx Book](https://styx-api.github.io/styxbook/), which is built using [mdBook](https://rust-lang.github.io/mdBook/).

The documentation covers:
- How to use the Styx compiler and NiWrap
- Advanced concepts and implementation details
- Contribution guidelines
- Example workflows
- Boutiques descriptor reference

## Building the Book

To build the book locally:

1. Install mdBook:
   ```bash
   cargo install mdbook
   # Optional: Install the mermaid plugin if needed
   cargo install mdbook-mermaid
   ```

2. Build the book:
   ```bash
   mdbook build
   ```

3. Or serve it locally with live reloading:
   ```bash
   mdbook serve
   # Then open http://localhost:3000 in your browser
   ```

## Contributing

Contributions to improve the documentation are welcome! Please see our [contributing guide](./src/contributing/book.md) for details on how to help.

## License

This documentation is licensed under the [MIT License](LICENSE).