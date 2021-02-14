# Fields

## Overview

- `name` - Field name 
- `type` - Field type (depends on the provider).  special `GROUP` type can be used to logically group some fields in  the schema without affecting the naming schema in the destination.
- `validator` [optional] - Field validator
- `source` - Links the field in the current schema to a field in the 
  "source" schema.
- `common` - when defined in the parent field contents will be 
  inherited by all nested fields (in the `fields`) 
- `fields` - list of nested fields 
- `analytics` - allows to tweak analytics engine 
- `dimension` - used to specify SCD type 

## Details

### Nested fields and "common"
Depending on the "Destination" nested fields may be handled a bit
differently. 

#### Field  groups
Fields with the special  `GROUP` type will be excluded from nested naming completely, effectively pulling the nested fields to the same level as `GROUP` field.

For example in the common relational databases table
fields can not be nested, therefore a specific naming conversion 
approach is used - field names from multiple levels are combined 
into a single plain name, like `name__nested_name__lvl3_name`. 

Note that specific delimiter, and the approach as a whole can be
customized by defining the `nestedDelimiter` field in the
Destination `spec`. 

On the other hand, some databases support JSONB or OBJECT types will be nested naturally.

###  Dimension types
#TODO: describe in more details
 - type 0 - retain
 - type 1 - overwrite
 - type 2 - new-row
 - type 3 - new-attribute
 - type 4 - history-table
 - type 5 - history-embedding
 - type 6 - combined
