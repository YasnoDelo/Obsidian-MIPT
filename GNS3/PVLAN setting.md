Configuring a  [[VLAN setting|VLAN]]  as a PVLAN
```
configure terminal
vlan 202
private-vlan primary
end
do sh vlan private-vlan
```

```
configure terminal
vlan 303
private-vlan community
end
show vlan private-vlan
```

```
configure terminal
vlan 440
private-vlan isolated
end
show vlan private-vlan
```

Associating a Secondary [[VLAN setting|VLAN]] with a Primary [[VLAN setting|VLAN]] 

```
configure terminal
vlan 202
private-vlan association 303-307,309,440
end
show vlan private-vlan
```

Configuring a Layer 2 Interface as a PVLAN Promiscuous Port
```
configure terminal
interface fastethernet 5/2
switchport mode private-vlan promiscuous
switchport private-vlan mapping 200 2 // 200 - primary, 2 - secondary vlan
end
```

Configuring a Layer 2 Interface as a PVLAN Host Port
```
configure terminal
interface fastethernet 5/1
switchport mode private-vlan host
switchport private-vlan host-association 200 2 // 200 - primary, 2 - secondary
end
```

Configuring a Layer 2 Interface as a PVLAN Trunk Port
```
configure terminal
interface fastethernet 5/1
switchport private-vlan association trunk 200 2 // 200 - primary, 2 - secondary
switchport mode private-vlan trunk
end
```

Permitting Routing of Secondary [[VLAN setting|VLAN]] Ingress Traffic
```
configure terminal
interface vlan 202
private-vlan mapping add 303-307,309,440
end
show interfaces private-vlan mapping
```
### Example

R1:
```
conf t

vlan 2001
name PRIMARY
vlan 2003
name ISOLATED
ex
do sh vlan
int range fa0/10-12
switchport mode access
ex
vlan 2001
private-vlan primary
vlan 2003
private-vlan isolated
ex
vlan 2001
private-vlan association 2003
ex
do sh vlan
do sh vlan pri
switchport mode private-vlan host
switchport private-vlan host 2001 2003
do sh vlan priv
switchport mode private-vlan pr
switchport private-vlan mapping 2001 2003
do sh int fa0/12 sw

```
R2:
```
int fa0/12
no switchport
no sh
ip add 192.168.1.2 255.255.255.0

```
R3
```
enable
conf t
int fa1/0/12
no switchport
no sh
ip add 192.168.1.4 255.255.255.0
```
R4:
```
enable
conf t
int g0/1
no switchport
no sh
ip add 192.168.1.21 255.255.255.0
```
