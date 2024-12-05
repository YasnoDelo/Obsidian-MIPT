## PAT
```
//ACL потребуется позже

ip access-list extended 100
permit ip 192.168.134.0 0.0.0.255 any

//настройка интерфейсов
int g1/0
ip nat inside

int f0/0
ip nat outside

// Далее в priveleged mode
ip nat inside source list 100 interface f0/0 overload
do sh ip nat tra //показывает действующие подмены
do sh ip nat stat 
```

| ПО ЧАСТЯМ         | ЗАЧЕМ                                             |
| ----------------- | ------------------------------------------------- |
| `ip nat`          | командуем для nat                                 |
| `inside`          | говорим, что начинаем разбирать логику трансляции |
| `source list 100` | Sourse, который проходит правила ACL 100          |
| `interface f0/0`  | Sourse выше заменяется на IP на интерфейсе `f0/0` |
| `overload`        | Указание, чтобы использовалось PAT                |

## PAT+NAT
```
\\ in global config
\\ инициализировали пул
ip nat pool CiscoPool 10.0.0.1 10.0.0.10 netmask 255.0.0.0
ip nat inside source list 100 pool CiscoPool overload
```

## NAT
Настраивается как PAT+NAT, но без ==overload==
