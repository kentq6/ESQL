
def list_of_strings(args: str):
    """ Returns list of strings separated by comma """
    return list(map(str.strip, args.split(',')))

def extract_set(args: str):
    """ Returns set of strings from an argument enclosed in brackets {} """
    args = args.replace('{', '').replace('}', '')
    return set(args.split(','))

def parse_MF_struct(input_file: str):
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
        predicate_input = input("PREDICATES FOR GVs: ")
        mf_structure['predicates'] = list(map(extract_set, predicate_input.split()))
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
                mf_structure['predicates'] = list(map(extract_set, args.split()))
                print(mf_structure['predicates'])

            # G = Predicate for having clause
            elif field == "HAVING":
                mf_structure['having'] = args.strip()
                
    return mf_structure

# if "__main__" == __name__:
#     parse_MF_struct("../input/input.txt")
    