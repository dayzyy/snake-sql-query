from mysql.connector import pooling, Error

class Database:
    pool = None

    @classmethod
    def init_pool(cls, host, user, password, database, pool_size=5):
        if cls.pool is None:
            cls.pool = pooling.MySQLConnectionPool(
                pool_name=f"pool_{user}_{database}",
                pool_size=pool_size,
                pool_reset_session=True,
                host=host,
                user=user,
                password=password,
                database=database
            )

    @classmethod
    def execute(cls, query, params=None, commit=False, fetchone=False, fetchall=False):
        if cls.pool is None:
            raise RuntimeError("Pool is not initialized. Call init_pool first.")

        conn = cls.pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def execute_many(cls, query, params=None, commit=False, fetchone=False, fetchall=False):
        if cls.pool is None:
            raise RuntimeError("Pool is not initialized. Call init_pool first.")

        conn = cls.pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.executemany(query, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
