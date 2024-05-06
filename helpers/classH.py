def_H_table = """
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
    """