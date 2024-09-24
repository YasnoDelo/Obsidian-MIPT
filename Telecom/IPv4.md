### Why does it exist?
Because [[MAC|MAC addresses]] are not hierarchical.

### Addresses
length: 32 bytes

Four octets:

| 1    | 2    | 3    | 4    | info      |
| ---- | ---- | ---- | ---- | --------- |
| 192. | 168. | 15.  | 47   | usual     |
| 255. | 255. | 255. | 255. | broadcast |
\
### Header format
![[IP_header.webp]]

| Name                | Value                                                                                                  | Meaning                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Version             | Always equal to 4                                                                                      | :)                                                               |
| IHL                 | 5-15                                                                                                   | Internet Header Length                                           |
| DSCP                |                                                                                                        | Differentiated Services Code Point                               |
| ECN                 |                                                                                                        | Explicit Congestion Notification                                 |
| Total Length        |                                                                                                        | Total Length including header and data                           |
| Identification      |                                                                                                        | Used to define, [[IPv4#^5c35ae\|what part]] of divided data came |
| Flags               | - bit 0: Reserved; must be zero<br>- bit 1: Don't Fragment (DF)<br>- bit 2: More Fragments (MF)        |                                                                  |
| Fragment offset     | - 1st [[IPv4#^5c35ae\|part]]:  is not shifted<br>- 2nd [[IPv4#^5c35ae\|part]]:  shifted from beginning |                                                                  |
| TTL                 |                                                                                                        | Time to live                                                     |
| Protocol            |                                                                                                        |                                                                  |
| Header checksum     |                                                                                                        |                                                                  |
| Source address      |                                                                                                        |                                                                  |
| Destination address |                                                                                                        |                                                                  |
| Options             |                                                                                                        | Is not necessary                                                 |

^082ef4

### Fragment division
If length of [[UDP]] data is too much for packet, it divides into parts 

Is field [[IPv4#^082ef4|total length]] 