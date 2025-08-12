**Spanning Tree Protocol**

Prevents the formation of loops from L2 [[Switch|switches]].

Main terms:
1) Bridge ID (priority (32768 by default + VLAN num) + MAC address) - 8 byte
2) Root Bridge ID
3) Port ID
4) Root Path Cost (depends on interface capacity)

#Algorythm 
1) Choosing of root bridge (the smallest Bridge ID)
2) Choosing of root ports
3) Choosing of designed ports
4) Blocking redundant channels

### Choosing of root bridge
1) Each [[Switch|switch]] sends [[BPDU]] messages, where say, that he is root
2) If [[Switch|switch]] sees, that there is another having less Bridge ID, he starts to send messages, where says, that it knows, what bridge is the root, and how far it is
### Choosing of ==root== port (or who is ==root== port)
The choice on which [[Switch|switch]] to make forwarding as ==root port== occurs according to the following scheme (The points are listed in descending order of importance):

- Lower Root Path Cost
- Lower neighbour's Bridge ID 
- Lower neighbour's Port ID 
- Lower it's own Port ID 

Won port (which has lower Root Path Cost for example) is ==root== port.

### Choosing of ==designated== port (or who is ==designated== port)
The choice on which [[Switch|switch]] to make forwarding as ==designated== port occurs according to the following scheme (The points are listed in descending order of importance):

- Lower Root Path Cost
- Lower neighbour's Bridge ID 
- Lower it's own Port ID 

Won port (which has lower Root Path Cost for example) (and who is not ==root== port) is ==designated==.

### Ports types
1) Root port - toward root
2) Designed port - listen and talk
3) Blocked port - don't listen or talk

### Ports state
1) Forwarding - stable state
2) Learning - analyse frames from users (fulling of [[Switch|MAC-table]])  
3) Listening - just listen [[BPDU]] frames (15 sec and can appear in Learning state)
4) Blocked - stable state

### Timers
[[Switch]] sens [[BPDU]]'s every 2 sec. If don't receive [[BPDU]]'s 20 sec, then sends [[BPDU]] with TCN flag upper to root. Received [[Switch|switch]] sends [[BPDU]] with flag TCA upper back

TCN - Topology Change N?
TCA - Topology Change Acknowlegment

If root disappears - setting algorythm repeats. 

### Versions

##### RSTP
No timers (just hello-timer = 2 sec)!
#Algorythm 
0) Root is chosen like in STP
1) Root blocks all ports for users
2) Root sends proposal messages
3) All routers block all ports for traffic except of port, which received  proposal message and send agreement back
4) 2 lvl [[Switch|switches]] repeat algorythm 

##### PVSTP
[[VLAN]] added (own tree for every [[VLAN]])
##### PVSTP+
[[VLAN#^c400a0|IEEE 802.1q]] support added. Instead of cisco's [[ISL]]
##### Rapid PVSTP
RSTP for each [[VLAN]]
##### MSTP
Multiple STP (we can make groups of [[VLAN|VLANs]] in one instance)
No timers!

### Advanced fuatures


| Name                | Description                                                      | Example                                                                                   |
| ------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| BPDU Guard          | If [[BPDU]] received, inteface will turn off                     | Port (may be access port) to user. Use in case, when we don't wait any [[BPDU]] from user |
| BPDU Guard advanced | If [[BPDU]] received, port will not send any [[BPDU]]            | Port (may be access port) to user. Use in case, when we wait some [[BPDU]] from user      |
| Root Guard          | Ports with this feature can't be [[STP\|root ports]]             | Port of root (or of back up root)                                                         |
| Port Fast           | Allow us to skip [[STP\|listening]] and [[STP\|learning]] stages | Port to user                                                                              |
| Loop Guard          | If [[BPDU]] wasn't received, port will not send any [[BPDU]]     | Port from root to backup root                                                             |
### Atacks
| Name                        | Description                                                                                        | Example                      |
| --------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------- |
| [[MAC\|MAC-table]] owerflow | In A send lots of [[MAC\|MACs]] from A host. [[Switch]] becomes [[Hub\|hub]]. A can listen B and C | ![[MAC_overflow.jpg]]        |
| [[MAC\|MAC]] rewrite        | obvios                                                                                             | Eva receives foreign traffic |
| [[DHCP]] starvation         | Eva wants too many addresses                                                                       | DoS                          |
| [[DHCP]] rogue              | Second EVIL [[DHCP]] server send wrong gateway                                                     | [[MITM\|Man In The Midle]]   |
| [[ARP]] spoofing            | A sends [[ARP\|ARP-request]]: what IP has B? C replies                                             |                              |
