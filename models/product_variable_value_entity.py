from datetime import datetime

class ProductVariableValueEntity:
	def __init__(self):
		self.id = None
		self.product_variable_id = None
		self.product_variable_sku = None
		self.variable_value_id = None
		self.variable_name = None
		self.variable_value = None
		self.is_hidden = 0
		self.created_date = str(datetime.now())
		self.created_by = "admin"
		self.modified_date = str(datetime.now())
		self.modified_by = "admin"