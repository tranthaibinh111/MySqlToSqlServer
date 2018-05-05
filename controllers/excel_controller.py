from openpyxl import load_workbook


class ExcelController:
    def __init__(self):
        raise Exception("Class ExcelController khong the khoi tao")

    @staticmethod
    def get_data(file_name, sheet_name="Sheet1"):
        if file_name == '':
            raise Exception("Chua cho thong tin file excel")

        try:
            wb = load_workbook(file_name, read_only=True)
            ws = wb[sheet_name]

            index = 0
            datas = []

            for row in ws.rows:
                index += 1

                # Khong doc dong title
                if index == 1:
                    continue

                data = []
                for cell in row:
                    data.append(cell.value)

                datas.append(data)

            return datas

        except Exception as e:
            print(e)
