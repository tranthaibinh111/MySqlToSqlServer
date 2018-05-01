import os

from datetime import datetime
from models.product_variable_entity import ProductVariableEntity
from controllers.excel_controller import  ExcelController

class ProductVariableController:
	def __init__(self, file_name, sheet_name="Sheet1", *product_controller):
		self.__file_name = file_name
		self.__sheet_name = sheet_name
		self.product_variables = []
		self.product_parents = []

		self.__mapping(*product_controller)

	def __mapping(self, product_controller):
		datas = ExcelController.get_data(self.__file_name, self.__sheet_name)

		index = 0
		parent_sku = None
		product_stock = 0

		for row in datas:
			index += 1
			product_variable = ProductVariableEntity()

			product_variable.id = index
			product_variable.parent_sku = row[0]
			product_variable.sku = row[4]

			product_variable.product_id = product_controller.get_product_id(product_variable.parent_sku)
			if product_variable.product_id is None:
				print(product_variable.parent_sku)
				raise "ParentSku khong ton tai trong table tbl_Product"

			if row[5] is None:
					product_variable.stock = 0
			else:
				# Do file excel co van de format nen de float
				if float(str(row[5]).replace("'", "")) < 0:
					product_variable.stock = 0
				else:
					product_variable.stock = row[5]

			if product_variable.stock > 0:
				product_variable.stock_status = 1
			else:
				product_variable.stock_status = 0

			product_variable.regular_price = row[7]
			product_variable.cost_of_good = row[8]
			product_variable.image = row[9]
			product_variable.color = row[12]
			product_variable.size = row[13]
			product_variable.retail_price = row[14]

			self.product_variables.append(product_variable)
			self.__calculator_product(product_variable.parent_sku, product_variable.stock, product_variable.regular_price)

	# Su ly lay thong tin stock  cho table product
	def __calculator_product(self, parent_sku, stock, regular_price):
		check_exist = False
		min_regular_price = regular_price

		for product_stock in self.product_parents:
			if product_stock["parent_sku"] == parent_sku:
				check_exist = True
				product_stock["stock"] += stock

				if product_stock["regular_price"] > min_regular_price:
					product_stock["regular_price"] = min_regular_price

		if not check_exist:
			self.product_parents.append({"parent_sku" : parent_sku, "stock": stock, "regular_price": regular_price})

	def __convert_sql(self, product_variable):
		if product_variable.product_id is None:
			product_variable.product_id = "NULL"

		if product_variable.parent_sku is None:
			product_variable.parent_sku = "NULL"

		if product_variable.stock is None:
			product_variable.stock = 0

		if product_variable.stock_status is None:
			product_variable.stock_status = 0

		if product_variable.regular_price is None:
			product_variable.regular_price = 0

		if product_variable.cost_of_good is None:
			product_variable.cost_of_good = 0

		if product_variable.image is None:
			product_variable.image = "NULL"

		if product_variable.manage_stock is None:
			product_variable.manage_stock = 1

		if product_variable.is_hidden is None:
			product_variable.is_hidden = 0

		if product_variable.created_date is None:
			product_variable.created_date = str(datetime.now())

		if product_variable.created_by is None:
			product_variable.created_by = "admin"

		if product_variable.modified_date is None:
			product_variable.modified_date = "NULL"

		if product_variable.modified_by is None:
			product_variable.modified_by = "NULL"

		if product_variable.color is None:
			product_variable.color = "NULL"

		if product_variable.size is None:
			product_variable.size = "NULL"

		if product_variable.retail_price is None:
			product_variable.retail_price = 0

		if product_variable.minimum_inventory_level is None:
			product_variable.minimum_inventory_level = 2

		if product_variable.maximum_inventory_level is None:
			product_variable.maximum_inventory_level = 10

		if product_variable.supplier_id is None:
			product_variable.supplier_id = "NULL"

		if product_variable.supplier_name is None:
			product_variable.supplier_name = "NULL"

	def export_sql(self):
		file_name = os.getcwd() + "\\export_sql\\product_variable.sql"

		with open(file_name, mode="w+", encoding="utf-8") as wf:
			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariable ON;\n")
			wf.write("\n")
			wf.write("DELETE FROM dbo.tbl_ProductVariable;\n")
			wf.write("\n")

			index = 0
			for product_variable in self.product_variables:
				index += 1

				self.__convert_sql(product_variable)

				sql_text = ""
				sql_text += "INSERT INTO dbo.tbl_ProductVariable("
				sql_text += "	ID"
				sql_text += ",	ProductID"
				sql_text += ",	ParentSKU"
				sql_text += ",	SKU"
				sql_text += ",	Stock"
				sql_text += ",	StockStatus"
				sql_text += ",	Regular_Price"
				sql_text += ",	CostOfGood"
				sql_text += ",	Image"
				sql_text += ",	ManageStock"
				sql_text += ",	IsHidden"
				sql_text += ",	CreatedDate"
				sql_text += ",	CreatedBy"
				sql_text += ",	ModifiedDate"
				sql_text += ",	ModifiedBy"
				sql_text += ",	color"
				sql_text += ",	size"
				sql_text += ",	RetailPrice"
				sql_text += ",	MinimumInventoryLevel"
				sql_text += ",	MaximumInventoryLevel"
				sql_text += ",	SupplierID"
				sql_text += ",	SupplierName"
				sql_text += ") VALUES("
				sql_text += "	" + str(product_variable.id)

				if product_variable.product_id == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.product_id) + "'"

				if product_variable.parent_sku == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.parent_sku) + "'"

				if product_variable.sku == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.sku) + "'"

				sql_text += ",	" + str(product_variable.stock)
				sql_text += ",	" + str(product_variable.stock_status)
				sql_text += ",	" + str(product_variable.regular_price)
				sql_text += ",	" + str(product_variable.cost_of_good)

				if product_variable.image == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.image) + "'"

				sql_text += ",	" + str(product_variable.manage_stock)
				sql_text += ",	" + str(product_variable.is_hidden)

				if product_variable.created_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_variable.created_date) + "' AS DATETIME2)"

				if product_variable.created_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.created_by) + "'"

				if product_variable.modified_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_variable.modified_date) + "' AS DATETIME2)"

				if product_variable.modified_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.modified_by) + "'"

				if product_variable.color == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.color) + "'"

				if product_variable.size == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.size) + "'"

				sql_text += ",	" + str(product_variable.retail_price)
				sql_text += ",	" + str(product_variable.minimum_inventory_level)
				sql_text += ",	" + str(product_variable.maximum_inventory_level)
				sql_text += ",	" + str(product_variable.supplier_id)

				if product_variable.supplier_name == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable.supplier_name) + "'"

				sql_text += ");\n"

				wf.write(sql_text)

				if index > 100:
					wf.write("GO\n")
					index = 0

			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariable OFF;\n")