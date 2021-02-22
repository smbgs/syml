# SYML

Syml (schema yml) is a yaml-based format similar and compatible to
k8s CRD's and used to define data schemas with relations,
tracing, migrations with rich versioning.


## Toolchain

### [Definitions & Documentation](./docs/schema/README.md)

Syml also can be embedded in Markdown, and the Syml toolchain
should support both yaml and markdown based Syml definitions.

### Core Libraries

This repository also includes the simple python-based tooling capable
of managing Syml and markdown files with Syml embeddings. 

This tooling contains python core libraries capable of
representing the YAML and Markdown files as SYML object model.

#### Dependencies

Schema validation:

- https://pypi.org/project/yamale/ - (currently used, has limitations that we already can feel, possibly needs prs?)
- https://pypi.org/project/yschema/ - (strong yamale alternative, but seems abandoned, possibly needs support)
- https://pypi.org/project/jsonschema/ - (lots of tooling, but quite verbose, yaml based schemas are not well supported)


Core libraries for other languages may be developed at some point.

## SYML Engine

Integrates Core SYML libraries into a higher level toolkit capable
of specific actions provided by the SYML engine modules.

### YML parser

YML Parser module is capable of reading the yml files from the
file-system or external URI (with necessary caching), includes
resolution and representing them as consolidated and
complete object model.

### YML serializer

YML Serializer module is capable of writing the yml files from
SYML object model (as separate files or directories with files).

### Markdown parser

Markdown Parser module is capable of reading the markdown files,
extracting SYML yaml definitions from them and with the help of
the YML Parser module representing them as consolidated and
complete object model.

### SQL Reverse Engineer

SQL Reverse Engineer module is capable of connecting to the 
compatible SQL databases and creating SYML object model entities
from the database entities.

#### Dependencies

Existing database (common SQL engines)

- https://docs.sqlalchemy.org/en/14/core/reflection.html (core principle)
- https://github.com/agronholm/sqlacodegen (implementation that generates sqlalchemy python tables, code can be a good stating poing)

DDL in files (common SQL engines)

- No candidates so far
- Potentially can be implemented by creating embedded postgres database, applying DDL, and then using above tools


### SQL Forward Engineer

SQL Forward Engineer module is capable of connecting to the
compatible SQL databases and managing (creating AND updating)
the database entities based on the SYML object model.

#### Dependencies

- sqlalchemy based, but fully custom made

### Data Analyzer

Data analyzer module is capable of connecting to the compatible databases and
retreiving the analytical data from entities (amount of rows in a table, distinct colum values, value histogramms etc.)

### K8S database manager
TBD

### HTML documentation generator
TBD

### OpenAPI bridge
TBD

### DBT bridge
TBD

## SYML Command Line Interface

Set of command line utilities based on the SYML core libraries
and SYML Engine for manual or automated management of SYML
definitions. CLI can be extended by providing additional 
SYML Engine modules.
