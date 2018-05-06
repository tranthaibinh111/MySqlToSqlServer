import os
from common.sql import CommonSql
from models import ProductEntity
from controllers import ExcelController


class ProductController:
    def __init__(self, file_name, sheet_name, category_controller):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.product_simples = []
        self.product_variables = []

        self.__mapping(category_controller)

    def __mapping(self, category_controller):
        data = ExcelController.get_data(self.__file_name, self.__sheet_name)

        index = 0

        for row in data:
            index += 1
            product = ProductEntity()

            product.id = index

            if row[14] is not None:
                categories = row[14].split(" > ")
                category_name = categories[len(categories) - 1]
                product.category_id = category_controller.get_category_id(category_name)

                if product.category_id is None:
                    print(category_name)
                    raise Exception("CategoryName khong ton tai trong table tbl_category")

            product.product_title = row[0]
            product.product_content = row[3]
            product.product_sku = row[5]

            if row[13] is not None and row[13].upper() == "VARIABLE":
                product.product_stock = 0
                product.manage_stock = 0
                product.product_style = 2
            else:
                if row[6] is not None:
                    if int(str(row[6]).replace("'", "")) > 0:
                        product.product_stock = row[6]
                    else:
                        product.product_stock = 0

                if product.product_stock > 0:
                    # in stock
                    product.stock_status = 1
                else:
                    # out stock
                    product.stock_status = 0

                product.manage_stock = 1
                product.regular_price = row[9]
                product.product_style = 1
                product.minimum_inventory_level = 2
                product.maximum_inventory_level = 10

            product.cost_of_good = row[11]
            product.retail_price = row[10]

            if row[12] is not None:
                image = row[12].split(" | ")
                product.product_images = image
                product.product_image = product.product_images[0]

            if product.manage_stock == 1:
                # simple
                self.product_simples.append(product)
            else:
                # variable
                self.product_variables.append(product)

    def get_product_list(self):
        return self.product_simples + self.product_variables

    def get_product_variable_id(self, product_sku):
        result = None

        for product in self.product_variables:
            if product.product_sku.upper() == product_sku.upper():
                result = product.id
                break

        return result

    def update_product_variable(self, product_parents):
        for product in self.product_variables:
            for group in product_parents:
                if product.product_sku == group["parent_sku"]:
                    product.regular_price = group["regular_price"]

                    if group["stock"] > 0:
                        # in stock
                        product.stock_status = 1
                    else:
                        # out stock
                        product.stock_status = 0

    def export_sql(self):
        file_name = os.getcwd() + "\\export_sql\\product.sql"

        with open(file_name, mode="w", encoding="utf-8") as wf:
            wf.write("SET IDENTITY_INSERT dbo.tbl_Product ON;\n")
            wf.write("\n")
            wf.write("DELETE FROM dbo.tbl_Product;\n")
            wf.write("\n")

            index = 0
            for product in self.get_product_list():
                index += 1

                if product.product_title is not None:
                    product.product_title = product.product_title.replace("'", "''")

                if product.product_content is not None:
                    product.product_content = product.product_content.replace("\n", "").replace("'", "''")

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_Product("
                sql_text += "     ID"
                sql_text += ",    CategoryID"
                sql_text += ",    ProductOldID"
                sql_text += ",    ProductTitle"
                sql_text += ",    ProductContent"
                sql_text += ",    ProductSKU"
                sql_text += ",    ProductStock"
                sql_text += ",    StockStatus"
                sql_text += ",    ManageStock"
                sql_text += ",    Regular_Price"
                sql_text += ",    CostOfGood"
                sql_text += ",    Retail_Price"
                sql_text += ",    ProductImage"
                sql_text += ",    ProductType"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ",    Materials"
                sql_text += ",    MinimumInventoryLevel"
                sql_text += ",    MaximumInventoryLevel"
                sql_text += ",    SupplierID"
                sql_text += ",    SupplierName"
                sql_text += ",    ProductStyle"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(product.id)
                sql_text += ",    " + CommonSql.f_str_value(product.category_id)
                sql_text += ",    " + CommonSql.f_str_value(product.product_old_id)
                sql_text += ",    " + CommonSql.f_str_value(product.product_title)
                sql_text += ",    " + CommonSql.f_str_value(product.product_content)
                sql_text += ",    " + CommonSql.f_str_value(product.product_sku)
                sql_text += ",    " + CommonSql.f_str_value(product.product_stock)
                sql_text += ",    " + CommonSql.f_str_value(product.stock_status)
                sql_text += ",    " + CommonSql.f_str_value(product.manage_stock)
                sql_text += ",    " + CommonSql.f_str_value(product.regular_price)
                sql_text += ",    " + CommonSql.f_str_value(product.cost_of_good)
                sql_text += ",    " + CommonSql.f_str_value(product.retail_price)
                sql_text += ",    " + CommonSql.f_str_value(product.product_image)
                sql_text += ",    " + CommonSql.f_str_value(product.product_type)
                sql_text += ",    " + CommonSql.f_str_value(product.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(product.created_date)
                sql_text += ",    " + CommonSql.f_str_value(product.created_by)
                sql_text += ",    " + CommonSql.f_str_value(product.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(product.modified_by)
                sql_text += ",    " + CommonSql.f_str_value(product.materials)
                sql_text += ",    " + CommonSql.f_str_value(product.minimum_inventory_level)
                sql_text += ",    " + CommonSql.f_str_value(product.maximum_inventory_level)
                sql_text += ",    " + CommonSql.f_str_value(product.supplier_id)
                sql_text += ",    " + CommonSql.f_str_value(product.supplier_name)
                sql_text += ",    " + CommonSql.f_str_value(product.product_style)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_Product OFF;\n")
