# Automated descriptor creation in NiWrap

<picture>
  <source srcset="./descriptor_extraction_dark.svg" media="(prefers-color-scheme: dark)" />
  <source srcset="./descriptor_extraction_light.svg" media="(prefers-color-scheme: light)" />
  <img src="./descriptor_extraction_light.svg" alt="MDN" />
</picture>

Some packages use shared internal data structures which store command line parsing information. By serializing these data structures, we can extract it and subsequently generate Boutiques descriptors from it which will always be correct and can be automatically updated whenever the packages change.

The rough steps to extract metadata are as follows:

1. Add JSON serialization code to the package.
2. Instead of emitting a help message, emit a JSON object.
3. Write a script to run all the commands and extract the JSON objects.
4. Write a script to generate Boutiques descriptors from the JSON objects.

Packages where this is viable:

- Connectome Workbench
- MRTrix3
