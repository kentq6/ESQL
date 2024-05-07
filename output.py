
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

    input_file = "input/input4.txt"

    
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
                    self.table[key][f] = -1 if ('min' in f) else 0
        
        def update(self, grouping_attributes, aggregate, val, gv):
            key = grouping_attributes
            if 'sum' in aggregate:
                self.table[key][aggregate] += val
            elif 'min' in aggregate:
                current_min = self.table[key][aggregate]
                self.table[key][aggregate] = current_min if (current_min < val and current_min != -1) else val
            elif 'max' in aggregate:
                current_max = self.table[key][aggregate]
                self.table[key][aggregate] = current_max if (current_max > val) else val
            elif 'count' in aggregate:
                self.table[key][aggregate] += 1
            elif 'avg' in aggregate:
                self.update_avg(grouping_attributes, aggregate, val, gv)
        
        def update_avg(self, grouping_attributes, aggregate, val, gv):
            key = grouping_attributes
            sum_aggr = str(gv) + '_sum_quant'
            count_aggr = str(gv) + '_count_quant'
            self.table[key][aggregate] = self.get(key, sum_aggr) / self.get(key, count_aggr)
    
        def get(self, grouping_attributes, aggregate):
            key = grouping_attributes
            return self.table[key][aggregate]
    
    
    _global = []
    
    mf_structure = {'select': 'cust, prod, 1_sum_quant, 1_count_quant, 1_avg_quant, 2_avg_quant', 'numGV': 2, 'groupAttributes': ['cust', 'prod'], 'fVector': ['1_sum_quant', '1_count_quant', '1_avg_quant', '2_avg_quant'], 'predicates': [["1.state='NJ'"], ["2.state='NY'"]], 'having': '2_avg_quant > 1_avg_quant'}

    # Create instance of H_Table
    h_table = H(len(mf_structure['groupAttributes']), len(mf_structure['fVector']))

    for entry, (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(mf_structure['numGV']):
    
            if i == 0:
                aggregate_funcs = ['1_sum_quant', '1_count_quant', '1_avg_quant']
                if (cust,prod) in h_table.table and state=='NJ':
                    avg_aggr = None
                    for func in aggregate_funcs:
                        if 'avg' in func:
                            avg_aggr = func
                        else:
                            h_table.update((cust,prod),func,quant,1)
                    if avg_aggr != None:
                        h_table.update((cust,prod),avg_aggr,quant,1)
                        
                else:
                    cols = mf_structure['fVector'].copy()
                    for func in aggregate_funcs:
                        if func not in cols:
                            cols.append(func)
                    h_table.insert((cust,prod), cols)
        
            if i == 1:
                aggregate_funcs = ['2_avg_quant', '2_sum_quant', '2_count_quant']
                if (cust,prod) in h_table.table and state=='NY':
                    avg_aggr = None
                    for func in aggregate_funcs:
                        if 'avg' in func:
                            avg_aggr = func
                        else:
                            h_table.update((cust,prod),func,quant,2)
                    if avg_aggr != None:
                        h_table.update((cust,prod),avg_aggr,quant,2)
                        
                else:
                    cols = mf_structure['fVector'].copy()
                    for func in aggregate_funcs:
                        if func not in cols:
                            cols.append(func)
                    h_table.insert((cust,prod), cols)
        

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
    