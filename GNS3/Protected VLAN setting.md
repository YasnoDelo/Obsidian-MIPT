R1:
```
// Настроим VLAN
vlan 10
name Users
exit

// Назначим порты в VLAN
interface range fa0/1 - 2
switchport mode access
switchport access vlan 10
switchport protected
spanning-tree portfast
no shutdown

interface fa0/24
switchport mode access
switchport access vlan 10
spanning-tree portfast
no shutdown
```

В данном случае `fa0/1` и `fa0/2` - protected. Они не могу общаться руг с другом, но каждый из них может общаться с non-protected `fa0/24`
