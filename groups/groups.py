#!/usr/bin/env python3
from typing import List, Tuple, Dict
import itertools
import copy
from pydantic import BaseModel
import collections


class AbstractGroupDef:
    """
    Finite groups represented as generators and rewrite rules.
    """

    def __init__(
        self,
        generators: Dict[str, int] = {("a", 1): 2, ("b", 1): 8},
        rewrite: List[Tuple[Tuple[str, int]]] = {
            (("b", 1), ("a", 1)): (("a", 1), ("b", 7))
        },
        sub=False,
    ):
        """
        Generators are a list of tuples of some form:
        [("a", 2), ("b", 8)]
        Rewrite rules are for rewriting/reducing expressions.
        """
        self.generators = generators
        self.rewrite = rewrite
        self.elements = []
        self.sub = sub

        self.ordering = {}  # might want to make this an arg
        for count, key in enumerate(self.generators.keys()):
            if count == 0:
                prev_key = key[0]
            else:
                self.ordering[prev_key] = key[0]

    def multiply(
        self, a: List[Tuple[str, int]], b: List[Tuple[str, int]]
    ) -> List[Tuple[str, int]]:
        """
        The binary operator equipped with the group
        """
        term = copy.deepcopy(a)
        term.extend(b)
        return self.normalize(term)

    def pow(self, term: List[Tuple[str, int]], power: int) -> List[Tuple[str, int]]:
        orig_term = copy.deepcopy(term)

        if power == 0:
            return []
        elif power == 1:
            return self.normalize(term)

        for i in range(1, power):
            term = self.normalize(self.multiply(copy.deepcopy(orig_term), term))

        return self.normalize(term)

    def normalize(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Recursively apply the rewrite rules until it is in a normal form.
        """
        ordered = False
        while len(term) > len(self.generators) or not ordered:
            expanded_term = self._expand_terms(term)

            new_term = []
            ordered = True
            for count, (generator, power) in enumerate(expanded_term):
                if count == 0:
                    prev_generator = generator
                    new_term.append((generator, power))
                else:
                    if (generator == prev_generator) or (
                        prev_generator in self.ordering
                        and generator == self.ordering[prev_generator]
                    ):
                        new_term.append((generator, power))  # all is well
                    else:
                        ordered = False
                        substitue_term = self.rewrite[
                            ((prev_generator, 1), (generator, 1))
                        ]

                        new_term.pop()  # remove last elm
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
            new_term.extend([(generator, 1)] * power)

        return new_term

    def _combine_like_terms(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Iteratively combines like terms. Don't ask me why this is so stateful and poorly written.
        """
        new_term = []
        count = 0

        for generator, power in term:
            if count > 0:
                if generator == prev_generator:  # like term discovered
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

    def _get_generator_order(self, generator):
        for each_generator, power in self.generators.keys():
            if generator == each_generator:
                return power * self.generators[(each_generator, power)]

    def _reduce_term_exp(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Reduces the term exponent to be most simple/smallest possible.
        """
        new_term = []
        for generator, power in term:
            if self._get_generator_order(generator) != 0:
                if power % self._get_generator_order(generator) != 0:
                    new_term.append(
                        (generator, power % self._get_generator_order(generator))
                    )
            else:  # only if generator's order is not known
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
            if power != 0 and power % self._get_generator_order(generator) != 0:
                return False
        return True

    def format(self, term: List[Tuple[str, int]], latex=False):
        if len(term) == 0:
            return "e"

        representation = ""
        for generator, power in term:
            if power:
                if latex:
                    representation += f"{generator}^\{{power}\}"
                else:
                    representation += f"{generator}^{power}"

        return representation

    def _close_group(self):
        """
        Tries to get the rest of the elements in the group by one round of closure (i.e. multiplying everything together)
        """
        for left_elm, right_elm in itertools.product(self.elements, self.elements):
            if (not self.check_identity(left_elm)) and (
                not self.check_identity(right_elm)
            ):
                new_elm = self.normalize(
                    self.normalize(
                        self.multiply(
                            self.normalize(left_elm), self.normalize(right_elm)
                        )
                    )
                )  # should not need so much wrapping, TODO: test and remove

                for each_elm in self.elements:
                    if self.compare(new_elm, each_elm):
                        break
                else:
                    self.elements.append(self.normalize(new_elm))


class AbstractGroup(AbstractGroupDef):
    """
    Higher order group functions
    """

    def __eq__(self, other) -> bool:
        if len(self.generators.keys()) != len(self.generators.keys()):
            return False

        for each_key in self.generators.keys():
            try:
                if self.generators[each_key] != other.generators[each_key]:
                    return False
            except:
                return False

        for each_key in self.rewrite.keys():
            try:
                if self.rewrite[each_key] != other.rewrite[each_key]:
                    return False
            except:
                return False

        if len(other.enumerate()) != len(self.enumerate()):
            return False

        for each_elm in self.enumerate():
            if not other.contains(each_elm):
                return False

        return True

    def order(self, term: List[Tuple[str, int]]) -> int:
        """
        Find the order of an element in a group
        """
        starting_term = self.normalize(copy.deepcopy(term))

        order = 1
        current_term = self.normalize(self.pow(copy.deepcopy(starting_term), 2))
        while not self.compare(current_term, starting_term):
            order += 1
            current_term = self.normalize(
                self.multiply(current_term, copy.deepcopy(starting_term))
            )

        return order

    def inverse(self, term: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Finds the inverse of an element
        """
        order = self.order(term)
        return self.normalize(self.pow(term, order - 1))

    def enumerate(self, remove_dups=True) -> List[List[Tuple[str, int]]]:
        """
        Enumerate all elements. Returns a list of all elements.
        """
        prev_size = -1

        self.elements.append([])  # identity!
        if not self.sub:  # get the full group
            for generator, power in self.generators.keys():
                self.elements.append([(generator, power)])

        while prev_size != len(self.elements):
            prev_size = len(self.elements)
            self._close_group()
        self._close_group()

        if remove_dups:
            self.remove_dups()

        return self.elements

    def contains(self, term: List[Tuple[str, int]], cache=True) -> bool:
        """
        Membership function equipped with the group/set.
        """
        if cache:
            for each_elm in self.elements:  # TODO: speedup and prefer enumerate
                if self.compare(each_elm, term):
                    return True
        else:
            for each_elm in self.enumerate():
                if self.compare(each_elm, term):
                    return True

        return False

    def remove_dups(self):
        """
        Remove dups in element list
        """
        dups_exist = True
        while dups_exist:
            dups_exist = False
            for i, each_term in enumerate(self.elements):
                for j, other_term in enumerate(self.elements):
                    if i != j and self.compare(each_term, other_term):
                        dups_exist = True
                        break

            if dups_exist:
                del self.elements[i]
                break

    def enumerate_subgroups(self) -> list:
        """
        Enumerates all subgroups, including the identity subgroup
        """
        subgroups = []
        for each_elm in self.enumerate():
            normal_elm = self.normalize(each_elm)
            # seen = False
            # for each_subgroup in subgroups: # check if already seen
            #     for each_subgroup_elm in each_subgroup.enumerate():
            #         if self.compare(normal_elm, self.normalize(each_subgroup_elm)):
            #             seen = True
            #     # if seen:
            #     #     break

            # if seen:
            #     continue

            # Construct subgroup
            subgroup = AbstractGroup(
                copy.deepcopy(self.generators), copy.deepcopy(self.rewrite), sub=True
            )
            subgroup.elements = [normal_elm]

            for each_subgroup in subgroups:
                if each_subgroup == subgroup:
                    break
            else:
                subgroups.append(subgroup)
            # breakpoint()

        return subgroups

    def enumerate_conjugacy_classes(self) -> list:
        """
        Enumerates all distinct conjugacy classes
        """
        conjugacy_classes = []
        self.enumerate()
        for each_elm in self.elements:
            conjugacy_class = []
            for other_elm in self.elements:
                seen = False
                unique = True
                conjugated_elm = self.conjugate(each_elm, other_elm)

                # Check if we've seen the elm before
                for each_seen_term in itertools.chain.from_iterable(conjugacy_classes):
                    if self.compare(conjugated_elm, each_seen_term):
                        seen = True
                        break
                else:
                    for each_seen_term in conjugacy_class:  # maybe combine this
                        if self.compare(conjugated_elm, each_seen_term):
                            unique = False
                            break

                if seen:
                    break
                elif unique:
                    conjugacy_class.append(conjugated_elm)

            if seen:  # since conjugacy classes partition
                continue
            else:
                conjugacy_classes.append(conjugacy_class)

        return conjugacy_classes

    def conjugate(
        self, a: List[Tuple[str, int]], b: List[Tuple[str, int]]
    ) -> List[Tuple[str, int]]:
        """
        Conjugates a by b. Returns bab^-1.
        """
        return self.normalize(self.multiply(b, self.multiply(a, self.inverse(b))))

    def is_normal_subgroup(self, subgroup) -> bool:
        """
        Calculates if subgroup is normal. subgroup should be an instance of AbstractGroup.
        """
        if not (subgroup.sub is True and self.sub is False):
            raise ValueError(
                "You need to call is_normal_subgroup on a group and pass a subgroup!"
            )

        normal = True
        for each_elm in subgroup.enumerate():
            for other_elm in self.enumerate():
                if subgroup.contains(self.conjugate(each_elm, other_elm)) is False:
                    normal = False
                    break

            if normal is False:
                break

        return normal
