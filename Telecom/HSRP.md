**Hot Standby Router Protocol**
### Roles
0) Group - [[Default gateway|default gateways]] united into local segment

|                        | V1 groups                   | V2 groups                   |
| ---------------------- | --------------------------- | --------------------------- |
| Amount of groups       | 10-255                      | 0-4095                      |
| Virtual-MAC            | $0000.0c07.AC\overline{xy}$ | $0000.0C9F.F\overline{xyz}$ |
| Multicast inside group | 224.0.0.2                   | 224.0.0.102                 |

1) Active
#Comment 
	1. Replies for [[ARP]]
	2. Relays the packets
	3. Sends [[HSRP]]-hellos
	4. Group's virtual-MAC = $0000.0c07.ac\overline{xy}$, there $\overline{xy}$ - number of group for example
2) Stanby
	1. Listen [[HSRP]]-hellos
	2. Wait timer (10 sec)

### Elections
1) Priority (0-255). Highest - active. Default = 100
2) IP address. Highest - active
3) Priority can be changed by track (from main routers upside)
4) Preempt - mechanism of active role interception
#Comment 

### Messages
1) Hello-message
2) Resign-message (new active)
3) Coup-message (while preempt)

### States
1) Initial (link up)
2) Learn (VIP)
3) Listen (knowing VIP, hello)
4) Speak (Election)
5) Standby (know who is active. he isn't)
6) Active

