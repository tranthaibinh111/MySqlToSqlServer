import os
from controllers import CategoryController, \
    InOutProductVariableController, \
    ProductController, \
    ProductImageController, \
    ProductVariableController, \
    ProductVariableValueController, \
    VariableValueController

if __name__ == "__main__":
    root_path = os.getcwd()

    # Lấy thông tin các danh mục cần thiết
    print("Lấy thông tin các danh mục cần thiết")
    category_file = {
        "path_full": root_path + "\\import_excel\\20180619_category.xlsx",
        "sheet": "category"
    }

    variable_value_file = {
        "path_full": root_path + "\\import_excel\\20180619_variable-value.xlsx",
        "sheet": "variable-value"
    }

    category_controller = CategoryController(category_file["path_full"], category_file["sheet"])
    variable_value_controller = VariableValueController(variable_value_file["path_full"], variable_value_file["sheet"])

    # Đọc thông tin từ file excel cần import
    print("Đọc thông tin từ file excel cần import")
    product_file = {
        "path_full": root_path + "\\import_excel\\20180619_san-pham.xlsx",
        "sheet": "san-pham"
    }
    product_variable_file = {
        "path_full": root_path + "\\import_excel\\20180619_bien-the.xlsx",
        "sheet": "bien-the"
    }

    product_controller = ProductController(product_file["path_full"], product_file["sheet"], category_controller)
    product_image_controller = ProductImageController(product_controller)
    product_variable_controller = ProductVariableController(product_variable_file["path_full"],
                                                            product_variable_file["sheet"],
                                                            product_controller)
    product_variable_value_controller = ProductVariableValueController(product_variable_controller,
                                                                       variable_value_controller)
    in_out_product_variable_controller = InOutProductVariableController(product_controller,
                                                                        product_variable_controller,
                                                                        variable_value_controller)

    # Update thông tin table chính từ table phụ
    print("Update thông tin table chính từ table phụ")
    product_controller.update_product_variable(product_variable_controller.product_parents)

    # Xuất file sql import
    print("Xuất file sql import")
    category_controller.export_sql()
    variable_value_controller.export_sql()
    product_controller.export_sql()
    product_image_controller.export_sql()
    product_variable_controller.export_sql()
    product_variable_value_controller.export_sql()
    in_out_product_variable_controller.export_sql()

    print("Ket thuc chuong trinh")