package main

import (
	"datarepo/src/server"
	"datarepo/src/utils"
	"fmt"
	"time"
)

func main() {
	// --------------------- Test for packet --------------------------
	// b := [...]byte{0x00, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x00}
	// pkt := server.Packet{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, b[:]}
	// buf := pkt.ToBuf()
	// fmt.Println(server.FromBuf(buf))

	// pkt2 := server.ServicePacket{pkt, 11, 12, 13, 14}
	// buf2 := pkt2.ToServiceBuf()
	// fmt.Println(server.FromServiceBuf(buf2))

	// ----------------------- Test for Handler Init -----------------------------
	// handler := handler.Handler{}
	// err := utils.LoadFromJson("config/database_configs.json", &handler)
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// err = handler.Init()
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// ----------------------- Test for Handler Write -----------------------------
	// handler := handler.Handler{}
	// err := utils.LoadFromJson("config/database_configs.json", &handler)
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// err = handler.Init()
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// // write in 5 table, time=0, value = xxxx
	// tempData := []float64{1.12312312, 123, 32, 1}
	// err = handler.WriteSynt(4, 0, tempData)
	// if err != nil {
	// 	fmt.Println(err)
	// }

	//-------------- Test for Hanlder Index Read ---------------------
	// handler := handler.Handler{}
	// err := utils.LoadFromJson("config/database_configs.json", &handler)
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// err = handler.Init()
	// if err != nil {
	// 	fmt.Println(err)
	// }
	// // READ from record5 table, time=0
	// data, err := handler.ReadSynt(4, 0)
	// if err != nil {
	// 	fmt.Println(err)
	// }
	// fmt.Println(data)

	// --------------- Test for Data service server ---------------------
	// udpServer := server.Server{}
	// err := utils.LoadFromJson("config/udpserver_configs.json", &udpServer)
	// if err != nil {
	// 	fmt.Println(nil)
	// }
	// err = udpServer.Init()
	// if err != nil{
	// 	fmt.Print(nil)
	// }
	// --------------- Test for Ground <-- Habitat <--> Subsystem ------------------------

	// Start Habitat server
	habitatServer := server.Server{}
	utils.LoadFromJson("config/habitat_server_configs.json", &habitatServer)
	go habitatServer.Init("config/database_configs.json")
	fmt.Println("Habitat Server Started")
	time.Sleep(2 * time.Second)

	// // Start Ground server
	// groundServer := server.Server{}
	// utils.LoadFromJson("config/ground_server_configs.json", &groundServer)
	// go groundServer.Init("config/mirror_configs.json")
	// fmt.Println("Ground Server Started")
	// time.Sleep(2 * time.Second)

	// // Let Ground server subscribe Habitat server
	// habitatServer.Subscribe(3, groundServer.LocalSrc, 0, 1000)
	// fmt.Println("Ground Server subscribed Habitat server")

	for {

	}

}
