from models.variable_value_entity import VariableValueEntity
from controllers.excel_controller import ExcelController


class VariableValueController:
    def __init__(self, file_name, sheet_name='Sheet1'):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.variable_values = []

        self.__mapping()

    def __mapping(self):
        datas = ExcelController.get_data(self.__file_name, self.__sheet_name)

        for row in datas:
            variable_value = VariableValueEntity()

            variable_value.id = row[0]
            variable_value.variable_id = row[1]
            variable_value.variable_name = row[2]
            variable_value.variable_value = row[3]
            variable_value.is_hidden = row[4]
            variable_value.create_date = row[5]
            variable_value.create_by = row[6]
            variable_value.modified_date = row[7]
            variable_value.modified_by = row[8]
            variable_value.variable_value_text = row[9]
            variable_value.sku_text = row[10]

            self.variable_values.append(variable_value)

    def get_variable_value_info(self, variable_name, variable_value_text):
        result = None

        for variable_value in self.variable_values:
            if variable_value.variable_name.upper() == variable_name.upper() and str(variable_value.variable_value_text).upper() == str(variable_value_text).upper():
                result = {
                            'id': variable_value.id,
                            'variable_name': variable_value.variable_name,
                            'variable_value': variable_value.variable_value,
                            'sku_text': variable_value.sku_text
                        }
                break

        return result
