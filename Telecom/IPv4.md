### Why does it exist?
Because [[MAC|MAC addresses]] are not hierarchical.

### Addresses

^69527c

length: 32 bytes $\Rightarrow$ $2^{32}$ variants of addresses 

Four octets:

| 1    | 2    | 3    | 4    | info                     |
| ---- | ---- | ---- | ---- | ------------------------ |
| 192. | 168. | 15.  | 47   | usual                    |
| 255. | 255. | 255. | 255. | [[Broadcast\|broadcast]] |

### Header format

^157405

Minimum size is 20 byte!
![[IP_header.webp]]

| Name                | Value                                                                                                  | Meaning                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Version             | Always equal to 4                                                                                      | :)                                                                     |
| IHL                 | 5-15                                                                                                   | Internet Header Length (in 4-bytes words)                              |
| DSCP                |                                                                                                        | Differentiated Services Code Point                                     |
| ECN                 |                                                                                                        | Explicit Congestion Notification                                       |
| Total Length        |                                                                                                        | Total Length including header and data                                 |
| Identification      |                                                                                                        | Used to define, what part of divided data came                         |
| Flags               | - bit 0: Reserved; must be zero<br>- bit 1: Don't Fragment (DF)<br>- bit 2: More Fragments (MF)        |                                                                        |
| Fragment offset     | - 1st [[IPv4#^5c35ae\|part]]:  is not shifted<br>- 2nd [[IPv4#^5c35ae\|part]]:  shifted from beginning | Offset of current message from the beginning (counts in 8-bytes words) |
| TTL                 | 255 minus amount of devices packet went througth                                                       | Time to live                                                           |
| Protocol            | 3                                                                                                      |                                                                        |
| Header checksum     |                                                                                                        |                                                                        |
| Source address      |                                                                                                        |                                                                        |
| Destination address |                                                                                                        |                                                                        |
| Options             |                                                                                                        | Is not necessary                                                       |

^082ef4

### Fragment division
If length of [[UDP]] data (for example) is too much for packet, it divides into parts 

Is field [[IPv4#^082ef4|total length]] 

### [[Class system]]
Class system of addressing
### [[CIDR]]
Mask system of addressing

| Class name | Value in the beggining (class system) | Value CIDR                | Point     |
| ---------- | ------------------------------------- | ------------------------- | --------- |
| A          | 0                                     | 0.0.0.0–127.255.255.255   |           |
| B          | 10                                    | 128.0.0.0–191.255.255.255 |           |
| C          | 110                                   | 192.0.0.0–223.255.255.255 |           |
| D          | 1110                                  | 224.0.0.0–255.255.255.255 | multicast |
| E          | 1111                                  | 224.0.0.0–255.255.255.255 | reserved  |
### [[ARP]] & [[proxy-ARP]]
Help to understand [[MAC]], knowing IP

### How I understand is device in my subnet
Knowing mask, I calculate network address. If device's address located here, here it is!

### [[ICMP]]
![[ICMP#^0137eb]]

### [[DHCP]]
![[DHCP#^ea08f6]] ![[DHCP#^e5638b]]
### Addressing

