from datetime import datetime


class ProductEntity:
    def __init__(self):
        self.id = None
        self.category_id = None
        self.product_old_id = None
        self.product_title = None
        self.product_content = None
        self.product_sku = None
        self.product_stock = 0
        self.stock_status = 0
        self.manage_stock = 1
        self.regular_price = 0
        self.cost_of_good = 0
        self.retail_price = 0
        self.product_image = None
        self.product_type = 0
        self.is_hidden = 0
        self.created_date = datetime.now()
        self.created_by = "admin"
        self.modified_date = None
        self.modified_by = None
        self.materials = None
        self.minimum_inventory_level = None
        self.maximum_inventory_level = None
        self.supplier_id = None
        self.supplier_name = None
        self.product_style = None

        # Dùng cho insert tabel ProductImage
        self.product_images = None