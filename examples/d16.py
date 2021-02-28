from groups import AbstractGroup

if __name__ == "__main__":
    group = AbstractGroup({"a": 2, "b": 8}, {(("b", 1), ("a", 1)): (("a", 1), ("b", 7))}) # default group

    # Enumerate all elements
    elements = group.enumerate()
    print(f"Listing elements ({len(elements)})")
    for each_elm in elements:
        print(f"{group.format(each_elm)} has order {group.order(each_elm)}")
    print("Order of the entire group:", len(elements))
