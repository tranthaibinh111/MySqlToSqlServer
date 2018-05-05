import os
from common.sql.common_sql import CommonSql
from models.in_out_product_variable_entity import InOutProductVariableEntity


class InOutProductVariableController:
    def __init__(self, product_controller, product_variable_controller, variable_value_controller):
        self.in_out_product_variable = []
        print(len(product_controller.product_simples))
        print(len(product_variable_controller.product_variables))

        self.__mapping(product_controller, product_variable_controller, variable_value_controller)

    def __mapping(self, product_controller, product_variable_controller, variable_value_controller):
        index = 0

        for data in product_controller.product_simples:
            index += 1
            product = InOutProductVariableEntity()

            product.id = index
            product.product_id = data.id
            product.product_variable_id = 0
            product.product_variable_name = None
            product.product_variable_value = None
            product.quantity = data.product_stock
            product.product_type = 1
            product.sku = data.product_sku
            product.product_variable = None
            product.parent_id = data.id

            self.in_out_product_variable.append(product)

        for data in product_variable_controller.product_variables:
            index += 1
            product = InOutProductVariableEntity()

            product.id = index
            product.product_id = 0
            product.product_variable_id = data.id

            if data.color is not None and data.size:
                product_variable_name = "Màu|Size"

                color = variable_value_controller.get_variable_value_info("Màu", data.color)
                size = variable_value_controller.get_variable_value_info("Size", data.size)
                product_variable_value = color["variable_value"] + "|" + size["variable_value"]
            else:
                if data.color is not None:
                    product_variable_name = "Màu|"

                    color = variable_value_controller.get_variable_value_info("Màu", data.color)
                    product_variable_value = color["variable_value"] + "|"
                elif data.size is not None:
                    product_variable_name = "Size|"

                    size = variable_value_controller.get_variable_value_info("Size", data.size)
                    product_variable_value = size["variable_value"] + "|"
                else:
                    product_variable_name = None
                    product_variable_value = None

            product.product_variable_name = product_variable_name
            product.product_variable_value = product_variable_value
            product.quantity = data.stock
            product.product_type = 2
            product.sku = data.sku
            product.product_variable = product_variable_value
            product.product_id = data.product_id

            self.in_out_product_variable.append(product)

    def export_sql(self):
        file_name = os.getcwd() + "\\export_sql\\in_out_product_variable.sql"

        with open(file_name, mode="w+", encoding="utf-8") as wf:
            wf.write("SET IDENTITY_INSERT dbo.tbl_InOutProductVariable ON;\n")
            wf.write("\n")
            wf.write("DELETE FROM dbo.tbl_InOutProductVariable;\n")
            wf.write("\n")

            index = 0
            for product in self.in_out_product_variable:
                index += 1

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_InOutProductVariable("
                sql_text += "     ID"
                sql_text += ",    AgentID"
                sql_text += ",    ProductID"
                sql_text += ",    ProductVariableID"
                sql_text += ",    ProductVariableName"
                sql_text += ",    ProductVariableValue"
                sql_text += ",    Quantity"
                sql_text += ",    QuantityCurrent"
                sql_text += ",    Type"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ",    ProductType"
                sql_text += ",    Note"
                sql_text += ",    OrderID"
                sql_text += ",    SessionInOutID"
                sql_text += ",    Status"
                sql_text += ",    ProductName"
                sql_text += ",    SKU"
                sql_text += ",    ProductImage"
                sql_text += ",    ProductVariable"
                sql_text += ",    MoveProID"
                sql_text += ",    ParentID"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(product.id)
                sql_text += ",    " + CommonSql.f_str_value(product.agent_id)
                sql_text += ",    " + CommonSql.f_str_value(product.product_id)
                sql_text += ",    " + CommonSql.f_str_value(product.product_variable_id)
                sql_text += ",    " + CommonSql.f_str_value(product.product_variable_name)
                sql_text += ",    " + CommonSql.f_str_value(product.product_variable_value)
                sql_text += ",    " + CommonSql.f_str_value(product.quantity)
                sql_text += ",    " + CommonSql.f_str_value(product.quantity_current)
                sql_text += ",    " + CommonSql.f_str_value(product.type)
                sql_text += ",    " + CommonSql.f_str_value(product.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(product.created_date)
                sql_text += ",    " + CommonSql.f_str_value(product.created_by)
                sql_text += ",    " + CommonSql.f_str_value(product.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(product.modified_by)
                sql_text += ",    " + CommonSql.f_str_value(product.product_type)
                sql_text += ",    " + CommonSql.f_str_value(product.note)
                sql_text += ",    " + CommonSql.f_str_value(product.order_id)
                sql_text += ",    " + CommonSql.f_str_value(product.session_in_out_id)
                sql_text += ",    " + CommonSql.f_str_value(product.status)
                sql_text += ",    " + CommonSql.f_str_value(product.product_name)
                sql_text += ",    " + CommonSql.f_str_value(product.sku)
                sql_text += ",    " + CommonSql.f_str_value(product.product_image)
                sql_text += ",    " + CommonSql.f_str_value(product.product_variable)
                sql_text += ",    " + CommonSql.f_str_value(product.move_pro_id)
                sql_text += ",    " + CommonSql.f_str_value(product.parent_id)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_InOutProductVariable OFF;\n")