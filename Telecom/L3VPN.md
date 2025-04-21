Provider's realisation of [[Tunnel|tunnels]] (better than usual client-client implementation: more available for scale, there is no reason no make connection beetween new point and ALL old ones)
![[L3VPN.png]]
$A = \sum \limits_{i=1}^nA_i$ - First subnet (any addresses, may cross with $B$)

$B = \sum \limits_{i=1}^nB_i$ - Second subnet (any addresses, may cross with $A$)

### With [[MPLS]]: 
Structure of header:

| $Eth$ | $Label_{out}$   | $Label_{in}$                          | $IP_n$                  | ... |
| ----- | --------------- | ------------------------------------- | ----------------------- | --- |
|       |                 | Need them to recognise client: A or B | Can be same for A and B | ... |
|       | Transport label | Service label                         | IP address              | ... |
|       | LDP             | BGP (or VPNv4 or VPNv6)               |                         | ... |

![[L3_VPN_scheme.png]]
$$CE - client's \quad edge$$
$$PE - provider's \quad edge, \quad P = provider$$

### Address VPNv4:

| Route distinguish (RD)                                                                                            | IP address |
| ----------------------------------------------------------------------------------------------------------------- | ---------- |
| 64 bits, is needed to distinguish between users with possibly identical IP addresses. Each [[VRF]] has own number | 32 bits    |
There is one more attribute like RD: route target
#### **Route Target (RT)**

- **Purpose**:  
    Controls **import/export of routes between VRFs** (Virtual Routing and Forwarding). Determines which routes will be available in a particular client's VRF.
    
- **How it works**:
    
    - RT is added to the route as an **extended BGP community** (Extended Community).
        
    - The PE router **exports** routes with the specified RT and **imports** routes that have the corresponding RT.
        
- **Example**:
    
    - Client A uses RT `100:100` to export its routes.
        
    - Client B uses RT `100:200`.
        
    - Client A's PE router imports only routes with RT `100:100`.

### Main Differences

| Параметр                     | Route Distinguisher (RD)                       | Route Target (RT)                               |
| ---------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| **Purpose**                  | Uniq prefixes in BGP VPNv4                     | Controle import/export in VRF                   |
| **Format**                   | `ASN:NN` or `IP:NN` (for example, `65000:100`) | Extended community BGP (for example, `100:100`) |
| **Where is used**            | While conversion IPv4 → VPNv4                  | When filtering routes between VRFs              |
| **Example of configuration** | `rd 65000:100`                                 | `route-target export/import 100:100`            |
