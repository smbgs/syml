package main

import "github.com/smbgs/syml/go-tools/core"

func GetSchemaFromParquet(request core.Action) (core.Data, error) {
	return core.Data{
		"adf": 123,
	}, nil
}

func main() {
	core.RegisterCommand("get-schema-from-parquet", GetSchemaFromParquet)
	core.Service()
}
