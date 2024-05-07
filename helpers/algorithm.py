import re
from helpers.mf_struct import parse_MF_struct

def get_gvs(sigma_vector):
    """ Returns list of grouping variables in query """
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
    """ Returns aggregate functions relevant to the given grouping variable """
    aggregate_funcs = []
    for f in fVector:
        if f[:len(gv)] == gv:
            aggregate_funcs.append(f)
    if any('avg' in func for func in aggregate_funcs):
        # If any of the aggregate_functions are avg
        # sum_func = gv + '_aux_sum_quant'
        # count_func = gv + '_aux_count_quant'
        # aggregate_funcs.append(sum_func)
        # aggregate_funcs.append(count_func)
        if not any('sum' in func for func in aggregate_funcs):
            # Add aggregate func to track sum
            sum_func = gv + '_sum_quant'
            aggregate_funcs.append(sum_func)
        if not any('count' in func for func in aggregate_funcs):
            # Add aggregate func to track count
            count_func = gv + '_count_quant'
            aggregate_funcs.append(count_func)
    return aggregate_funcs

def produce_algorithm(input_file = None):

    # Produce mf-structure
    mf_structure = parse_MF_struct(input_file)

    output = f"""
    mf_structure = {mf_structure}

    # Create instance of H_Table
    h_table = H(len(mf_structure['groupAttributes']), len(mf_structure['fVector']))

    for entry, (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(mf_structure['numGV']):
    """

    grouping_variables = get_gvs(mf_structure['predicates'])

    for j in range(len(mf_structure['predicates'])):
        # Each iteration of j aggregates one group (identified by gv)

        current_gv = grouping_variables[j]
        aggregate_funcs = find_gv_aggregates(current_gv, mf_structure['fVector'])

        # Get grouping attributes from predicate vector
        gv, grouping_attributes, conditions = parse_predicates(mf_structure['predicates'][j], mf_structure['groupAttributes'])
        ga = ','.join(grouping_attributes)

        def_cond = f"""if ({ga}) in h_table.table"""
        if bool(conditions):
            # Additional conditions exist
            def_cond += " and "
            str_conditions = " and ".join(conditions)
            def_cond += str_conditions

        output += f"""
            if i == {j}:
                aggregate_funcs = {aggregate_funcs}
                {def_cond}:
                    avg_aggr = None
                    for func in aggregate_funcs:
                        if 'avg' in func:
                            avg_aggr = func
                        else:
                            h_table.update(({ga}),func,quant,{gv})
                    if avg_aggr != None:
                        h_table.update(({ga}),avg_aggr,quant,{gv})
                        
                else:
                    cols = mf_structure['fVector'].copy()
                    for func in aggregate_funcs:
                        if func not in cols:
                            cols.append(func)
                    h_table.insert(({ga}), cols)
        """
    return output

