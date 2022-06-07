from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_device(deviceid):
        sql = "SELECT * FROM device WHERE deviceid = %s"
        params = [deviceid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_devices():
        sql = "SELECT * FROM device"
        return Database.get_rows(sql)

    @staticmethod
    def read_historiek():
        sql = "SELECT * FROM historiek"
        return Database.get_rows(sql)

    @staticmethod
    def insert_historiek(value, deviceid, actieid, commentaar=None):
        sql = "INSERT INTO historiek (waarde, commentaar, deviceid, actieid) VALUES (%s, %s, %s, %s)"
        params = [value, commentaar, deviceid, actieid]
        return Database.execute_sql(sql, params)
