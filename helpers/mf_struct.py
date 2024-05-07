import re

def list_of_strings(args: str):
    """ Returns list of strings separated by comma """
    return list(map(str.strip, args.split(',')))

def extract_sets(args: str):
    """ Returns list of predicates, grouped by grouping variable """
    predicates = []
    res = re.findall(r'\{.*?\}', args)
    for s in res:
        set_str = s.replace('{','').replace('}','').split(',')
        predicates.append(list(set_str))
    # print(str(predicates))
    return predicates

def parse_MF_struct(input_file = None):
    """ 
    Produces MF struct detailing the 6 arguments needed for phi operator

    Parameters
    ----------
    input_file : str, optional
        Path to input file. If not provided, function will request user input.
    
    Returns
    -------
    dict representing an MF struct
    """

    mf_structure = dict()

    if input_file == None:
        # Manually collect arguments if input file not specified
        mf_structure['select'] = input("SELECTION ATTRIBUTES: ")
        mf_structure['numGV'] = int(input("NUMBER OF GROUPING VARIABLES: "))
        mf_structure['groupAttributes'] = list_of_strings(input("GROUPING ATTRIBUTES: "))
        mf_structure['fVector'] = list_of_strings(input("AGGREGATE FUNCTIONS: "))
        mf_structure['predicates'] = extract_sets(input("PREDICATES FOR GVs: "))
        mf_structure['having'] = input("HAVING: ")

    else: 
        # Read arguments from input file
        f = open(input_file, 'r').readlines()

        for line in f:
            current_input = line.split(": ")
            field = current_input[0]
            args = current_input[1]

            # S = List of projected attributes for the query output
            if field == 'SELECTION ATTRIBUTES':
                mf_structure['select'] = args.strip()

            # n = Number of grouping variables
            elif field == 'NUMBER OF GROUPING VARIABLES':
                mf_structure['numGV'] = int(args)

            # V = List of grouping attributes
            elif field == 'GROUPING ATTRIBUTES':
                # list[str]
                mf_structure['groupAttributes'] = list_of_strings(args)

            # [F] = {F0, ... , Fn} List of sets of aggregate functions
            elif field == 'AGGREGATE FUNCTIONS':
                # list[str]
                mf_structure['fVector'] = list_of_strings(args)

            # [σ] = {σ0, ... , σn} List of predicates to define ranges for GVs
            elif field == 'PREDICATES FOR GVs':
                # list[set{str}]
                mf_structure['predicates'] = extract_sets(args)


            # G = Predicate for having clause
            elif field == "HAVING":
                mf_structure['having'] = args.strip()
                
    return mf_structure

def parse_having(having_str: str):
    """ 
    Produces list of parsed conditions in HAVING clause

    Parameters
    ----------
    having_str : str
        Direct input of HAVING clause
    
    Returns
    -------
    res : list[list(str)]
        Each nested list represents one condition within HAVING, with the format [param1, param2, operator]
    """
    res = []
    having_conditions = having_str.split(" and ")
    for cond in having_conditions:
        if ">" in cond:
            params = list(map(str.strip, cond.split(">")))
            params.extend([">"])
            res.append(params)
        elif "<" in cond:
            params = list(map(str.strip, cond.split("<")))
            params.extend(["<"])
            res.append(params)
        elif "=" in cond:
            params = list(map(str.strip, cond.split("=")))
            params.extend(["=="])
            res.append(params)
        elif "!=" in cond:
            params = list(map(str.strip, cond.split("!=")))
            params.extend(["!="])
            res.append(params)
    return res

def apply_having(having_str: str, info: dict):
    bools = []
    having_conditions = parse_having(having_str)
    for params in having_conditions:
        if  (params[2] == ">" and info[params[0]] > info[params[1]]) or \
            (params[2] == "<" and info[params[0]] < info[params[1]]) or \
            (params[2] == "==" and info[params[0]] == info[params[1]]) or \
            (params[2] == "!=" and info[params[0]] != info[params[1]]):
            bools.append(True)
        else:
            bools.append(False)
    return all(bools)

# if "__main__" == __name__:
#     parse_MF_struct("../input/input.txt")
    