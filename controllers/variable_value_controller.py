import os
from common.sql import CommonSql
from models import VariableValueEntity
from controllers import ExcelController


class VariableValueController:
    def __init__(self, file_name, sheet_name):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.variable_values = []

        self.__mapping()

    def __mapping(self):
        data = ExcelController.get_data(self.__file_name, self.__sheet_name)

        for row in data:
            variable_value = VariableValueEntity()

            variable_value.id = row[0]
            variable_value.variable_id = row[1]
            variable_value.variable_name = row[2]
            variable_value.variable_value = row[3]
            variable_value.variable_value_text = row[9]
            variable_value.sku_text = row[10]

            self.variable_values.append(variable_value)

    def get_variable_value_info(self, variable_name, variable_value_text):
        result = None

        for variable_value in self.variable_values:
            if variable_value.variable_name.upper() == variable_name.upper() \
                    and str(variable_value.variable_value_text).upper() == str(variable_value_text).upper():
                result = {
                            'id': variable_value.id,
                            'variable_name': variable_value.variable_name,
                            'variable_value': variable_value.variable_value,
                            'sku_text': variable_value.sku_text
                        }
                break

        return result

    def export_sql(self):
        file_name = os.getcwd() + "\\export_sql\\variable_value.sql"

        with open(file_name, mode="w", encoding="utf-8") as wf:
            wf.write("SET IDENTITY_INSERT dbo.tbl_VariableValue ON;\n")
            wf.write("\n")
            wf.write("DELETE FROM dbo.tbl_VariableValue;\n")
            wf.write("\n")

            index = 0
            for variable_value in self.variable_values:
                index += 1

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_VariableValue("
                sql_text += "     ID"
                sql_text += ",    VariableID"
                sql_text += ",    VariableName"
                sql_text += ",    VariableValue"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ",    VariableValueText"
                sql_text += ",    SKUText"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(variable_value.id)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.variable_id)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.variable_name)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.variable_value)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.create_date)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.create_by)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.modified_by)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.variable_value_text)
                sql_text += ",    " + CommonSql.f_str_value(variable_value.sku_text)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_VariableValue OFF;\n")
