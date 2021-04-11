package main

import (
	"github.com/smbgs/syml/go-tools/core"
	"log"
)

func main() {
	core.RegisterCommand("get-schema-from-parquet", func(action core.Action) (core.Data, error) {
		//  TODO: get the actual schema from parquet file passed as URI or resource
		return core.Data{
			"test": 123,
		}, nil
	})

	if err := core.Service("go-parquet"); err != nil {
		log.Fatal("Unable to finalize service:", err)
	}
	log.Fatal("Finished")
}
