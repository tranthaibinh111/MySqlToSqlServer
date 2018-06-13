from datetime import datetime


class CategoryEntity:
    def __init__(self):
        self.id = None
        self.category_name = None
        self.category_description = None
        self.category_level = None
        self.parent_id = None
        self.is_hidden = None
        self.create_date = datetime.now()
        self.create_by = "admin"
        self.modified_date = None
        self.modified_by = None
