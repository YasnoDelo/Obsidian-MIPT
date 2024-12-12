Link Aggregation Group

Allows us ti unite several physical channels in one logic between two [[Switch|switches]]

### Traffic balancing
#### HASH
$$F(MAC_s, MAC_r, (optional\ IP, UDP\ or\ TCP\ ports))$$
1) EtherChannel (N channels -> calculates HASH for each packet, $HASH\%N$ - number of channel, on which data sends)

