Open Shortest Path First. Protocol of dynamic [[Routing|routing]]

### Metric
Metric $M=\frac{BW_{ref}}{BW}$
$BW_{ref}$ - base of metric. Higher limit of interface speed. All values bigger has equal path cost. Any speeds less than 1 are rounded up to 1.
![[Path_cost.jpeg]]

### Areas
[[OSPF]] divides network on areas. [[Router]] does not built network tree for areas he isn't connected.

![[ospf-area-border-router-abr.jpg]]
In AS1 OSPF is used. In AS2 - another protocol

Between areas works like [[Distance vector|distance vector]]. In area works like [[Link state|link state]]
All zones have to be connected to ==Area0==. Connected just to Area1 and Area2 [[Router|router]] can send packets, but can't send [[Router|router information]].

### Router ID
Identifier of [[Router|router]] 

In priority
1) By admin
2) By loopback
3) By physical interface



### OSPF v2
For [[IPv4]]

### OSPF v3
Mostly for [[IPv6]], can be used for [[IPv4]]


