**Transmission Control Protocol**
Protocol number in [[IPv4#^157405|IP header]] is 63

Connection oriented protocol, reliable

Uses [[Port|porst]] and [[Socket|sockets]]
### Header
![[TCP_head.png]] ^5e9227

### Connection establishment
![[Handshake.png]] ^acd395

### Connection termination
![[tcp_termination.png]]
ACK and FIN can be send in one message

### Sliding window
![[Sliding_window.png]] ^6d4218

Window in the same time moves in the right and change its size(changes depends on network quality)

If one packet was lost, window stops and waits while it doesn't come. Any ACKs has got after lost packet doesn't count.

### Slow start
If network is fine, we can increase window size
![[Slow_start.png]]
If network is NOT fine, we can decrease windows size until minimum size

### Path MTUD(iscovery)
Special algorithm for getting to know MTU on the path of packet (to optimise segment size)
We send large packet with upper [[IPv4#^082ef4|flag]] "do not fragment". Too big packet through away with special [[ICMP#^ab6721|ICMP-message]]

Or we can use [[MSS]] :)
# Classic way
Right window edge is last ACKed packet

### Massive ACKs avoidance
If A->B sends lots of packets, B have to send lots of ACKs. That's why was figured out algorithm of Multyacknowledgment when B sends 1 ACK on several packets

# Nowadays

### Fast Retransmition
When the sender receives three identical ACKs for the same segment, it indicates that one or more data segments have been lost. For example, if the sender sent segments 1, 2, 3, and 4, and received ACKs for 1, 2, and 3 but not for 4, then three ACKs for segment 3 indicate the loss of segment 4

### Selective ACK (SACK)
Avoiding Redundant ACKs: Instead of sending an ACK for every packet received, SACK allows the receiver to tell the sender which specific packets were received and which were missing. This significantly reduces the number of ACK packets needed

In [[TCP#^5e9227|TCP options]] we can tag beginning and end of ACKed packets
![[SACK.jpg]]

### TFO (TCP fast open)
We can encapsulate data in [[TCP#^acd395|handshake]]