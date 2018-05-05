from datetime import datetime


class InOutProductVariableEntity:
    def __init__(self):
        self.id = None
        self.agent_id = 1
        self.product_id = None
        self.product_variable_id = None
        self.product_variable_name = None
        self.product_variable_value = None
        self.quantity = None
        self.quantity_current = 0
        self.type = 1
        self.is_hidden = 0
        self.created_date = datetime.now()
        self.created_by = "admin"
        self.modified_date = None
        self.modified_by = None
        self.product_type = None
        self.note = None
        self.order_id = 0
        self.session_in_out_id = 0
        self.status = 1
        self.product_name = None
        self.sku = None
        self.product_image = None
        self.product_variable = None
        self.move_pro_id = 0
        self.parent_id = None
