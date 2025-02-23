from datetime import datetime


class ProductImageEntity:
    def __init__(self):
        self.id = None
        self.product_id = None
        self.product_image = None
        self.is_hidden = 0
        self.created_date = datetime.now()
        self.created_by = "admin"
        self.modified_date = None
        self.modified_by = None
