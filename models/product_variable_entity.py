from datetime import datetime

class ProductVariableEntity:
	def __init__(self):
		self.id = None
		self.product_id = None
		self.parent_sku = None
		self.stock = 0
		self.stock_status = 0
		self.regular_price = 0
		self.cost_of_good = 0
		self.image = None
		self.manage_stock = 1
		self.is_hidden = 0
		self.created_date = str(datetime.now())
		self.created_by = "admin"
		self.modified_date = None
		self.modified_by = None
		self.color = None
		self.size = None
		self.retail_price = 0
		self.minimum_inventory_level = None
		self.maximum_inventory_level = None
		self.supplier_id = None
		self.supplier_name = None