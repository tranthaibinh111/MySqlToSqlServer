import os

from datetime import datetime
from models.product_image_entity import ProductImageEntity
from controllers.excel_controller import  ExcelController

class ProductImageController:
	def __init__(self, product_controller):
		self.product_images = []
		self.__mapping(product_controller)

	def __mapping(self, product_controller):

		index = 0

		for product in product_controller.products:
			if product.product_images is not None:
				for image in product.product_images:

					index += 1
					product_image = ProductImageEntity()

					product_image.id = index
					product_image.product_id = product.id
					product_image.product_image = image
					product_image.is_hidden= product.is_hidden
					product_image.created_date= product.created_date
					product_image.created_by= product.created_by
					product_image.modified_date= product.modified_date
					product_image.modified_by= product.modified_by

					self.product_images.append(product_image)

	def __convert_sql(self, product_image):
		if product_image.product_id is None:
			product_image.product_id = "NULL"

		if product_image.product_image is None:
			product_image.product_sku = "NULL"

		if product_image.is_hidden is None:
			product_image.is_hidden = 0

		if product_image.created_date is None:
			product_image.created_date = str(datetime.now())

		if product_image.created_by is None:
			product_image.created_by = "admin"

		if product_image.modified_date is None:
			product_image.modified_date = "NULL"

		if product_image.modified_by is None:
			product_image.modified_by = "NULL"

	def export_sql(self):
		file_name = os.getcwd() + "\\export_sql\\product_image.sql"

		with open(file_name, mode="w+", encoding="utf-8") as wf:
			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductImage ON;\n")
			wf.write("\n")
			wf.write("DELETE FROM dbo.tbl_ProductImage;\n")
			wf.write("\n")

			index = 0
			for product_image in self.product_images:
				index += 1

				self.__convert_sql(product_image)

				sql_text = ""
				sql_text += "INSERT INTO dbo.tbl_ProductImage("
				sql_text += "	ID"
				sql_text += ",	ProductID"
				sql_text += ",	ProductImage"
				sql_text += ",	IsHidden"
				sql_text += ",	CreatedDate"
				sql_text += ",	CreatedBy"
				sql_text += ",	ModifiedDate"
				sql_text += ",	ModifiedBy"
				sql_text += ") VALUES("
				sql_text += "	" + str(product_image.id)
				sql_text += ",	" + str(product_image.product_id)

				if product_image.product_image == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_image.product_image) + "'"

				sql_text += ",	" + str(product_image.is_hidden)

				if product_image.created_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_image.created_date) + "' AS DATETIME2)"

				if product_image.created_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_image.created_by) + "'"

				if product_image.modified_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_image.modified_date) + "' AS DATETIME2)"

				if product_image.modified_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_image.modified_by) + "'"

				sql_text += ");\n"

				wf.write(sql_text)

				if index > 100:
					wf.write("GO\n")
					index = 0

			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductImage OFF;\n")