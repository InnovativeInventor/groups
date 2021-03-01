from groups import AbstractGroup

if __name__ == "__main__":
    group = AbstractGroup()  # default group

    # Enumerate all elements
    elements = group.enumerate()
    print(f"Listing elements ({len(elements)})")
    for each_elm in elements:
        print(f"{group.format(each_elm)} has order {group.order(each_elm)}")
    print("Order of the entire group:", len(elements))

    # Enumerate subgroups
    subgroups = group.enumerate_subgroups()
    print("\nEnumerating subgroups:\n")
    for each_subgroup in subgroups:
        for each_elm in each_subgroup.enumerate():
            print(group.format(each_elm), end = ", ")
        print(f"Order: {len(each_subgroup.elements)}\n")

    # Enumerating normal subgroups
    print("\nEnumerating normal subgroups:\n")
    for each_subgroup in subgroups:
        if group.is_normal_subgroup(each_subgroup):
            for each_elm in each_subgroup.enumerate():
                print(group.format(each_elm), end = ", ")
            print(f"Order: {len(each_subgroup.elements)}\n")
