Exists on both [[Physical|physical]] and [[Data link|data link]] layers because it requires special architecture

### In the past
1) Unpredictable upstream time
2) Non-reliable
3) [[Coax]]

### Now
1) [[Optical fiber]] or [[Twisted pair]]
2) Reliable
3) Absolutely predictable

# Physical structure
##### Two types of connection
1) Straight ^da0482
2) Crossover

![[straight_crossover.jpeg]]
Was made before [[Auto MDI,MDIX]] standard appeared. Needed because of different structure of devices in the ends of line. ^b70dbf

### Coding types
![[NRZ_Manch_RZ.jpeg]]
![[Manch.jpeg]]
1) [[NRZ]]
2) [[Manchester]]
3) [[RZ]]

### Ethernet Physical Layer Sublayers
1) [[PCS]]
2) [[PMA]]
3) [[PMD]]

# Algorithm logic
[[CSMA,CD]]

### Technical equipment
L1:
1) [[Hub]]
2) [[Repeater]]
L2:
1) [[Bridge]]
2) [[Switch]]

### MAC
[[MAC]]

### Topology
#### Physical
1) Star (physically with switch in the center)
2) Bus
#### Logic
We can use [[VLAN]] for logical connection

### Frame structure

| Name     | Value                                    | Lenght (bytes) |
| -------- | ---------------------------------------- | -------------- |
| Preamble | 10101010... for sync                     | 7              |
| SFD      | 10101011   label of frame beginning      | 1              |
| DA       | MAC destination                          | 6              |
| SA       | MAC source                               | 6              |
| T/L      | info about lenght(>=1536) or type(<1536) | 2              |
| Payload  | data                                     | 46-1500        |
| FCS      | control sum                              | 4              |
| IFG      | frame gap                                | 12             |
### Half/full duplex

**Half duplex** - sometimes data goes in one direction, sometimes - in another. (now disappeared)
**Full duplex** - always in both direction. 

