from models.category_entity import CategoryEntity
from controllers.excel_controller import ExcelController


class CategoryController:
    def __init__(self, file_name, sheet_name='Sheet1'):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.categorys = []

        self.__mapping()

    def __mapping(self):
        datas = ExcelController.get_data(self.__file_name, self.__sheet_name)

        for row in datas:
            category = CategoryEntity()

            category.id = row[0]
            category.category_name = row[1]
            category.category_description = row[2]
            category.category_level = row[3]
            category.parent_id = row[4]
            category.is_hidden = row[5]
            category.create_date = row[6]
            category.create_by = row[7]
            category.modified_date = row[8]
            category.modified_by = row[9]

            self.categorys.append(category)

    def get_category_id(self, category_name):
        result = None

        for category in self.categorys:
            if category.category_name.upper() == category_name.upper():
                result = category.id
                break

        return result
