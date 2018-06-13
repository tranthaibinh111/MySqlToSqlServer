import os
from common.sql import CommonSql
from controllers import ExcelController
from models import CategoryEntity


class CategoryController:
    def __init__(self, file_name, sheet_name):
        self.__file_name = file_name
        self.__sheet_name = sheet_name
        self.categories = []

        self.__mapping()

    def __mapping(self):
        data = ExcelController.get_data(self.__file_name, self.__sheet_name)

        for row in data:
            category = CategoryEntity()

            category.id = row[0]
            category.category_name = row[1]
            category.category_description = row[2]
            category.category_level = row[3]
            category.parent_id = row[4]
            category.is_hidden = row[5]

            self.categories.append(category)

    def get_category_id(self, category_name):
        result = None

        for category in self.categories:
            if category.category_name.upper() == category_name.upper():
                result = category.id
                break

        return result

    def export_sql(self):
        file_name = os.getcwd() + "\\export_sql\\category.sql"

        with open(file_name, mode="w", encoding="utf-8") as wf:
            wf.write("SET IDENTITY_INSERT dbo.tbl_Category ON;\n")
            wf.write("\n")
            wf.write("DELETE FROM dbo.tbl_Category;\n")
            wf.write("\n")

            index = 0
            for category in self.categories:
                index += 1

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_Category("
                sql_text += "     ID"
                sql_text += ",    CategoryName"
                sql_text += ",    CategoryDescription"
                sql_text += ",    CategoryLevel"
                sql_text += ",    ParentID"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(category.id)
                sql_text += ",    " + CommonSql.f_str_value(category.category_name)
                sql_text += ",    " + CommonSql.f_str_value(category.category_description)
                sql_text += ",    " + CommonSql.f_str_value(category.category_level)
                sql_text += ",    " + CommonSql.f_str_value(category.parent_id)
                sql_text += ",    " + CommonSql.f_str_value(category.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(category.create_date)
                sql_text += ",    " + CommonSql.f_str_value(category.create_by)
                sql_text += ",    " + CommonSql.f_str_value(category.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(category.modified_by)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_Category OFF;\n")
