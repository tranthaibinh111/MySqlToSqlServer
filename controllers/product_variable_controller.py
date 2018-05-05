import os
from common.sql.common_sql import CommonSql
from models.product_variable_entity import ProductVariableEntity
from controllers.excel_controller import ExcelController


class ProductVariableController:
    def __init__(self, file_name, sheet_name, product_controller):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.product_variables = []
        self.product_parents = []

        self.__mapping(product_controller)

    def __mapping(self, product_controller):
        data = ExcelController.get_data(self.__file_name, self.__sheet_name)

        index = 0

        for row in data:
            index += 1
            product_variable = ProductVariableEntity()

            product_variable.id = index
            product_variable.parent_sku = row[0]
            product_variable.sku = row[4]

            product_variable.product_id = product_controller.get_product_variable_id(product_variable.parent_sku)
            if product_variable.product_id is None:
                print(product_variable.parent_sku)
                raise Exception("ParentSku khong ton tai trong table tbl_Product")

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
            product_variable.minimum_inventory_level = 2
            product_variable.maximum_inventory_level = 10

            self.product_variables.append(product_variable)
            self.__calculator_product(product_variable.parent_sku,
                                      product_variable.stock,
                                      product_variable.regular_price)

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
            self.product_parents.append({"parent_sku": parent_sku, "stock": stock, "regular_price": regular_price})

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

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_ProductVariable("
                sql_text += "     ID"
                sql_text += ",    ProductID"
                sql_text += ",    ParentSKU"
                sql_text += ",    SKU"
                sql_text += ",    Stock"
                sql_text += ",    StockStatus"
                sql_text += ",    Regular_Price"
                sql_text += ",    CostOfGood"
                sql_text += ",    Image"
                sql_text += ",    ManageStock"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ",    color"
                sql_text += ",    size"
                sql_text += ",    RetailPrice"
                sql_text += ",    MinimumInventoryLevel"
                sql_text += ",    MaximumInventoryLevel"
                sql_text += ",    SupplierID"
                sql_text += ",    SupplierName"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(product_variable.id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.product_id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.parent_sku)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.sku)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.stock)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.stock_status)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.regular_price)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.cost_of_good)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.image)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.manage_stock)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.created_date)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.created_by)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.modified_by)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.color)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.size)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.retail_price)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.minimum_inventory_level)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.maximum_inventory_level)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.supplier_id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable.supplier_name)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariable OFF;\n")
