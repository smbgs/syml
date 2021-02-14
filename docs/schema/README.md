# SYML

## Schema

SYML Schema is a primary SYML entity that generally defines the list
of fields (that can also be grouped into hierarchies) and additional
metadata that links one schema to another.

### [Sources](sources.md)

Sources describe where the data is coming from.

Declared in the `source` as a single object, or a
list field.

The field is optional, but quite useful in ETL/ELT workflows
when you want to define and document where the data is coming from.
By using another versioned SYML schema you can create the contract
for both data source and data receiver with explicit field types 
and versioning.

See "Fields" and "Destination" descriptions for more 
information.

### [Include](include.md)

Include section can be used to add additional SYML schemas from
external files. This is a common mechanism of re-using some common
definitions for parts of the definitions.

### [Destination](destination.md)

Destination (declared in the `dest` field as a single object)
describes where the data is stored.

### [Fields](fields.md)

Each field can have type metadata - depending on the storage this
metadata can be defined a bit differently, but the general idea
should support common database types and constraints.

Moreover, fields can have more high-level validators, similar 
to OpenAPI schemas.

### Examples

- [TPC-H Snowflake](../samples/tpc-h/README.md)  contains a simple but relatevely complete example of the SYML schema definition in the markdown files.
