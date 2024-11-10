Config commands

### How to go in
command from [[Privileged mode|privileged mode]] 
```bash
conf t
```

### How to go out
command 
```bash
exit
```

### Missing commands
1) No ```ping``` (just ```do ping```)
2) No ```show verion``` (```do show verion```)

| ```hostname``` + name                   | Изменяет нынешнее имя                                         |
| --------------------------------------- | ------------------------------------------------------------- |
| ```interface``` + name                  | Режим настройки интерфейса name                               |
| `no shutdown`                           | Активировать интерфейс                                        |
| `line vty` + fst_num + last_num         | Зайти в настройку линии                                       |
| `login local`                           | Создание базы данных пользователей (только в настройке линии) |
| `username` + name + `secret` + password | Создаём нового пользователя                                   |
|                                         |                                                               |
|                                         |                                                               |
| ACL'ы                                   |                                                               |
| `access-group` + ACL_num + `out/in`     | Настроить ACL на интерфейс                                    |
|                                         |                                                               |
|                                         |                                                               |
OR ```do + any_command```