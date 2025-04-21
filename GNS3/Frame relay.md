`do sh frame pvc` - посмотреть инфу про статистику и FR
`do sh frame map` - посмотреть инфу про подключения


R4
```
conf t
int se4/0
no sh

enc fr

int s4/0.102 point-to-point
frame-relay interface-dlci 102
exit
ip add 192.168.24.4 255.255.255.0

do sh frame pvc
```

R2
```
conf t
int se4/0
no sh

enc fr

int s4/0.104 point-to-point
frame-relay interface-dlci 104
exit
ip add 192.168.24.2 255.255.255.0
```