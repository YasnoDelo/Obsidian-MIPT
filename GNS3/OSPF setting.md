
| Command                                  | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `router ospf 1`                          | инициализируем процесс 1. каждый процесс - одно дерево |
| `router-id 3.3.3.3`                      | Ставим ID на роутере                                   |
| `network 0.0.0.0 255.255.255.255 area 0` | Ставим сети, участвующие в OSPF. Маска wildcart        |
| `sh ip ospf data`                        | Показать всю информацию по OSPF                        |
| `clear ip ospf process`                  | Очистить таблицу маршрутизации                         |


```
++++R2

router ospf 1
network 192.168.23.0 0.0.0.255 area 0
passive-int e2/1

  

++++R3

router ospf 1
network 0.0.0.0 255.255.255.255 area 0
router-id 3.3.3.3

  

++++R4

router ospf 1
network 0.0.0.0 255.255.255.255 area 0
int lo0
ip add 4.4.4.4 255.255.255.255
int lo1
ip add 44.44.44.44 255.255.255.255

  

++++R5

router ospf 1
network 192.168.45.0 0.0.0.255 area 0
```