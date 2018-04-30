import os

from datetime import datetime
from models.product_variable_value_entity import ProductVariableValueEntity
from controllers.excel_controller import  ExcelController

class ProductVariableValueController:
	def __init__(self, product_variable_controller, variable_value_controller):
		self.product_variable_values = []
		self.__mapping(product_variable_controller, variable_value_controller)

	def __mapping(self, product_variable_controller, variable_value_controller):

		index = 0

		for product_variable in product_variable_controller.product_variables:
			product_variable_column = []

			if product_variable.color is not None and product_variable.size is not None:
				product_variable_column = ["Color", "Size"]
			elif product_variable.color is not None:
				product_variable_column = ["Color"]
			elif product_variable.size is not None:
				product_variable_column = ["Size"]

			for column in product_variable_column:
				index += 1
				product_variable_value = ProductVariableValueEntity()

				product_variable_value.id = index
				product_variable_value.product_variable_id = product_variable.id

				if column == "Color":
					info_variable_value = variable_value_controller.get_variable_value_info(column, product_variable.color)
				else:
					info_variable_value = variable_value_controller.get_variable_value_info(column, product_variable.size)

				if info_variable_value is None:
					print(column, " ", product_variable.color, " ", product_variable.size)
					raise("Color or Size khong ton tai trong table tbl_VariableValue")

				product_variable_value.product_variable_sku = str(product_variable.parent_sku) + str(info_variable_value["sku_text"])
				product_variable_value.variable_value_id = info_variable_value["id"]
				product_variable_value.variable_name = info_variable_value["variable_name"]
				product_variable_value.variable_value = info_variable_value["variable_value"]
				product_variable_value.is_hidden= product_variable.is_hidden
				product_variable_value.created_date= product_variable.created_date
				product_variable_value.created_by= product_variable.created_by
				product_variable_value.modified_date= product_variable.modified_date
				product_variable_value.modified_by= product_variable.modified_by

				self.product_variable_values.append(product_variable_value)

	def __convert_sql(self, product_variable_value):
		if product_variable_value.product_variable_id is None:
			product_variable_value.product_variable_id = "NULL"

		if product_variable_value.product_variable_sku is None:
			product_variable_value.product_variable_sku = "NULL"

		if product_variable_value.variable_value_id is None:
			product_variable_value.variable_value_id = "NULL"

		if product_variable_value.variable_name is None:
			product_variable_value.variable_name = "NULL"

		if product_variable_value.variable_value is None:
			product_variable_value.variable_value = "NULL"

		if product_variable_value.is_hidden is None:
			product_variable_value.is_hidden = 0

		if product_variable_value.created_date is None:
			product_variable_value.created_date = str(datetime.now())

		if product_variable_value.created_by is None:
			product_variable_value.created_by = "admin"

		if product_variable_value.modified_date is None:
			product_variable_value.modified_date = str(datetime.now())

		if product_variable_value.modified_by is None:
			product_variable_value.modified_by = "admin"

	def export_sql(self):
		file_name = os.getcwd() + "\\export_sql\\product_variable_value.sql"

		with open(file_name, mode="w+", encoding="utf-8") as wf:
			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariableValue ON;\n")
			wf.write("\n")
			wf.write("DELETE FROM dbo.tbl_ProductVariableValue;\n")
			wf.write("\n")

			index = 0
			for product_variable_value in self.product_variable_values:
				index += 1

				self.__convert_sql(product_variable_value)

				sql_text = ""
				sql_text += "INSERT INTO dbo.tbl_ProductVariableValue("
				sql_text += "	ID"
				sql_text += ",	ProductVariableID"
				sql_text += ",	ProductvariableSKU"
				sql_text += ",	VariableValueID"
				sql_text += ",	VariableName"
				sql_text += ",	VariableValue"
				sql_text += ",	IsHidden"
				sql_text += ",	CreatedDate"
				sql_text += ",	CreatedBy"
				sql_text += ",	ModifiedDate"
				sql_text += ",	ModifiedBy"
				sql_text += ") VALUES("
				sql_text += "	" + str(product_variable_value.id)
				sql_text += ",	" + str(product_variable_value.product_variable_id)

				if product_variable_value.product_variable_sku == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable_value.product_variable_sku) + "'"

				sql_text += ",	" + str(product_variable_value.variable_value_id)

				if product_variable_value.variable_name == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable_value.variable_name) + "'"

				if product_variable_value.variable_value == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable_value.variable_value) + "'"

				sql_text += ",	" + str(product_variable_value.is_hidden)

				if product_variable_value.created_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_variable_value.created_date) + "' AS DATETIME2)"

				if product_variable_value.created_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable_value.created_by) + "'"

				if product_variable_value.modified_date == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	CAST('" + str(product_variable_value.modified_date) + "' AS DATETIME2)"

				if product_variable_value.modified_by == "NULL":
					sql_text += ",	NULL"
				else:
					sql_text += ",	N'" + str(product_variable_value.modified_by) + "'"

				sql_text += ");\n"

				wf.write(sql_text)

				if index > 100:
					wf.write("GO\n")
					index = 0

			wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariableValue OFF;\n")