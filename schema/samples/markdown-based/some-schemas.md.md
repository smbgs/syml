## Schema 1

```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: markdown-embedded-schema-1
  version: 0.0.1
  
spec:

  storage:
    provider: postgres
    type: table
    database: test-database
    schema: public
    table: sample-source-a

  fields:
    - name: field1
      type: text
    - name: field2
      type: integer

```

## Schema 2

```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: markdown-embedded-schema-2
  version: 0.0.1

spec:

  storage:
    provider: postgres
    type: table
    database: test-database
    schema: public
    table: sample-source-b

  fields: 
    - name: field3
      type: integer

```