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
    """