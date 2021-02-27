#!/usr/bin/env python3
from typing import List, Tuple, Dict
import itertools
import copy
from pydantic import BaseModel

class AbstractGroup():
    """
    Finite groups represented as generators and rewrite rules.
    """
    def __init__(self, generators: Dict[str, int] = {"a": 2, "b": 8},
                 rewrite: List[Tuple[Tuple[str, int]]] = {(("b", 1), ("a", 1)): (("a", 1), ("b", 7))}):
        """
        Generators are a list of tuples of some form:
        [("a", 2), ("b", 8)]
        Rewrite rules are for rewriting/reducing expressions.
        """
        self.generators = generators
        self.elm_ordering = list(self.generators.keys())
        self.rewrite = rewrite
        self.elements = []

        self.ordering = {}
        for count, key in enumerate(self.generators.keys()):
            if count == 0:
                prev_key = key
            else:
                self.ordering[prev_key] = key

    def multiply(self, a: List[Tuple[str, int]], b: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        The binary operator equipped with the group
        """
        a.extend(b)
        return a

    def pow(self, term: List[Tuple[str, int]], power: int) -> List[Tuple[str, int]]:
        orig_term = copy.deepcopy(term)

        for i in range(1, power):
            term = self.normalize(self.multiply(orig_term, term))

        return term

    def normalize(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Recursively apply the rewrite rules until it is in a normal form.
        """
        ordered = False
        while (len(term) > len(self.generators) or not ordered):
            expanded_term = self._expand_terms(term)

            new_term = []
            ordered = True
            for count, (generator, power) in enumerate(expanded_term):
                if count == 0:
                    prev_generator = generator
                    new_term.append((generator, power))
                else:
                    if (generator == prev_generator) or (prev_generator in self.ordering and generator == self.ordering[prev_generator]):
                        new_term.append((generator, power)) # all is well
                    else:
                        ordered = False
                        substitue_term = self.rewrite[((prev_generator, 1), (generator, 1))]

                        new_term.pop() # remove last elm
                        new_term.extend(list(substitue_term))

                prev_generator = generator

            term = self._reduce_term_exp(self._combine_like_terms(new_term))

        return term

    def _expand_terms(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Expand terms into powers of one.
        """
        new_term = []
        for generator, power in term:
            new_term.extend([(generator, 1)]*power)

        return new_term

    def _combine_like_terms(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Iteratively combines like terms. Don't ask me why this is so stateful and poorly written.
        """
        new_term = []
        count = 0

        for generator, power in term:
            if count > 0:
                if generator == prev_generator: # like term discovered
                    prev_power += power
                    continue
                else:
                    new_term.append((prev_generator, prev_power))

            prev_index = count
            prev_generator = generator
            prev_power = power
            count += 1
        else:
            if count >= 1:
                new_term.append((prev_generator, prev_power))

        return new_term

    def _reduce_term_exp(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Reduces the term exponent to be most simple/smallest possible.
        """
        new_term = []
        for generator, power in term:
            if self.generators[generator] != 0:
                if power % self.generators[generator] != 0:
                    new_term.append((generator, power % self.generators[generator]))
            else: # only if generator's order is not known
                new_term.append((generator, power))

        return new_term

    def compare(self, a: List[Tuple[str, int]], b: List[Tuple[str, int]]):
        """
        Compare if a and b are equal
        """
        a_normalized = self.normalize(a)
        b_normalized = self.normalize(b)

        if len(a_normalized) != len(b_normalized):
            return False

        for i in range(len(a_normalized)):
            if a_normalized[i] != b_normalized[i]:
                return False

        return True

    def check_identity(self, term: List[Tuple[str, int]]) -> bool:
        """
        Check if a term is equal to the identity
        """
        for generator, power in term:
            if power != 0 and power % self.generators[generator] != 0:
                return False
        return True

    def print(self, term: List[Tuple[str, int]]):
        for generator, power in term:
            if power:
                print(f"{generator}^{power}", end="")
        print()

    def enumerate(self):
        """
        Enumerate all elements
        """
        prev_size = -1
        for generator in self.generators.keys():
            self.elements.append([(generator, 1)])

        while prev_size != len(self.elements):
            prev_size = len(self.elements)
            for left_elm, right_elm in itertools.product(self.elements, self.elements):
                if (not self.check_identity(left_elm)) and (not self.check_identity(right_elm)):
                    new_elm = self.normalize(self.normalize(self.multiply(list(left_elm), list(right_elm))))

                    for each_elm in self.elements:
                        if self.compare(new_elm, each_elm):
                            break
                    else:
                        self.elements.append(new_elm)

        return self.elements
