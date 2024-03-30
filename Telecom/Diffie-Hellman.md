Encryption [[Protocol|protocol]], uses [[Symmetrical encryption protocols|symmetrical]] method of cryptography with [[Encription key|one security key]]

#Algorythm
The operation of the algorithm can be described as follows:
Suppose there are two subscribers: Alice and Bob. Both subscribers know some two numbers $g$ and $p$, which are not secret and can be known also to other interested parties. In order to create a secret key unknown to no one else, both subscribers generate large random numbers: Alice the number ''$a$'', Bob the number ''$b$''. Alice then calculates the remainder of the division:
$$A=g^a \bmod p$$
and sends it to Bob, and Bob calculates the remainder of the division:
$$B=g^b \bmod p$$
and passes it to Alice. It is assumed that an attacker can get both of these values, but not modify them

In the second step, Alice calculates a value based on the ''$a$'' she has and the ''$B$'' received over the network:
$$B^a\bmod p=g^{ab}\bmod p$$
Bob calculates a value based on the ''$b$'' he has and the ''$A$'' received over the network:
$$A^b\bmod p=g^{ab}\bmod p$$
Alice and Bob got the same number:
$$K=g^{ab}\bmod p$$
That's what they can use as their [[Encription key|secret key]].