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
    assert group.order([("a", 3), ("b", 3)]) == 2


def test_subgroups():
    group = AbstractGroup()
    assert len(group.enumerate_subgroups()) == 12
    for each_group in group.enumerate_subgroups():
        assert [] in each_group.enumerate()


def exists_test_normal_subgroups():
    group = AbstractGroup()
    counter = 0
    for each_subgroup in group.enumerate_subgroups():
        if group.is_normal_subgroup(each_subgroup):
            counter += 1

    assert counter == 4


def test_inverse():
    group = AbstractGroup()
    for each_elm in group.enumerate():
        print(each_elm)
        assert group.normalize(group.multiply(group.inverse(each_elm), each_elm)) == []


def test_pow():
    group = AbstractGroup()

    assert group.pow([("a", 0)], 0) == []
    assert group.pow([("a", 1)], 0) == []
    assert group.pow([("a", 2)], 1) == []
    assert group.pow([("b", 8)], 1) == []

    assert group.pow([("b", 1)], 1) == [("b", 1)]
    assert group.pow([("b", 3)], 1) == [("b", 3)]
    assert group.pow([("b", 1)], 2) == [("b", 2)]
    assert group.pow([("b", 2)], 2) == [("b", 4)]
    assert group.pow([("b", 2)], 5) == [("b", 2)]


def test_contains():
    group = AbstractGroup()
    for each_elm in group.enumerate():
        assert group.contains(each_elm)


def test_conjugacy_classes():
    group = AbstractGroup()
    assert len(group.enumerate_conjugacy_classes()) == 7
