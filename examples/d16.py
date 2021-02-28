from groups import AbstractGroup

if __name__ == "__main__":
    group = AbstractGroup({"a": 2, "b": 8}, {(("b", 1), ("a", 1)): (("a", 1), ("b", 7))}) # default group

    # Enumerate all elements
    elements = group.enumerate()
    print(f"Listing elements ({len(elements)})")
    for each_elm in elements:
        print(f"{group.format(each_elm)} has order {group.order(each_elm)}")
    print("Order of the entire group:", len(elements))

    # Enumerate subgroups
    subgroups = group.enumerate_subgroups()
    print("\nEnumerating subgroups")
    for each_subgroup in subgroups:
        print(each_subgroup.enumerate())

    # Enumerating normal subgroups
    print("\nEnumerating normal subgroups")
    for each_subgroup in subgroups:
        if group.is_normal_subgroup(each_subgroup):
            print(each_subgroup.enumerate())
