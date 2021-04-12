package core

type Data = map[string]interface{}

type Action struct {
	Cid   string `json:"cid"`
	Name  string `json:"name"`
	Args  Data   `json:"args"`
	Shape Data   `json:"shape"`

	Info   bool `json:"info"`
	Errors bool `json:"errors"`
}

type Response struct {
	Cid  string `json:"cid"`
	Data Data   `json:"data"`
}

type Callback = func(action Action) (Data, error)

var Commands = make(map[string]Callback)
