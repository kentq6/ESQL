def_H_table = """
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
    """