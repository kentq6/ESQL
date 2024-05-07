import re
from helpers.mf_struct import parse_MF_struct

def get_gvs(sigma_vector):
    gvs = []
    for pset in sigma_vector:
        v = pset[0].split('.')
        gvs.append(v[0])
    return gvs

def parse_predicates(sigma: list, default_ga: list):

    # Set of grouping attributes
    grouping_attributes = {}
    # List of conditions
    conditions = []

    for predicate in sigma:
        params = re.split(r'[=\.<>]', predicate)
        gv = params[0]
        # print(str(params))
        if params[1] == params[2]:
            grouping_attributes.add(params[1])
        else:
            this_cond = predicate[len(gv)+1:].replace("=", "==")
            conditions.append(this_cond)
            # print(str(conditions))
    if not grouping_attributes:
        grouping_attributes = default_ga

    return gv, grouping_attributes, conditions

def find_gv_aggregates(gv: str, fVector: list):
    aggregate_funcs = []
    for f in fVector:
        if f[:len(gv)] == gv:
            aggregate_funcs.append(f)
    return aggregate_funcs

def produce_algorithm(input_file = None):

    output = f"""
    mf_structure = parse_MF_struct(input_file)

    # Create instance of H_Table
    h_table = H(len(mf_structure['groupAttributes']), len(mf_structure['fVector']))

    for entry, (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(mf_structure['numGV']):
    """

    # Produce mf-structure
    mf_structure = parse_MF_struct(input_file)
    grouping_variables = get_gvs(mf_structure['predicates'])

    for j in range(len(mf_structure['predicates'])):
        # Each iteration of j aggregates one group (identified by gv)

        current_gv = grouping_variables[j]
        aggregate_funcs = find_gv_aggregates(current_gv, mf_structure['fVector'])

        # Get grouping attributes from predicate vector
        gv, grouping_attributes, conditions = parse_predicates(mf_structure['predicates'][j], mf_structure['groupAttributes'])
        ga = ','.join(grouping_attributes)

        def_cond = f"""if ({ga}) in h_table"""
        if bool(conditions):
            # Additional conditions exist
            def_cond += " and "
            str_conditions = " and ".join(conditions)
            def_cond += str_conditions

        output += f"""
            if i == {j}:
                aggregate_funcs = {aggregate_funcs}
                {def_cond}:
                    for func in aggregate_funcs:
                        h_table.update({ga},func,quant)
                else:
                    h_table.insert({ga})
        """


    return output

