import pymysql as sql

class DB:
    def __init__(self):
        # Параметры подключения
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '1111'
        self.db_name = 'Paws_Beans'

        self.connection = None
        self.cursor = None

    def connect(self):
        """Подключение к MySQL серверу"""
        try:
            self.connection = sql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                charset='utf8mb4',
                cursorclass=sql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("Успешное подключение к MySQL серверу")
        except sql.Error as e:
            print(f"Ошибка подключения: {e}")

    def add_user(self, username, mail=None):
        """Добавление пользователя"""
        try:
            query = """
            INSERT INTO `users` (username, mail, date_registration)
            VALUES (%s, %s, NOW())
            """
            params = (username, mail)

            self.cursor.execute(query, params)
            self.connection.commit()

            user_id = self.cursor.lastrowid
            print(f"Пользователь '{username}' добавлен с ID: {user_id}")
            return user_id

        except sql.Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            self.connection.rollback()
            return None

    def close(self):
        """Закрытие соединения"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Соединение закрыто")


db = DB()
db.connect()

db.add_user("ivan_petrov", "ivan@example.com")
db.add_user("maria_sidorova", "maria@example.com")
db.add_user("alex_smirnov")

db.close()