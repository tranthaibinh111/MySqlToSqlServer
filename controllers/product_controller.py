import os

from models.product_entity import ProductEntity
from controllers.excel_controller import  ExcelController

class ProductController:
	def __init__(self, file_name, sheet_name="Sheet1", *category_controller):
		self.__file_name = file_name
		self.__sheet_name = sheet_name
		self.products = []

		self.__mapping(*category_controller)

	def __mapping(self, category_controller):
		datas = ExcelController.get_data(self.__file_name, self.__sheet_name)

		index = 0

		for row in datas:
			index += 1
			product = ProductEntity()

			product.id = index

			if row[14] is not None:
				categores = row[14].split(" > ")
				categore_name = categores[len(categores) - 1]
				product.category_id = category_controller.get_category_id(categore_name)

				if product.category_id is None:
					print(categore_name)
					raise "CategoryName khong ton tai trong table tbl_category"

			product.product_title = row[0]
			product.product_content = row[3]
			product.product_sku = row[5]

			if row[13] is None:
				if row[13].upper() == "VARIABLE":
					product.manage_stock = 0
				else:
					product.manage_stock = 1
			else:
				product.manage_stock = 1

			product.regular_price = row[9]
			product.cost_of_good = row[10]
			product.retail_price = row[11]

			if row[12] is not None:
				image = row[12].split(" | ")
				product.product_images = image
				product.product_image = product.product_images[0]

			self.products.append(product)

	def __convert_sql(self, product):
		if product.category_id is None:
			product.category_id = "NULL"

		if product.product_old_id is None:
			product.product_old_id = "NULL"

		if product.product_title is None:
			product.product_title = "NULL"
		else:
			product.product_title = product.product_title.replace("'", "''")

		if product.product_content is None:
			product.product_content = "NULL"
		else:
			product.product_content = product.product_content.replace("\n", "").replace("'", "''")

		if product.product_sku is None:
			product.product_sku = "NULL"

		if product.product_stock is None:
			product.product_stock = 0

		if product.stock_status is None:
			product.stock_status = 0

		if product.manage_stock is None:
			product.manage_stock = 1

		if product.regular_price is None:
			product.regular_price = 0

		if product.cost_of_good is None:
			product.cost_of_good = 0

		if product.retail_price is None:
			product.retail_price = 0

		if product.product_image is None:
			product.product_image = "NULL"

		if product.product_type is None:
			product.product_type = 0

		if product.is_hidden is None:
			product.is_hidden = 0

		if product.created_date is None:
			product.created_date = str(datetime.now())

		if product.created_by is None:
			product.created_by = "admin"

		if product.modified_date is None:
			product.modified_date = str(datetime.now())

		if product.modified_by is None:
			product.modified_by = "admin"

		if product.materials is None:
			product.materials = "NULL"

		if product.minimum_inventory_level is None:
			product.minimum_inventory_level = "NULL"

		if product.maximum_inventory_level is None:
			product.maximum_inventory_level = "NULL"

		if product.supplier_id is None:
			product.supplier_id = "NULL"

		if product.supplier_name is None:
			product.supplier_name = "NULL"

		if product.product_style is None:
			product.product_style = "NULL"

	def get_product_id(self, product_sku):
		result = None

		for product in self.products:
			if product.product_sku.upper() == product_sku.upper():
				result = product.id
				break

		return result

	def update_status_stock(self, product_total):
		for product in self.products:
			for group in product_total:
				if product.product_sku == group[0]:
					product.product_stock = group[1]

					if product.product_stock > 0:
						product.stock_status = 1 #instock
					else:
						product.stock_status = 0 #outstock

	def export_sql(self):
		file_name = os.getcwd() + "\\export_sql\\product.sql"

		with open(file_name, mode="w", encoding="utf-8") as wf:
			wf.write("SET IDENTITY_INSERT dbo.tbl_Product ON;\n")
			wf.write("\n")
			wf.write("DELETE FROM dbo.tbl_Product;\n")
			wf.write("\n")

			index = 0
			for product in self.products:
				index += 1

				self.__convert_sql(product)

				sql_text = ""
				sql_text += "INSERT INTO dbo.tbl_Product("
				sql_text += "	ID"
				sql_text += ",	CategoryID"
				sql_text += ",	ProductOldID"
				sql_text += ",	ProductTitle"
				sql_text += ",	ProductContent"
				sql_text += ",	ProductSKU"
				sql_text += ",	ProductStock"
				sql_text += ",	StockStatus"
				sql_text += ",	ManageStock"
				sql_text += ",	Regular_Price"
				sql_text += ",	CostOfGood"
				sql_text += ",	Retail_Price"
				sql_text += ",	ProductImage"
				sql_text += ",	ProductType"
				sql_text += ",	IsHidden"
				sql_text += ",	CreatedDate"
				sql_text += ",	CreatedBy"
				sql_text += ",	ModifiedDate"
				sql_text += ",	ModifiedBy"
				sql_text += ",	Materials"
				sql_text += ",	MinimumInventoryLevel"
				sql_text += ",	MaximumInventoryLevel"
				sql_text += ",	SupplierID"
				sql_text += ",	SupplierName"
				sql_text += ",	ProductStyle"
				sql_text += ") VALUES("
				sql_text += "	" + str(product.id)
				sql_text += ",	" + str(product.category_id)
				sql_text += ",	" + str(product.product_old_id)

				if product.product_title == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.product_title) + "'"

				if product.product_content == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.product_content) + "'"

				if product.product_sku == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.product_sku) + "'"

				sql_text += ",	" + str(product.product_stock)
				sql_text += ",	" + str(product.stock_status)
				sql_text += ",	" + str(product.manage_stock)
				sql_text += ",	" + str(product.regular_price)
				sql_text += ",	" + str(product.cost_of_good)
				sql_text += ",	" + str(product.retail_price)

				if product.product_image == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.product_image) + "'"

				sql_text += ",	" + str(product.product_type)
				sql_text += ",	" + str(product.is_hidden)

				if product.created_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product.created_date) + "' AS DATETIME2)"

				if product.created_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.created_by) + "'"

				if product.modified_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product.modified_date) + "' AS DATETIME2)"

				if product.modified_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.modified_by) + "'"

				if product.materials == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.materials) + "'"

				sql_text += ",	" + str(product.minimum_inventory_level)
				sql_text += ",	" + str(product.maximum_inventory_level)
				sql_text += ",	" + str(product.supplier_id)

				if product.supplier_name == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product.supplier_name) + "'"

				sql_text += ",	" + str(product.product_style)
				sql_text += ");\n"

				wf.write(sql_text)

				if index > 100:
					wf.write("GO\n")
					index = 0

			wf.write("SET IDENTITY_INSERT dbo.tbl_Product OFF;\n")