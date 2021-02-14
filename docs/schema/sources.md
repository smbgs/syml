# Sources

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