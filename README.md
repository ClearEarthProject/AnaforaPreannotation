# Anafora Automatic Pre-Annotation

This script creates [Anafora](https://github.com/weitechen/anafora) pre-annotation files, marking any occurences of a string as a given entity type. The strings and corresponding entities are specified using a CSV file. For example:

```
Floating ice,Ice_attachment
Sea ice,Ice_source
Sea-ice,Ice_source
Ice rind,Ice_devel
Ice rinds,Ice_devel
```

The preannotation script gives precedence to longer strings and does not doubly-annotate. It also treats strings as non-case-sensitive.

The script also requires a path to the schema that contains the entity types (needed for "parentType" field in XML), the name used by the schema/mode (which is part of the filename).

preannotation.py usage:
```
  -h, --help              show this help message and exit
  --csv CSV               CSV file of strings to preannotate
  --schema SCHEMA         Path to Anafora schema XML
  --name NAME             Schema name used in the filenames
  --directory DIRECTORY   Anafora directory to create preannotation files for
```

This repository also contains the latest versions of the CSV files used for the ClearEarth project's pre-annotation.
