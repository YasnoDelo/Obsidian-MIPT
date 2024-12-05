Process on the [[Router]] 
1) Table fulling
2) Table using

| Protocol                                                         | Abr         | Administrative distance  |
| ---------------------------------------------------------------- | ----------- | ------------------------ |
| Directly connected                                               | C           | 0                        |
| Static route                                                     | S           | 1                        |
| Enhanced Interior Gateway Routing Protocol (EIGRP) summary route | D (summary) | 5                        |
| External Border Gateway Protocol (BGP)                           | B           | 20                       |
| Internal EIGRP                                                   | D           | 90                       |
| Interior Gateway Routing Protocol (IGRP)                         | I           | 100                      |
| Open Shortest Path First (OSPF)                                  | O           | 110                      |
| Intermediate System-to-Intermediate System (IS-IS)               | i           | 115                      |
| Routing Information Protocol (RIP)                               | R           | 120                      |
| Exterior Gateway Protocol (EGP)                                  | E           | 140                      |
| On Demand Routing (ODR)                                          | o           | 160                      |
| External EIGRP                                                   | EX          | 170                      |
| Internal BGP                                                     | B (iBGP)    | 200                      |
| Unknown                                                          | *           | 255 (невозможен маршрут) |

