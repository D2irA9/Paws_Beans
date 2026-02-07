import pymysql as sql, json

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

    def add_user(self, username):
        """Добавление пользователя"""
        try:
            query = """
                INSERT INTO `users` (username)
                VALUES (%s)
            """
            params = (username)

            self.cursor.execute(query, params)
            self.connection.commit()

            user_id = self.cursor.lastrowid
            print(f"Пользователь '{username}' добавлен с ID: {user_id}")
            return user_id

        except sql.Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            self.connection.rollback()
            return None

    def get_nps_id(self, nps_name):
        """ Получение ID Nps """
        try:
            query = "SELECT id FROM nps WHERE name = %s"
            self.cursor.execute(query, (nps_name,))
            result = self.cursor.fetchone()
            return result['id'] if result else None
        except sql.Error as e:
            print(f"Ошибка получения ID NPS: {e}")
            return None

    def add_statistics(self, user_id, nps_name, order_data, result):
        """ Добавление статистики """
        try:
            order_json = json.dumps(order_data, ensure_ascii=False)

            nps_id = self.get_nps_id(nps_name)

            if nps_id is None:
                print(f"Имя Nps '{nps_name}' не найден")
                nps_id = 2

            query = """
                INSERT INTO `statistics` (id_user, id_nps, `order`, result)
                VALUES (%s, %s, %s, %s)
            """
            params = (user_id, nps_id, order_json, result)

            self.cursor.execute(query, params)
            self.connection.commit()

            stat_id = self.cursor.lastrowid
            print(f"✅ Статистика сохранена (ID: {stat_id})")
            print(f"   Пользователь: {user_id}, NPS: {nps_name} (ID: {nps_id})")
            print(f"   Результат: {result}")
            return stat_id
        except Exception as e:
            print(f"❌ Ошибка сохранения статистики: {e}")
            self.connection.rollback()
            return None

    def get_user_statistics(self, user_id, limit=20):
        """Получить статистику пользователя"""
        try:
            query = """
                SELECT 
                    s.id,
                    s.id_user,
                    s.id_nps,
                    n.name as nps_name,
                    s.`order`,
                    s.result,
                    DATE_FORMAT(s.created_at, '%%d.%%m.%%Y %%H:%%i') as order_time
                FROM statistics s
                LEFT JOIN nps n ON s.id_nps = n.id
                WHERE s.id_user = %s
                ORDER BY s.id DESC
                LIMIT %s
            """
            self.cursor.execute(query, (user_id, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            return []

    def close(self):
        """Закрытие соединения"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Соединение закрыто")


db = DB()