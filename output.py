
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

    input_file = "input/input2.txt"

    
    class H:
        def __init__(self, num_grouping_attributes, num_aggregates):
            self.num_grouping_attributes = num_grouping_attributes
            self.num_aggregates = num_aggregates
            self.table = dict()
    
        def insert(self, grouping_attributes, fVector):
            key = grouping_attributes
            if key not in self.table:
                self.table[key] = dict()
                for f in fVector:
                    self.table[key][f] = 0
        
        def update(self, grouping_attributes, aggregate, val):
            key = grouping_attributes
            if 'sum' in aggregate:
                self.table[key][aggregate] += val
            elif 'min' in aggregate:
                current_min = self.table[key][aggregate]
                self.table[key][aggregate] = current_min if current_min<val else val
            elif 'max' in aggregate:
                current_max = self.table[key][aggregate]
                self.table[key][aggregate] = current_max if current_max>val else val
            elif 'count' in aggregate:
                self.table[key][aggregate] += 1
    
        def get(self, grouping_attributes):
            key = grouping_attributes
            return self.table.get(key, None)
    
    
    _global = []
    
    mf_structure = parse_MF_struct(input_file)

    # Create instance of H_Table
    h_table = H(len(mf_structure['groupAttributes']), len(mf_structure['fVector']))

    for entry, (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(mf_structure['numGV']):
    
            if i == 0:
                aggregate_funcs = ['1_sum_quant', '1_count_quant', '1_min_quant', '1_max_quant']
                if (cust,prod) in h_table.table and state=='NJ':
                    for func in aggregate_funcs:
                        h_table.update((cust,prod),func,quant)
                else:
                    h_table.insert((cust,prod), mf_structure['fVector'])
        
            if i == 1:
                aggregate_funcs = ['2_sum_quant']
                if (cust,prod) in h_table.table and state=='NY':
                    for func in aggregate_funcs:
                        h_table.update((cust,prod),func,quant)
                else:
                    h_table.insert((cust,prod), mf_structure['fVector'])
        

    for entry_id, info in h_table.table.items():
        entry = []
        if type(entry_id) is tuple:
            for t in entry_id:
                entry += [t]
        else:
            entry += [entry_id]
        entry += [*info.values()]
        _global.append(entry)

    headers = mf_structure['select'].split(',')
    
    return tabulate.tabulate(_global,
                        headers=headers, tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    