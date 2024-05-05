import json

def extract_set(str):
    return json.loads(str)

def parse_MF_Struct(input_file = None):
    struct = dict()

    if input_file == None:
        struct['select'] = input("SELECTION ATTRIBUTES: ")
        struct['numGV'] = input("NUMBER OF GROUPING VARIABLES: ")
        struct['groupAttributes'] = input("GROUPING ATTRIBUTES: ")
        struct['fVector'] = input("AGGREGATE FUNCTIONS: ")
        struct['predicates'] = input("PREDICATES FOR GVs: ")
        struct['having'] = input("HAVING: ")

    else: 
        f = open(input_file, 'r').readlines()

        for line in f:
            args = line.split(": ")
            field = args[0]
            if field == 'SELECTION ATTRIBUTES':
                struct['select'] = args[1]
            elif field == 'NUMBER OF GROUPING VARIABLES':
                struct['numGV'] = int(args[1])
            elif field == 'GROUPING ATTRIBUTES':
                struct['groupAttributes'] = args[1]
            elif field == 'AGGREGATE FUNCTIONS':
                struct['fVector'] = map(extract_set, args[1:])
            elif field == 'PREDICATES FOR GVs':
                struct['predicates'] = map(extract_set, args[1:])
            elif field == "HAVING":
                struct['having'] = args[1]
                
    return struct
