
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv

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

    class H:
        def __init__(self, num_grouping_attributes, num_aggregates):
            self.num_grouping_attributes = num_grouping_attributes
            self.num_aggregates = num_aggregates
            self.table = dict()
    
        def insert(self, grouping_attributes, aggregates):
            key = tuple(grouping_attributes)
            if key not in self.table:
                self.table[key] = [None] * self.num_aggregates
    
            for i, aggregate in enumerate(aggregates):
                self.table[key][i] = aggregate
    
        def get(self, grouping_attributes):
            key = tuple(grouping_attributes)
            return self.table.get(key, None)
    
    _global = []
    
    
    h_table = H(0, 3)
    for (cust, prod, day, month, year, state, quant, date) in enumerate(all_sales, 1):
        for i in range(3):
    
            
        
    
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    