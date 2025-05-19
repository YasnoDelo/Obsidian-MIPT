![[Pasted image 20250517165222.png]]
R1
```
configure terminal
vlan 200
private-vlan primary
end
do sh vlan private-vlan
```

R2
```
conf t
int f/1/0
no sh
ip add 10.10.12.2 255.255.255.0
```