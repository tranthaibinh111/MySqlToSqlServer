from datetime import datetime


class CommonSql:
    @staticmethod
    def f_str_value(parameter):
        result = None

        if parameter is None:
            result = "NULL"
        else:
            if type(parameter) is str:
                result = "N'" + parameter + "'"
            elif type(parameter) is int:
                result = str(parameter)
            elif type(parameter) is float:
                result = str(parameter)
            elif type(parameter) is datetime:
                result = "CAST('" + str(parameter) + "' AS DATETIME2)"
            else:
                result = None

        if result is None:
            print(str(parameter) + ": " + str(type(parameter)))
            raise Exception("Kieu parameter khong ton tai trong dinh nghia ham common")
        else:
            return result
