# TPC-H SYML Markdown Sample
This is the common TPC-H SYML  schema sample as it is defined in the Snowflake example.

Based on http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf

### Part
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-part
  version: 2.17.1
  desc: >
    Parts that can be supplied to customers    
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      type: dimension
      database: DEMO_DB
      schema: TPC-H
      table: PART
    
  common:   
    analytics:
      enabled: true
    metrics:
    - metric: distinct
  
    dimension: overwrite
    
  fields:
  
  - name: P_PARTKEY
    type: TEXT
    tags: ["pk"]
  
  - name: P_NAME 
    type: TEXT
  
  - name: P_MFGR 
    type: TEXT
    
  - name: P_BRAND 
    type: TEXT
    
  - name: P_TYPE 
    type: TEXT
  
  - name: P_SIZE
    type: INTEGER
    
  - name: P_CONTAINER
    type: TEXT
    analytics:
      metrics:
      - metric: enum
  
  - name: P_RETAILPRICE
    type: DECIMAL
    analytics:
      metrics:
      - metric: spread
        top: 10
    
  - name: P_COMMENT 
    type: TEXT
  
```

### Supplier
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-supplier
  version: 2.17.1
  desc: >
    Part supplier
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      type: dimension
      database: DEMO_DB
      schema: TPC-H
      table: SUPPLIER
    
  fields:
  - name: S_SUPPKEY
    type: TEXT
    tags: ["pk"]
    
  - name: PROFILE
    type: GROUP
      dimension: overwrite    
    
    fields: 
  
    - name: S_NAME 
      type: TEXT    

    - name: S_ADDRESS
      type: TEXT

    - name: S_NATIONKEY 
      type: TEXT
      relation:
        type: foreign-key
        tags: ["logical"]
        target:
        schema: @md/schema/tpc-h-nation
        field: NATIONKEY

    - name: S_PHONE
      type: TEXT
  
    - name: S_ACCTBAL
      type: DECIMAL
    
  - name: S_COMMENT
    type: TEXT
  
```

### Part  supplier
```yaml
gapiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-part-supplier
  version: 2.17.1
  desc: >
    Links the parts to suppliers and adds availability and supply costs
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      type: dimension-link
      database: DEMO_DB
      schema: TPC-H
      table: PARTSUPP
    
  fields:
    
  - name: PS_PARTKEY
    type: TEXT
    tags: ["pk"]
    relation:
      type: foreign-key
    target:
      schema: @md/schema/tpc-h-part
      field: P_PARTKEY
      
  - name: PS_SUPPKEY
    type: TEXT
    tags: ["pk"]
      relation:
      type: foreign-key
    tags: ["logical"]
    target:
      schema: @md/schema/tpc-h-supplier
      field: S_SUPKEY

  - name: PS_AVAILQTY
    type: INTEGER

  - name: PS_SUPPLYCOST
    type: INTEGER
    
  - name: COMMENT
    type: TEXT  
      
```

### Orders
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-order
  type: domain  
  version: 2.17.1
  desc: >
    Customer orders
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      database: DEMO_DB
      schema: TPC-H
      table: ORDER
    
  fields:
  
  - name: O_ORDERKEY
    type: TEXT
    tags: ["pk"]

  - name: O_CUSTKEY
    type: TEXT

  - name: O_ORDERSTATUS
    type: TEXT

  - name: O_TOTALPRICE
    type: DECIMAL

  - name: O_ORDERPRIORITY
    type: TEXT

  - name: O_CLERK
    type: TEXT

  - name: O_SHIPPRIORITY
    type: INTEGER

  - name: O_COMMENT
    type: TEXT

```

### Line item
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-line-item
  type: fact  
  version: 2.17.1
  desc: > 
    Detailed list of order lines
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      database: DEMO_DB
      schema: TPC-H
      table: LINEITEM
    
  fields:
  
  - name: L_ORDERKEY
    type: TEXT
    tags: ["pk"]

  - name: L_PARTKEY
    type: TEXT

  - name: L_SUPPKEY
    type: TEXT

  - name: L_LINENUMBER
    type: INTEGER
    tags: ["pk"]

  - name: L_LINESTATUS
    type: TEXT

  - name: MONETARY
    type: GROUP

    fields:

    - name: L_QUANTITY
      type: DECIMAL

    - name: L_EXTENDEDPRICE
      type: DECIMAL

    - name: L_DISCOUNT
      type: DECIMAL

    - name: L_TAX
      type: DECIMAL

  - name: SHIPPING
    type: GROUP

    - name: L_RETURNFLAG
      type: TEXT

    - name: L_SHIPDATE
      type: DATE

    - name: L_COMMITDATE
      type: DATE

    - name: L_RECEIPTDATE
      type: DATE

    - name: L_SHIPINSTRUCT
      type: TEXT

    - name: L_SHIPMODE
      type: TEXT

    - name: L_COMMENT
      type: TEXT

```

### Customer
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-customer
  type: domain  
  version: 2.17.1
  desc: >
    Customer orders
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      database: DEMO_DB
      schema: TPC-H
      table: CUSTOMER
    
  fields:
  
  - name: C_CUSTKEY
    type: TEXT
    tags: ["pk"]
    
  - name: PROFILE
    type: GROUP
      dimension: overwrite  

    fields:

    - name: C_NAME 
      type: TEXT    

    - name: C_ADDRESS
      type: TEXT

    - name: C_NATIONKEY 
      type: TEXT
      relation:
      type: foreign-key
      tags: ["logical"]
      target:
        schema: @md/schema/tpc-h-nation
        field: NATIONKEY

    - name: C_PHONE
      type: TEXT

    - name: C_ACCTBAL
      type: DECIMAL
      desc: Account balance

  - name: C_MKTSEGMENT
    type: TEXT

  - name: C_COMMENT
    type: TEXT
```

### Nation
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-nation
  type: dimension  
  version: 2.17.1
  desc: >
    Nation (country etc.)
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      database: DEMO_DB
      schema: TPC-H
      table: NATION
    
  fields:
  
  - name: NATIONKEY
    type: TEXT
    tags: ["pk"]
  
  - name: NAME 
    type: TEXT    

  - name: REGIONKEY 
    type: TEXT    
      relation:
      type: foreign-key
    tags: ["logical"]
    target:
      schema: @md/schema/tpc-h-region
      field: R_REGIONKEY

  - name: COMMENT
    type: TEXT    

```



### Region
```yaml
apiVersion: v1.syml.somebugs.com
kind: Schema
meta:
  name: tpc-h-region
  type: dimension  
  version: 2.17.1
  desc: > 
    Region (asia, europe etc.)
  
spec:

  dest:
    kind: database
    provider: snowflake
    type: table
    spec:
      database: DEMO_DB
      schema: TPC-H
      table: REGION
    
  fields:
  
  - name: R_REGIONKEY
    type: TEXT
    tags: ["pk"]
  
  - name: R_NAME 
    type: TEXT    

  - name: R_COMMENT
    type: TEXT    

```
