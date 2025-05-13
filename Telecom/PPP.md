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
| Address              | 1                    | 0xFF - standard broadcast address        |
| Control              | 1                    | 0x03, unnumbered data                    |
| Protocol             | 2                    | PPP ID of embedded data                  |
| Information          | variable (0 or more) | datagram                                 |
| Padding              | variable (0 or more) | optional padding                         |
| Frame Check Sequence | 2                    | frame checksum                           |
| Flag                 | 1                    | 0x7E, omitted for successive PPP packets |

### Helpers
[[LCP]] - link control protocol
[[NCP]] - network control protocols (such as [[IPCP]], [[IPXCP]])

Additional protocols, which encapsulates in [[PPP]]

### Features
1) Different networks support (Different networks). We can connect devices from different subnets. 
   PPP allows you to encapsulate traffic from different network protocols ([[IPv4|IP]], [[IPv6]], [[IPX]], [[AppleTalk]]) via Network Control Protocol ([[NCP]]). Each protocol uses a different [[NCP]] (e.g., [[IPCP]] for [[IPv4]], [[IPV6CP]] for [[IPv6]]) that negotiates connection parameters
2) IP address assignment (Address assignment)
There are three addressing schemes:
- Using existing interface addresses (e.g. [[Ethernet]])
- Unique addresses for PPP interfaces (e.g., `hostname-ppp`)
- Automatic assignment via [[IPCP]] (`ip address negotiated` command)
1) [[MLPPP]] - aggregation of several physical cables in one logic 
2) [[PPP]] unnumbered  (A configuration where the [[PPP]] interface does not get a separate [[IPv4]] address, but uses the address of another interface (such as Ethernet))
3) [[PPP]] neighbour route
   After successful [[IPCP]] negotiation, [[PPP]] automatically creates a route to the neighbouring node. Example:
   - A route like `192.168.1.2 via ppp0` is added for interface `ppp0`
   - You can disable it with the `no peer neighbour-route` command

Olifer pg.588