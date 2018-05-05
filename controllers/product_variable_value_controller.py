import os
from common.sql.common_sql import CommonSql
from models.product_variable_value_entity import ProductVariableValueEntity


class ProductVariableValueController:
    def __init__(self, product_variable_controller, variable_value_controller):
        self.product_variable_values = []
        self.__mapping(product_variable_controller, variable_value_controller)

    def __mapping(self, product_variable_controller, variable_value_controller):

        index = 0

        for product_variable in product_variable_controller.product_variables:
            product_variable_column = []

            if product_variable.color is not None and product_variable.size is not None:
                product_variable_column = ["Màu", "Size"]
            elif product_variable.color is not None:
                product_variable_column = ["Màu"]
            elif product_variable.size is not None:
                product_variable_column = ["Size"]

            for column in product_variable_column:
                index += 1
                product_variable_value = ProductVariableValueEntity()

                product_variable_value.id = index
                product_variable_value.product_variable_id = product_variable.id

                if column == "Màu":
                    info_variable_value = variable_value_controller.get_variable_value_info(column,
                                                                                            product_variable.color)
                else:
                    info_variable_value = variable_value_controller.get_variable_value_info(column,
                                                                                            product_variable.size)

                if info_variable_value is None:
                    print(column, " ", product_variable.color, " ", product_variable.size)
                    raise Exception("Color or Size khong ton tai trong table tbl_VariableValue")

                product_variable_value.product_variable_sku = product_variable.sku
                product_variable_value.variable_value_id = info_variable_value["id"]
                product_variable_value.variable_name = info_variable_value["variable_name"]
                product_variable_value.variable_value = info_variable_value["variable_value"]
                product_variable_value.is_hidden = product_variable.is_hidden
                product_variable_value.created_date = product_variable.created_date
                product_variable_value.created_by = product_variable.created_by
                product_variable_value.modified_date = product_variable.modified_date
                product_variable_value.modified_by = product_variable.modified_by

                self.product_variable_values.append(product_variable_value)

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

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_ProductVariableValue("
                sql_text += "     ID"
                sql_text += ",    ProductVariableID"
                sql_text += ",    ProductvariableSKU"
                sql_text += ",    VariableValueID"
                sql_text += ",    VariableName"
                sql_text += ",    VariableValue"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(product_variable_value.id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.product_variable_id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.product_variable_sku)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.variable_value_id)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.variable_name)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.variable_value)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.created_date)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.created_by)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(product_variable_value.modified_by)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_ProductVariableValue OFF;\n")
