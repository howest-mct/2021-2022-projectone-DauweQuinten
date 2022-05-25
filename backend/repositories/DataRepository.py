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
    def read_one_device(deviceid):
        sql = "SELECT * FROM device WHERE deviceid = %s"
        params = [deviceid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_all_devices():
        sql = "SELECT * FROM device"
        return Database.get_rows(sql)
