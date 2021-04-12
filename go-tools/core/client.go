package core

import (
	"bufio"
	"encoding/json"
	"fmt"
	"github.com/mitchellh/go-homedir"
	"log"
	"net"
	"os"
)

type ServiceClient struct {
	Connection  net.Conn
	ServiceName string
}

func makeServiceClient(serviceName string) ServiceClient {
	var sockAddr = fmt.Sprintf("~/.syml/sockets/%s.sock", serviceName)

	sockAddr, err := homedir.Expand(sockAddr)

	if err := os.RemoveAll(sockAddr); err != nil {
		log.Fatal(err)
	}

	conn, err := net.Dial("unix", sockAddr)
	if err != nil {
		log.Fatal("listen error:", err)
	}

	return ServiceClient{
		ServiceName: serviceName,
		Connection:  conn,
	}
}

func (client ServiceClient) Call(action Action) Response {

	reader := bufio.NewReader(client.Connection)
	writer := bufio.NewWriter(client.Connection)

	marshal, err := json.Marshal(action)

	if err != nil {
		log.Fatal(err)
	}

	_, err = writer.Write(marshal)
	_, err = writer.WriteString("\n")
	err = writer.Flush()

	line, _, _ := reader.ReadLine()

	var response Response

	if err := json.Unmarshal(line, &response); err != nil {
		// TODO: don't panic!
		panic(err)
	}

	return response

}

func (client ServiceClient) Close() error {
	return client.Connection.Close()
}
