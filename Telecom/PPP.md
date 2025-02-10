**Point-to-Point Protocol**

1) Intelligent 
2) [[IPv4]], [[IPv6]]
3) [[Control plane|Control protocols]]
4) Authentication for proper equipment
5) Synchronization

### Header
| Name                 | Number of bytes      | Description                              |
| -------------------- | -------------------- | ---------------------------------------- |
| Flag                 | 1                    | 0x7E, the beginning of a PPP frame       |
| Address              | 1                    | 0xFF, standard broadcast address         |
| Control              | 1                    | 0x03, unnumbered data                    |
| Protocol             | 2                    | PPP ID of embedded data                  |
| Information          | variable (0 or more) | datagram                                 |
| Padding              | variable (0 or more) | optional padding                         |
| Frame Check Sequence | 2                    | frame checksum                           |
| Flag                 | 1                    | 0x7E, omitted for successive PPP packets |

### Helpers
[[LCP]] - link control protocols
[[NCP]] - network control protocols

Additional protocols, which encapsulates in [[PPP]]

### Features
1) Different networks
2) Address assignment
3) MLPPP
4) PPP unnumbered
5) PPP neighbour route

