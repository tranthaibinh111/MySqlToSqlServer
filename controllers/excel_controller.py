from openpyxl import load_workbook


class ExcelController:
    def __init__(self):
        raise Exception("Class ExcelController khong the khoi tao")

    @staticmethod
    def get_data(file_name, sheet_name):
        if file_name == '':
            raise Exception("Chua cho thong tin file excel")

        try:
            wb = load_workbook(file_name, read_only=True)
            ws = wb[sheet_name]

            index = 0
            data = []

            for row in ws.rows:
                index += 1

                # Khong doc dong title
                if index == 1:
                    continue

                data_row = []
                for cell in row:
                    data_row.append(cell.value)

                data.append(data_row)

            return data

        except Exception as e:
            print(e)
