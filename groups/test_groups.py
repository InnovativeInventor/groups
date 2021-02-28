from groups.groups import AbstractGroup


def test_combine_rules_1():
    test_case = [("a", 4), ("a", 4), ("b", 3), ("b", 1)]

    group = AbstractGroup()
    assert group._combine_like_terms(test_case) == [("a", 8), ("b", 4)]


def test_combine_rules_null():
    group = AbstractGroup()
    assert group._combine_like_terms([]) == []


def test_normalize_group():
    test_case = [("a", 4), ("a", 4), ("b", 1), ("a", 1), ("b", 1)]

    group = AbstractGroup()
    assert group.normalize(test_case) == [("a", 1)]


def test_normalize_group_1():
    test_case = [("a", 1), ("b", 3), ("a", 1)]

    group = AbstractGroup()
    assert group.normalize(test_case) == [("b", 5)]


def test_enmuerate():
    group = AbstractGroup()
    assert group.enumerate()

def test_order_a_b():
    group = AbstractGroup()
    assert group.order([("a", 1)]) == 2
    assert group.order([("b", 1)]) == 8