More powerful  commands

### How to go in
command from [[User mode|user mode]] 
```bash
enable
```

### How to go out
command 
```bash
disable
```

### Some commands
| Основные                                         |                                                          |
| ------------------------------------------------ | -------------------------------------------------------- |
| ```show version```                               | Всякая инфа про заргузку (ОС, версия)                    |
| ```show inventory```                             | Показывает установленные модули                          |
| ```show env```+ ...                              | Показывает температуру и другие характеристики           |
| ```show processes``` + ...                       | Показывает процессы                                      |
| ```show processes cpu history```                 | Показывает графики загруженности                         |
|                                                  |                                                          |
| **Сессионные**                                   |                                                          |
| ```reload```                                     | Перезагружает                                            |
| ```show running-config```                        | Показывает содержание запущенного конфига                |
| ```show startup-config```                        | Показывает содержание стартового конфига                 |
| ```copy running-config startup-config```         | Перезапись из первого конфига во второй                  |
| ```write```                                      | Записывает из рана в стартап                             |
| ```show history```                               | Показывает историю введённых команд                      |
|                                                  |                                                          |
| Инфо про интерфейсы                              |                                                          |
| ```debug``` + ...                                | Включает дебаг                                           |
| ```undebug``` + ... / ```no debug``` + ...       | Выключает дебаг                                          |
| ```show ip interface brief```                    | Показать все интерфейсы                                  |
| `show cdp neighbour`                             | Показать все соседние устройства (подключённые напрямую) |
| `show cdp entry` + name                          | Все данные об устройстве рядом                           |
| `clear line` + port_name                         | Очистить все процессы                                    |
| `show interface` + interface name                | Подробная информация про инрефейс                        |
| `ping` + ip name $\pm$ repeat + amount of repeat | Пинг ip-адреса                                           |
| `show inventory`                                 | Информация про подключённые интерфейсы (с нумерацией)    |
|                                                  |                                                          |
| Инфо про рантайм                                 |                                                          |
| `show run \| incl dhcp`                          | Показывает настройки именно DHCP                         |
|                                                  |                                                          |
| Инфо про ACL                                     |                                                          |
| `sh ip access`                                   | Показать все ACL'ы                                       |
