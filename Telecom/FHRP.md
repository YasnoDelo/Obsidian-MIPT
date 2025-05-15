**First Hop Redundancy Protocol**
(Это семейство протоколов, чуть-чуть по разному решающих одну задачу)

Problem statement:
Single point of failure (единая точка отказа) - отрезает доступ к участку сети в случае отказа.

Можно добавить дополнительных избыточных устройств и каналов связи + некоторые протоколы, учитывающие избыточность.
Добавлять можно, например, роутеры и свичи, [[WAN]], [[LAN]] каналы. Для свичей учитывает избыточность [[STP]]. Для роутеров помогают протоколы динамической маршрутизации и [[FHRP]]

If [[Default gateway|default gateway]] is down, [[PC]] will not have any network. That's why we need several [[Default gateway|default gateways]]. There we will use [[FHRP]].

We can use [[FHRP]] just then clients are connected to network via [[L2]]. 

Some realisation: 
1) [[HSRP]] - Hot Standby Router Protocol
#Comment
	1. One active router and all other - standby 
	2. Subnet balancing (via engineer's hands, not real balancing)
	3. Cisco's one
2) [[VRRP]] - Virtual Router Redundant Protocol
#Comment
	1. One active router and all other - standby 
	2. Subnet balancing (via engineer's hands, not real balancing)
	3. IETF's one
1) [[GLBP]] - Gateway Load Balance Protocol
#Comment
	1. One active router and all other - standby 
	2. Host balancing (real balancing)
	3. Cisco's one

### Main principle
1) There is virtual IP-address of default gateway, which users are using.
2) For [[Router|routers]] synchronising, they (routers) send [[FHRP]] messages.
3) If active [[Router|router]] becomes physically disabled, there are elections of new active one.

