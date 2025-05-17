**Server Load Balancing**

### Defs
1) Server farm - list of servers servers, between which load is balancing
2) Real server - physical server
3) vServer - logical server to which the client is connected (client think, that he is connected to just 1 server)
4) sNAT - reassigning the destination address from a common gateway (balancing tool) to a specific real server (and vice versa) -> reason of lack of productivity


| L3                         | L2                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Has sNAT->less performance | Without sNAT->more performance                                                                                                    |
|                            | Every client has loopback0, for server processing on his vIP (doesn't discard). MAC dest - address of physical server's interface |
|                            | In one L2-segment                                                                                                                 |
