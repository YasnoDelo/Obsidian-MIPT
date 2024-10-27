**Transmission Control Protocol**
Protocol number in [[IPv4#^157405|IP header]] is 63

Connection oriented protocol, reliable

Uses [[Port|porst]] and [[Socket|sockets]]
### Header
![[TCP_head.png]]

### Connection establishment
![[Handshake.png]]

### Connection termination
![[tcp_termination.png]]
ACK and FIN can be send in one message

### Sliding window
![[Sliding_window.png]]

Window in the same time moves in the right and change its size(changes depends on network quality)

If one packet was lost, window stops and waits while it doesn't come. Any ACKs has got after lost packet doesn't count.

### Slow start
If network is fine, we can increase window size
![[Slow_start.png]]
If network is NOT fine, we can decrease windows size until minimum size