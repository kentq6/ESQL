
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

    input_file = "input/input.txt"

    
    class H:
        def __init__(self, num_grouping_attributes, num_aggregates):
            self.num_grouping_attributes = num_grouping_attributes
            self.num_aggregates = num_aggregates
            self.table = dict()
    
        def insert(self, grouping_attributes):
            key = tuple(grouping_attributes)
            if key not in self.table:
                self.table[key] = dict()
        
        def update(self, grouping_attributes, aggregate, aggregate_value):
            key = tuple(grouping_attributes)
            self.table[key][aggregate] = aggregate_value
    
        def get(self, grouping_attributes):
            key = tuple(grouping_attributes)
            return self.table.get(key, None)
    
    
    _global = []
    
    
    mf_structure = parse_MF_struct(input_file)

    # Create instance of H_Table
    h_table = H(len(mf_structure['groupAttributes']), len(mf_structure['fVector']))

    for entry, (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(mf_structure['numGV']):
    
            if i == 0:
                aggregate_funcs = ['1_sum_quant']
                if (cust) in h_table and state=='NJ':
                    for func in aggregate_funcs:
                        h_table.update(cust,func,quant)
                else:
                    h_table.insert(cust)
        
            if i == 1:
                aggregate_funcs = ['2_sum_quant']
                if (cust) in h_table and state=='NY':
                    for func in aggregate_funcs:
                        h_table.update(cust,func,quant)
                else:
                    h_table.insert(cust)
        
    
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    