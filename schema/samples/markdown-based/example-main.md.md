# Markdown SYML embedding

This is an example of markdown-based embedding for syml definitions, allowing you to use markdown as a core  documentation, but at the same time embed semantically connected definitions.

## Sample schema describing the Snowflake database table

This table is derived from multiple Postgres tables, and the mapping is defined inline. Note that SYML does not force you to define the specific mapping, and you can just use human-readable text to descrive the mapping process. 

At the same time, SYML also allows for custom tooling layer to interpret the mapping definition if the specific structure is defined. 

```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: sample-syml-schema
spec:

  storage:
    provider: snowflake
    type: table
    database: DEMO_DB
    schema: PUBLIC
    table: SAMPLE_DEST
	
  sources:
  
    - name: sample-source_a
	  syml: ./some-schemas.md/schema/markdown-embedded-schema-1

    - name: sample-source_b
	  syml: ./some-schemas.md/schema/markdown-embedded-schema-2


  fields:
  	- name: dimensional
	  common:
		source: @sample-source_a
	    
	  fields:
	    - name: derived_field1
		  type: TEXT
		  source:
		  	field: field1
		  
	    - name: derived_field2
		  type: NUMBER
		  source:
		    field: field2

	    - name: derived_field3
		  type: NUMBER
		  source:
			source: @sample-source_b		  
		    field: field3			
```

### Description

The desciption can also be provided in markdown format. 
If no description provided - the text between the closest header before the yaml embedding should be used by the tooling layer as the description.

### Source references

You can reference the source definition defined in the `.syml.yml` file or the markdown file with the syml embedding by using common URI schema, and adding the `syml path` at the end.

In this example you can see the following path: 

`./some-schemas.md/schema/markdown-embedded-schema-1` - this path consists of the following parts:

- `./some-schemas.md` - this is the URI part of [the reference](./some-schemas.md) relative to the current file in the example, but URI schema is supported (for example, you can reference another github repository using `http(s)://<path to the specific schema>`).  
- `schema/` the short name of the type of the resource definition (derived from the `kind` field, lowercased) 
- `markdown-embedded-schema-1` the name of the definition (from the `metadata.name` field). Should form the unique pair with the `kind` value in the parent file.