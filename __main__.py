import os

from controllers.category_controller import CategoryController
from controllers.variable_value_controller import VariableValueController
from controllers.product_controller import ProductController
from controllers.product_image_controller import ProductImageController
from controllers.product_variable_controller import ProductVariableController
from controllers.product_variable_value_controller import ProductVariableValueController

if __name__ == "__main__":
	category_controller = CategoryController(os.getcwd() + "\\import_excel\\category.xlsx", "category")
	variable_value_controller = VariableValueController(os.getcwd() + "\\import_excel\\variable-value.xlsx", "variable-value")

	product_controller = ProductController(os.getcwd() + "\\import_excel\\san-pham.xlsx", "san-pham", category_controller)
	product_image_controller = ProductImageController(product_controller)
	product_variable_controller = ProductVariableController(os.getcwd() + "\\import_excel\\bien-the.xlsx", "bien-the", product_controller)
	product_variable_value_controller = ProductVariableValueController(product_variable_controller, variable_value_controller)

	product_controller.update_status_stock(product_variable_controller.product_totals)

	product_controller.export_sql()
	product_image_controller.export_sql()
	product_variable_value_controller.export_sql()
	product_variable_controller.export_sql()

	print("Ket thuc chuong trinh")