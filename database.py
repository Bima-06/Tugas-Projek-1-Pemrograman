import pymysql

class Database:
    def __init__(self):
        self.config = {
            "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            "port": 4000,
            "user": "248ANe4PUz9mf17.root",
            "password": "wn5umMhh5nYxJJCi",
            "database": "peminjaman_alat",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": False,
            "ssl": {"ssl": True}
        }

    def connect(self):
        return pymysql.connect(**self.config)