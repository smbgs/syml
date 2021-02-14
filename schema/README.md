# SYML

## Schema

SYML Schema is a primary SYML entity that generally defines the list
of fields (that can also be grouped into hierarchies) and additional
metadata that links one schema to another.

### Sources

Sources describe where the data is coming from.

Declared in the `source` as a single object, or a
list field.

The field is optional, but quite useful in ETL/ELT workflows
when you want to define and document where the data is coming from.
By using another versioned SYML schema you can create the contract
for both data source and data receiver with explicit field types 
and versioning.

See "Fields" and "Storage" descriptions for more 
information.

#### Spec fields

- `name` [optional] - name for the source that can be used in
  schema field definitions with `@` prefix in the `source` field.

- `syml` [optional] - URI to another SYML schema that can be
  used as a whole source definition (supports yaml and 
  markdown files).
  
- `include` [optional, only] - allows to include the external source
  definitions from "Include" section. Basically replaces the 
  whole source definition with the source or list of sources.
  
  Example: @included-schema/source/*

### Include

Include section can be used to add additional SYML schemas from
external files. This is a common mechanism of re-using some common
definitions for parts of the definitions.

#### Spec fields

- `syml` [optional] - URI to another SYML schema that can be
  used as a whole source definition (supports yaml and
  markdown files).

### Destination

Destination (declared in the `dest` field as a single object)
describes where the data is stored.

#### Spec fields

- `kind` - Destination kind i.e. (database, api)
- `provider` - Destination provider i.e. (snowflake, postgres, rest)
- `type` - Destination type i.e. (table, view, response, params)
- `spec` - Destination on the `kind`, `provider` and `type`
  
Database kind spec specifics:

- `database`
- `schema`
- `table`  
- `nestedDelimiter` - `__` (default) 

### Fields

Each field can have type metadata - depending on the storage this
metadata can be defined a bit differently, but the general idea
should support common database types and constraints.

Moreover, fields can have more high-level validators, similar 
to OpenAPI schemas.

#### Spec fields

- `name` - Field name 
- `type` - Field type (depends on the provider)
- `validator` [optional] - Field validator
- `source` - Links the field in the current schema to a field in the 
  "source" schema.
- `common` - when defined in the parent field contents will be 
  inherited by all nested fields (in the `fields`) 
- `fields` - list of nested fields 

Depending on the "Destination" nested fields may be handled a bit
differently. For example in the common relational databases table
fields can not be nested, therefore a specific naming conversion 
approach is used - field names from multiple levels are combined 
into a single plain name, like `name__nested_name__lvl3_name`. 

Note that specific delimiter, and the approach as a whole can be
customized by defining the `nestedDelimiter` field in the
Destination `spec`. 