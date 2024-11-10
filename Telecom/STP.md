**Spanning Tree Protocol**

Prevents the formation of loops from L2 [[Switch|switches]].

Main terms:
1) Bridge ID (priority (32768 by default + VLAN num) + MAC address)
2) Root Bridge ID
3) Port ID
4) Root Path Cost (depends on interface capacity)

#Algorythm 
1) Choosing of root bridge (the smallest Bridge ID)
2) Blocking redundant channels

The choice on which [[Switch|switch]] to block the port occurs according to the following scheme:

- Lower Root Path Cost.
- Lower Bridge ID.
- Lower Port ID.

Lost port (which has lower Root Path Cost for example) are blocked. Wined ports are in  forwarding mode. 
