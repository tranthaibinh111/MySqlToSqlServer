from datetime import datetime


class VariableValueEntity:
    def __init__(self):
        self.id = None
        self.variable_id = None
        self.variable_name = None
        self.variable_value = None
        self.is_hidden = 0
        self.create_date = datetime.now()
        self.create_by = "admin"
        self.modified_date = None
        self.modified_by = None
        self.variable_value_text = None
        self.sku_text = None
