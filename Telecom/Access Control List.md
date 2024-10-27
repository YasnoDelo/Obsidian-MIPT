[[Router]] technology, that allows identifying different types of traffic and taking different actions with them

### Ability
1) Filtration (drop/pass)
2) Prioritisation (QoS)
3) Translation (NAT/PAT)

### Main info
1) Set up on the [[Interface|interface]], don't work else
2) **==Ordered==** list of commands (condition -> action{`permit` or `deny`})
3) Checks until the first match
4) Direction influences processing
5) Works independently on each [[Interface|interface]]
6) Default action if didn't match anything - `deny all`

### Types
#### 1st categorisation

| Type              | Description                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------ |
| Standart/Basic    | [[IPv4#^082ef4\|Source IP]] check                                                          |
| Advanced/Extended | [[IPv4#^082ef4\|Source IP]], [[IPv4#^082ef4\|destination IP]], source/destination [[Port]] |
#### 2nd categorisation

| Type     | Description                                                                                |
| -------- | ------------------------------------------------------------------------------------------ |
| Numbered | Just numbered [[Access Control List\|ACL]] lists                                           |
| Named    | [[Access Control List\|ACL]] lists named for a high level of comfort during implementation |

### List structure

ACL ___ name/number ___

| line    | Condition | Action  |
| ------- | --------- | ------- |
| xxx     | yyy       | zzz     |
| qqq     | www       | eee     |
| $\dots$ | $\dots$   | $\dots$ |
| last    | `any`     | `deny`  |
### Example

1) ACL 12

| line | Condition | Action   |
| ---- | --------- | -------- |
| 1    | `any`     | `permit` |

2) ACL 14

| line | Condition   | Action |
| ---- | ----------- | ------ |
| 1    | `source IP` | `deny` |

### Wildcard bits
As inverted mask. Interested bits are in the places, there lie 0's. There are 1's - places doesn't matter
