import subprocess
from helpers.algorithm import produce_algorithm
from helpers.classH import def_H_table

def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    query_num = input("Query number: ")

    if query_num:
        fname = "input/input{}.txt".format(query_num)
    else:
        fname = None
        
    # Get arguments for Phi operator
    algorithm = produce_algorithm(fname)

    # Note: The f allows formatting with variables. Indentation is preserved.
    tmp = f"""
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
from helpers.mf_struct import parse_MF_struct

def query():
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    select_stmt = "SELECT * FROM sales"
    cur.execute(select_stmt)
    all_sales = cur.fetchall()

    input_file = "{fname}"

    {def_H_table}
    
    _global = []
    {algorithm}

    headers = mf_structure['select'].split(',')

    def cleanup(info: dict, fVector = mf_structure['fVector']):
        vs = []
        for k,v in info.items():
            if k in fVector:
                vs.append(v)
        return vs

    for entry_id, info in h_table.table.items():
        entry = []
        if type(entry_id) is tuple:
            for t in entry_id:
                entry += [t] 
        else:
            entry += [entry_id]
        entry += cleanup(info)
        
        _global.append(entry)
    
    return tabulate.tabulate(_global,
                        headers=headers, tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code to a file
    open("output.py", "w").write(tmp)
    # Execute the generated code
    subprocess.run(["python3", "output.py"])


if "__main__" == __name__:
    main()
