## Groups
Representing certain kinds of finite groups in terms of generators and rewrite rules. 
Work in progress. 
This is probably not the best way to represent groups, but whatever.
Contributions are welcome.
 
## Example (D_16)
The group `D_16` can be represented like so
```
a^2 = e
b^8 = e
ba = ab^7
```

``` python
from groups import AbstractGroup
group = AbstractGroup({"a": 2, "b": 8}, {(("b", 1), ("a", 1)): (("a", 1), ("b", 7))}) # default group
```
where each element is represented as a list of tuples containing the generator, followed by the power of the generator.

To enumerate all the elements in the group you can then do
``` python
group.enumerate()
```

To multiply particular elements together you can do
``` python
group.multiply(term_1, term_2)
```

To normalize/simplify an element to its simplest form you can do
``` python
group.normalize(term_1)
```

To get the inverse of an element, you can do
``` python
group.inverse(term_1)
```

Voila -- some basic group stuff! More basic group operations are used in [`examples/d16.py`](/examples/d16.py)
