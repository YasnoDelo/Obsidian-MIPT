R1
```
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
!
interface FastEthernet0/0
 ip address 10.0.15.1 255.255.255.0
 duplex half
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet1/1
 ip address 10.0.13.1 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet2/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet2/1
 ip address 10.0.14.1 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet3/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface Serial4/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/3
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/4
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/5
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/6
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/7
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/3
 no ip address
 shutdown
 serial restart-delay 0
!
router bgp 12345
 bgp log-neighbor-changes
 network 1.1.1.1 mask 255.255.255.255
 redistribute connected route-map Delete
 neighbor LEAF peer-group
 neighbor LEAF remote-as 12345
 neighbor LEAF weight 2000
 neighbor 10.0.13.3 remote-as 12345
 neighbor 10.0.14.4 remote-as 12345
 neighbor 10.0.15.5 peer-group LEAF
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
!
!
no cdp log mismatch duplex
!
route-map Delete permit 10
 match interface Loopback0
!
!
!
control-plane
!
!
!
mgcp profile default
!         
!
!
gatekeeper
 shutdown
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
 transport input all
!
!
end
```

R2
```
interface Loopback0
 ip address 2.2.2.2 255.255.255.255
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet1/1
 no ip address
 shutdown 
 duplex auto
 speed auto
!
interface FastEthernet2/0
 ip address 10.0.23.2 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet2/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/0
 ip address 10.0.24.2 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet3/1
 ip address 10.0.25.2 255.255.255.0
 duplex auto
 speed auto
!
interface Serial4/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/3
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/4
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/5
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/6
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/7
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/0
 no ip address
 shutdown
 serial restart-delay 0
!         
interface Serial5/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/3
 no ip address
 shutdown
 serial restart-delay 0
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
!
!
no cdp log mismatch duplex
!         
!
!
control-plane
!
!
!
mgcp profile default
!
!
!
gatekeeper
 shutdown
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
 transport input all
!
!
end

```

R3
```
interface Loopback0
 ip address 3.3.3.3 255.255.255.255
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet1/1
 ip address 10.0.13.3 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet2/0
 ip address 10.0.23.3 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet2/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface Serial4/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/3
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/4
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/5
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/6
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/7
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/3
 no ip address
 shutdown
 serial restart-delay 0
!
router bgp 12345
 bgp log-neighbor-changes
 redistribute connected route-map Delete
 neighbor 10.0.13.1 remote-as 12345
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
!
!
no cdp log mismatch duplex
!
route-map Delete permit 10
 match interface Loopback0
!
!
!
control-plane
!
!
!
mgcp profile default
!
!
!
gatekeeper
 shutdown
!
!         
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
 transport input all
!
!
end
```

R4
```
interface Loopback0
 ip address 4.4.4.4 255.255.255.255
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex half
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet1/1
 no ip address
 shutdown 
 duplex auto
 speed auto
!
interface FastEthernet2/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet2/1
 ip address 10.0.14.4 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet3/0
 ip address 10.0.24.4 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet3/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface Serial4/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/3
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/4
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/5
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/6
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/7
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/3
 no ip address
 shutdown
 serial restart-delay 0
!
router bgp 12345
 bgp log-neighbor-changes
 redistribute connected route-map Delete
 neighbor 10.0.14.1 remote-as 12345
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
!
!
!
ip prefix-list Delete seq 5 deny 10.0.0.0/8 le 32
ip prefix-list Delete seq 10 permit 0.0.0.0/0 le 32
no cdp log mismatch duplex
!
route-map Delete permit 10
 match ip address prefix-list Delete
 set weight 1000
!
!
!
control-plane
!
!
!
mgcp profile default
!
!
!         
gatekeeper
 shutdown
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
 transport input all
!
!
end
```

R5
```
interface Loopback0
 ip address 5.5.5.5 255.255.255.255
!
interface FastEthernet0/0
 ip address 10.0.15.5 255.255.255.0
 duplex half
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet1/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet2/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet2/1
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet3/1
 ip address 10.0.25.5 255.255.255.0
 duplex auto
 speed auto
!
interface Serial4/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/3
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/4
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/5
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/6
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial4/7
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/0
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/1
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/2
 no ip address
 shutdown
 serial restart-delay 0
!
interface Serial5/3
 no ip address
 shutdown
 serial restart-delay 0
!
router bgp 12345
 bgp log-neighbor-changes
 network 5.5.5.5 mask 255.255.255.255
 neighbor 10.0.15.1 remote-as 12345
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
!
!
no cdp log mismatch duplex
!
!
!
control-plane
!
!
!
mgcp profile default
!
!
!
gatekeeper
 shutdown
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
 transport input all
!
!
end
```