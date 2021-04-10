package core

import (
	"bufio"
	"encoding/json"
	"github.com/mitchellh/go-homedir"
	"log"
	"net"
	"os"
)

type Data = map[string]interface{}

type Action struct {
	Name  string `json:"nameK"`
	Args  Data   `json:"args"`
	Cid   string `json:"cid"`
	Shape Data   `json:"shape"`

	Info   bool `json:"info"`
	Errors bool `json:"errors"`
}

type Response struct {
	Data Data   `json:"data"`
	Cid  string `json:"cid"`
}

type Callback = func(action Action) (Data, error)

var Commands = make(map[string]Callback)

func HandleClient(conn net.Conn) {
	log.Printf("Client connected [%s]", conn.RemoteAddr().Network())

	var action Action

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)

	line, _, _ := reader.ReadLine()

	if err := json.Unmarshal(line, &action); err != nil {
		panic(err)
	}

	callback := Commands[action.Name]

	log.Print(Commands)
	log.Print(action)

	data, err := callback(action)
	response := Response{
		Data: data,
		Cid:  action.Cid,
	}

	marshal, err := json.Marshal(response)
	if err != nil {
		log.Fatal(err)
	}
	_, err = writer.Write(marshal)

	_, err = writer.WriteString("\n")
	err = writer.Flush()

	if err != nil {
		log.Fatal(err)
	}

	err = conn.Close()

	if err != nil {
		log.Fatal(err)
	}

}

func RegisterCommand(
	name string,
	handler Callback,
) {
	Commands[name] = handler
}

func Service() {
	var sockAddr = "~/.syml/sockets/test-go-socket.sock"

	sockAddr, err := homedir.Expand(sockAddr)

	if err := os.RemoveAll(sockAddr); err != nil {
		log.Fatal(err)
	}

	l, err := net.Listen("unix", sockAddr)
	if err != nil {
		log.Fatal("listen error:", err)
	}

	log.Print("Started unix server at:", sockAddr)

	defer l.Close()

	for {
		// Accept new connections, dispatching them to echoServer
		// in a goroutine.
		conn, err := l.Accept()

		if err != nil {
			log.Fatal("accept error:", err)
		}

		go HandleClient(conn)
	}
}
