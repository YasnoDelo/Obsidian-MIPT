(virtual local area network)

Is edge for [[Broadcast|broadcast domain]]

Trunk is connection between [[Switch|switches]]
### Trunk frame structure (IEEE 802.1q)

| Name     | Value                                    | Lenght (bytes) |
| -------- | ---------------------------------------- | -------------- |
| Preamble | 10101010... for sync                     | 7              |
| SFD      | 10101011   label of frame beginning      | 1              |
| DA       | MAC destination                          | 6              |
| SA       | MAC source                               | 6              |
| TRID     | Tag protocol identifier (0x8100)         | 2              |
| PCP      | Priority code point                      | 3/8            |
| DEI      | Discard eligibility identifier           | 1/8            |
| VID      | VLAN identifier                          | 1.5            |
| T/L      | info about lenght(>=1536) or type(<1536) | 2              |
| Payload  | data                                     | 46-1500        |
| FCS      | control sum                              | 4              |
| IFG      | frame gap                                | 12             |

![[VLAN.png]]

### Types of ports
1) **Access port или порт доступа** — A port that is on a specific [[VLAN]] and transmits untagged frames. Typically, this is a port looking at a user device
2) **Trunk port или магистральный порт** — A port that carries tagged traffic (untagged frames means as tagged with native one). Typically, this port is raised between network devices ([[Switch|SW]], [[Router|R]])

### Native VLAN
Automatically set VLAN ID (if non-tagged frame goes through Trunk port, it automatically treated as tagged with native one) 