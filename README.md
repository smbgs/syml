# SYML

Syml (schema yml) is a yaml-based format similar and compatible to
k8s CRD's and used to define data schemas with relations,
tracing, migrations with rich versioning.


## Toolchain

### [Definitions & Documentation](./docs/schema/README.md)

Syml also can be embedded in Markdown, and the Syml toolchain
should support both yaml and markdown based Syml definitions.

### Core

This repository also includes the simple python-based tooling capable
of managing Syml and markdown files with Syml embeddings. 

This tooling contains python core libraries capable of
representing the YAML and Markdown files as SYML object model.

Core libraries for other languages may be developed at some point.

### Command Line Interface

Integrates Core SYML libraries into a higher level toolkit capable
of specific actions provided by the SYML engine modules.

Set of command line utilities based on the SYML core libraries
and SYML Engine for manual or automated management of SYML
definitions. CLI can be extended by providing additional 
SYML Engine modules.

----

### Initial release completeness

- [ ] Core Framework
- [ ] Command Line Interface
- [ ] Profiles  
- [ ] Schemas
- [ ] Database Tools  
    - [ ] Reverser
    - [ ] Pulse
    - [ ] Analytics
    - [ ] Seeder
- [ ] K8s
- [ ] DevOps

----

### Short-term todo:

- Core Framework
    - [x] Reduce boilerplate for CLI clients


- Schemas
    - [x] Implement the prototype for syml core / monitor to work with schemas
    - [ ] Implement simple CLI schema visualizer (outline core schema parts)
    - [x] Create openapi schema for SYMLSchema
    - [ ] Monitoring
        - [x] Implement validation API for SYMLSchema
        - [x] Extend the CLI to support schema validation
        - [ ] Extend the core service framework to support monitoring
        - [ ] Extend the CLI to support monitoring (start moving towards interactive shell)


- DevOps
    - [x] Figure out how to debug syml services in IDE
    - [x] Figure out how to test services
    - [ ] Improve pipenv things (slow cmd)


- Database Tools
    - DB Reverser
        - [ ] Update the output to be in SYML schema format (as an option?)
    - DB Seeder
        - [ ] Implement the initial POC that can consume SYML schema and update the database
	
