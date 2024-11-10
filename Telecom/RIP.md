[[IGP]], [[DP]]

Uses [[UDP]] 520-521

It is one of the oldest routing protocols used to exchange routing information between routers within the same autonomous system. It belongs to the class of protocols using a distance metric, where the main metric is the number of hops ([[IPv4#^082ef4|hop]] count) to the target network.

### Metric
Amount of [[IPv4|L3 hops]]

Available destination is `[1,15]`

Unavailable destination is `16` 

### Database
Each [[Router|router]] has it's own

### Timers
Are basic of [[RIP]]

#### Update timer
Frequency of protocol update (30 sec)

#### Invalid timer
If a route update is not received before this timer expires, the route will be marked as Invalid, i.e. with a metric of 16. The default timer is 180 seconds

#### Holddown timer

^3a9c36

After the timer expires, the distance to the route becomes 16 (180 sec). We need it for announcement to neighbours. 

#### Flush timer
The default timer is 240 seconds, 60 more than the ==invalid timer==. If this timer expires before the route updates arrive, the route will be **removed** from the routing table. If a route is removed from the routing table, then the other timers that corresponded to it are also removed

That's why [[RIP]] is slow - because far routers get to know about router removed from available ones



### Building a routing table
1) **Creating a ==minimal table==**. Initially, the TCP/IP stack software automatically creates a minimal routing table on each router that considers only directly connected networks.
2) **Broadcasting the ==Minimum Table== to Neighbors**. After initialization, each router begins sending [[RIP]] messages to its neighbors, which contain its ==minimum table==. [[RIP]] messages are transmitted in [[UDP]] datagrams and include two parameters for each network: its [[IPv4#^69527c|IP address]] and its distance from the router that sent the message.
3) **Receiving [[RIP]] messages from neighbors and processing the received information**. After receiving similar messages from neighbors, the router increases each received metric field by one and remembers through which port and from which router the new information was received (the address of this router will become the address of the next router if this entry is added to the routing table). The [[RIP]] protocol replaces an entry about a network only if the new information has a better metric than the existing one. As a result, only one entry remains in the routing table about each network; if there are several entries that are equivalent in terms of paths to the same network, then the entry that arrived to the router first still remains in the table. There is an exception to this rule: if the worse information about a network came from the same router, on the basis of whose message the entry was created, then the worse information replaces the better one.
4) **Sending a new table to neighbors**. Each router sends a new [[RIP]] message to all its neighbors. In this message, it places data on all networks known to it: both directly connected and remote ones, which the router learned about from [[RIP]] messages.
5) **Receiving [[RIP]] messages from neighbors and processing the received information.** Step 5 repeats step 3 - routers receive [[RIP]] messages, process the information they contain, and adjust their routing tables based on it.

### Fighting loops
1) **Split horizon** — information about updating the route database is not sent **back** to the used interfaces
2) **Triggered update** — updates are sent immediately when a route changes, instead of waiting for the Update timer to expire. 
3) **Route poisoning** — this is the forced removal of a route and its transfer to a hold state, used to combat route loops. 
4) **Poison reverse** — The route is marked as unreachable, i.e. with a metric of 16, and sent in updates.
5) Freezing changes - while [[RIP#^3a9c36|holddown timer]] isn't expired, router can't update info about this [[Prefix|prefix]]

### RIPv1
Classful routing protocol in [[IPv4]]

### RIPv2
Classless routing protocol in [[IPv4]]

Uses masks
Supports [[VLSM]]
### RIPng
For [[IPv6]]