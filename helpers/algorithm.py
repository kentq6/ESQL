from helpers.mf_struct import parse_MF_struct

def parse_predicates(sigmaVector):

    # Set of grouping variables
    grouping_attributes = set()

    # Dictionary of predicates where key:GV and value:list(tuple)
    # Tuple structure: (attribute, value)
    predicates = {}

    for pred_set in sigmaVector:
        # pred_list = x.split(',').strip()
        for pred in pred_set:
            tmp = [str.strip(x) for x in pred.split("=")]
            b = tmp[0].split(".")

            # Identify grouping attributes
            gv = b[0]
            if b[1] == tmp[1]:
                grouping_attributes.append(b[1])
            else:
                # Parse predicates and store in dict as  sets of tuples
                if gv in predicates:
                    predicates[gv].extend([(b[1],tmp[1])])
                else:
                    predicates[gv] = [(b[1],tmp[1])]

            af = (b[1],tmp[1])
            if gv in predicates:
                predicates[gv].extend([af])
            else:
                predicates[gv] = [af]

    return grouping_attributes, predicates

def produce_algorithm(input_file = None):

    # Produce mf-structure
    mf_structure = parse_MF_struct(input_file)
    n = mf_structure['numGV']

    # Get grouping attributes from predicate vector
    grouping_attributes, predicates = parse_predicates(mf_structure['predicates'])
    ga = tuple(grouping_attributes)

    output = f"""
    mf_structure = parse_MF_struct(input_file)
    grouping_attributes, predicates = parse_predicates(mf_structure['predicates'])
    len_GA = len(grouping_attributes)
    len_predicates = len(predicates)

    h_table = H(len_GA, len_predicates)

    for (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range({n}):
            curr_gv = mf_structure['groupAttributes'][i]
    """

    if bool(predicates):
        # Predicates exist
        output += f"""
            if ({ga}) in h_table"""
        temp = ""
        for n in range(len(predicates)):
            if n < len(predicates) - 1:
                temp += " and "
            

    else:
        output += f"""
            if ({ga}) in h_table:
                h_table.update({ga},mf_structure['fVector'][{i}])
            else:
                htable.insert({ga})
        """

    return output

