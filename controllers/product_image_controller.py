import os
from common.sql.common_sql import CommonSql
from models.product_image_entity import ProductImageEntity


class ProductImageController:
    def __init__(self, product_controller):
        self.product_images = []
        self.__mapping(product_controller)

    def __mapping(self, product_controller):

        index = 0

        for product in product_controller.get_product_list():
            if product.product_images is not None:
                for image in product.product_images:

                    index += 1
                    product_image = ProductImageEntity()

                    product_image.id = index
                    product_image.product_id = product.id
                    product_image.product_image = image
                    product_image.is_hidden = product.is_hidden
                    product_image.created_date = product.created_date
                    product_image.created_by = product.created_by
                    product_image.modified_date = product.modified_date
                    product_image.modified_by = product.modified_by

                    self.product_images.append(product_image)

    def export_sql(self):
        file_name = os.getcwd() + "\\export_sql\\product_image.sql"

        with open(file_name, mode="w+", encoding="utf-8") as wf:
            wf.write("SET IDENTITY_INSERT dbo.tbl_ProductImage ON;\n")
            wf.write("\n")
            wf.write("DELETE FROM dbo.tbl_ProductImage;\n")
            wf.write("\n")

            index = 0
            for product_image in self.product_images:
                index += 1

                sql_text = ""
                sql_text += "INSERT INTO dbo.tbl_ProductImage("
                sql_text += "     ID"
                sql_text += ",    ProductID"
                sql_text += ",    ProductImage"
                sql_text += ",    IsHidden"
                sql_text += ",    CreatedDate"
                sql_text += ",    CreatedBy"
                sql_text += ",    ModifiedDate"
                sql_text += ",    ModifiedBy"
                sql_text += ") VALUES("
                sql_text += "     " + CommonSql.f_str_value(product_image.id)
                sql_text += ",    " + CommonSql.f_str_value(product_image.product_id)
                sql_text += ",    " + CommonSql.f_str_value(product_image.product_image)
                sql_text += ",    " + CommonSql.f_str_value(product_image.is_hidden)
                sql_text += ",    " + CommonSql.f_str_value(product_image.created_date)
                sql_text += ",    " + CommonSql.f_str_value(product_image.created_by)
                sql_text += ",    " + CommonSql.f_str_value(product_image.modified_date)
                sql_text += ",    " + CommonSql.f_str_value(product_image.modified_by)
                sql_text += ");\n"

                wf.write(sql_text)

                if index > 100:
                    wf.write("GO\n")
                    index = 0

            wf.write("SET IDENTITY_INSERT dbo.tbl_ProductImage OFF;\n")
