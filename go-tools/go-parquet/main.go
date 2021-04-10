package main

import (
	"github.com/smbgs/syml/go-tools/core"
	"log"
)

func GetSchemaFromParquet(request core.Action) (core.Data, error) {
	return core.Data{
		"adf": 123,
	}, nil
}

func main() {
	core.RegisterCommand("get-schema-from-parquet", GetSchemaFromParquet)

	if err := core.Service(); err != nil {
		log.Fatal("Unable to finalize service:", err)
	}
	log.Fatal("Finished")

}
