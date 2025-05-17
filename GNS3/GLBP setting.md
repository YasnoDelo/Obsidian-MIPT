Всё как в [[VRRP setting|VRRP]] и [[HSRP setting|HSRP]]

R1:
```
int f1/0
glbp 1 ip 192.168.123.123
glbp 1 preempt
glbp 1 load-balancing weighted 
```
