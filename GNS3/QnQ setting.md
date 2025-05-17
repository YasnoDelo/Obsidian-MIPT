Чтобы можно было связывать вот такие схемы
![[QnQ_schema.png]]
Где [[VLAN setting|VLAN]] у компов из разных офисов совпадают:
![[QnQ_VLAN_plan.png]]
Нужно настроить свитчи так:
1) SW1,2,5,6 - access с нужным VLAN в сторону клиента и trunk в сторону провайдерского оборудования
2) SW3,4: ![[QnQ_SW3_conf.png]]![[QnQ_SW4_conf.png]]
3) На R1:
```
conf t
int f0/0
no sh

int f0/0.112
encapsulation dot1Q 11 second-dot1q 2
ip add 192.168.0.1 255.255.255.0

int f0/0.113
encapsulation dot1Q 11 second-dot1q 3
ip add 192.168.1.1 255.255.255.0

int f0/0.122
encapsulation dot1Q 12 second-dot1q 2
ip add 192.168.2.1 255.255.255.0

int f0/0.123
encapsulation dot1Q 12 second-dot1q 3
ip add 192.168.3.1 255.255.255.0
```


| command                                                        | discription                                                                                                              |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `encapsulation dot1Q` + QnQ_VLAN_num `second-dot1q` + VLAN_num | Настроить на декапсуляцию сначала внешнего тега от QnQ (QnQ_VLAN_num), а потом - внутреннего от обычного VLAN (VLAN_num) |
