from collections import defaultdict
from tabulate import tabulate

def mf_query(phi_args):
    # Unpack the Φ operator arguments
    grouping_attrs, selections, aggregates, relations = phi_args

    # Initialize the H Table
    h_table = defaultdict(lambda: defaultdict(list))

    # Process each group
    for group_key, group in group_by(relations, grouping_attrs):
        # Step 1: Compute F0 (aggregates of the full group)
        f0 = compute_aggregates(group, aggregates[0])
        h_table[group_key][None] = f0

        # Step 2: Compute selections and aggregates for each Ri
        for i, (selection, aggs) in enumerate(zip(selections, aggregates[1:]), start=1):
            ri = apply_selection(group, selection)
            fi = compute_aggregates(ri, aggs)
            h_table[group_key][i] = fi

    # Convert the H Table to a list of rows
    rows = []
    headers = ["Grouping Attributes"] + [f"R{i}" for i in range(len(selections) + 1)]
    rows.append(headers)

    for group_key, group_data in sorted(h_table.items()):
        row = [str(group_key)]
        for i in range(len(selections) + 1):
            row.append(str(group_data[i]))
        rows.append(row)

    # Print the H Table using tabulate
    print(tabulate(rows, headers="firstrow", tablefmt="grid"))

# Helper functions
def group_by(relations, grouping_attrs):
    groups = defaultdict(list)
    for relation in relations:
        group_key = tuple(relation[attr] for attr in grouping_attrs)
        groups[group_key].append(relation)
    return groups.items()

def compute_aggregates(group, aggs):
    return [compute_aggregate(group, agg) for agg in aggs]

def compute_aggregate(group, agg):
    # Implement aggregate functions like sum, max, min, etc.
    pass

def apply_selection(group, selection):
    # Apply the selection condition to the group
    return [relation for relation in group if selection(relation)]
