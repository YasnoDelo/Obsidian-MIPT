(virtual local area network)

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
