code_for_H_table = """
    class H:
        def __init__(self, num_grouping_attributes, num_aggregates):
            self.num_grouping_attributes = num_grouping_attributes
            self.num_aggregates = num_aggregates
            self.table = {}
    
        def insert(self, grouping_attributes, aggregates):
            key = tuple(grouping_attributes)
            if key not in self.table:
                self.table[key] = [None] * self.num_aggregates
    
            for i, aggregate in enumerate(aggregates):
                self.table[key][i] = aggregate
    
        def get(self, grouping_attributes):
            key = tuple(grouping_attributes)
            return self.table.get(key, None)
    """