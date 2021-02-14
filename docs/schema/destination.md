# Destination
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