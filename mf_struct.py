def list_of_strings(args):
    return list(map(str.strip, args.split(',')))

def extract_set(args):
    args = args.replace('{', '').replace('}', '')
    return set(args.split(','))

def parse_MF_Struct(input_file = None):
    struct = dict()

    if input_file == None:
        # Manually collect arguments if input file not specified
        struct['select'] = input("SELECTION ATTRIBUTES: ")
        struct['numGV'] = int(input("NUMBER OF GROUPING VARIABLES: "))
        struct['groupAttributes'] = list_of_strings(input("GROUPING ATTRIBUTES: "))
        struct['fVector'] = list_of_strings(input("AGGREGATE FUNCTIONS: "))
        predicate_input = input("PREDICATES FOR GVs: ")
        struct['predicates'] = list(map(extract_set, predicate_input.split()))
        struct['having'] = input("HAVING: ")

    else: 
        # Read arguments from input file
        f = open(input_file, 'r').readlines()

        for line in f:
            current_input = line.split(": ")
            field = current_input[0]
            args = current_input[1]

            # S = List of projected attributes for the query output
            if field == 'SELECTION ATTRIBUTES':
                struct['select'] = args.strip()

            # n = Number of grouping variables
            elif field == 'NUMBER OF GROUPING VARIABLES':
                struct['numGV'] = int(args)

            # V = List of grouping attributes
            elif field == 'GROUPING ATTRIBUTES':
                # Type: [ str, ... ]
                struct['groupAttributes'] = list_of_strings(args)

            # [F] = {F0, ... , Fn} List of sets of aggregate functions
            elif field == 'AGGREGATE FUNCTIONS':
                # Type: [ str, ... ]
                struct['fVector'] = list_of_strings(args)

            # [σ] = {σ0, ... , σn} List of predicates to define ranges for GVs
            elif field == 'PREDICATES FOR GVs':
                # Type: List of sets of strings [ {str}, ... ]
                struct['predicates'] = list(map(extract_set, args.split()))

            # G = Predicate for having clause
            elif field == "HAVING":
                struct['having'] = args.strip()
                
    return struct
