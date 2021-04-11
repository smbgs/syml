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

	// TODO: call the syml `schemas` service to validate and store the
	//  result. Note, this will require the `schemas` service to
	//  Support getting schemas directly

	// TODO: this should be inside the core
	if err := core.Service("go-parquet"); err != nil {
		log.Fatal("Unable to finalize service:", err)
	}

	log.Fatal("Finished")
}
