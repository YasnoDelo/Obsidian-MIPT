
| Comand                            | Description                                            |
| --------------------------------- | ------------------------------------------------------ |
| `int tun0`                        | поднимаем интерфейс для туннеля                        |
| `tunnel mode` + mode_name         | Настраиваем туннель                                    |
| `tunnel mode gre ip`              | Настраиваем туннель IP через GRE                       |
| `tunnel source e2/3`              | Отправитель через физический интерфейс (плохой дизайн) |
| `tunnel destination 192.168.45.5` | Получатель через IP                                    |
| `keepalive`                       | Мониторинг состояния туннеля                           |
|                                   |                                                        |

```
int tun0
ip add 192.168.25.2 255.255.255.0  // логический адрес туннеля
tunnel mode gre ip
tunnel source Ethernet2/3
tunnel destination 192.168.45.5    // адрес физического интерфейса
keepalive