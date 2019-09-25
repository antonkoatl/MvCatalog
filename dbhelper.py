import sqlite3


class DBHelper:
    db_file = "data.db"

    sql_create_movies_table = """ CREATE TABLE IF NOT EXISTS movies (
                                            id integer PRIMARY KEY,
                                            name text,
                                            orig_name text NOT NULL UNIQUE,
                                            year integer,
                                            country text,
                                            genre text,
                                            length integer,
                                            rating text,
                                            director text,
                                            script text,
                                            actors text,
                                            description text
                                        ); """

    sql_create_files_table = """CREATE TABLE IF NOT EXISTS files (
                                        id integer PRIMARY KEY,
                                        movie_id integer NOT NULL,
                                        name text NOT NULL,
                                        size text,
                                        resolution text,
                                        codec text,
                                        bitrate integer,
                                        length integer,
                                        audio text,
                                        subs text,
                                        FOREIGN KEY (movie_id) REFERENCES movies (id)
                                    );"""

    def __init__(self):
        self.conn = None
        self.cursor_list = None
        self.list_last_element = None

    def connect(self):
        self.create_connection(self.db_file)
        self.create_table(self.sql_create_movies_table)
        self.create_table(self.sql_create_files_table)

    def get_movies(self):
        return self.get_movies_data()

    def get_list(self):
        return self.get_list_data()

    def create_connection(self, db_file):
        self.conn = None

        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
            if self.conn:
                self.conn.close()

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def fill_test_data(self):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM movies")
            c.execute("INSERT INTO movies VALUES (NULL, NULL, 'Glow', '2019', 'Russia', 'Genre', '0', '0+', 'Andy Hunter', '', '', 'Some description')")
            c.execute("INSERT INTO movies VALUES (NULL, 'Аватар', 'Avatar', '2009', 'Великобритания,США', 'Боевик,Драма,Приключения,Фантастика', '162', 'PG-13', 'Andy Hunter', 'Джеймс Кэмерон', 'Джеймс Кэмерон', 'Some description')")
            c.execute("DELETE FROM files")
            c.execute("INSERT INTO files VALUES (NULL, '1', 'Glow.avi', '0', '320x240', 'MPEG', '1000', '0', 'English', NULL)")
            c.execute("INSERT INTO files VALUES (NULL, '1', 'Glow.avi', '0', '320x240', 'MPEG', '1000', '0', 'English', NULL)")
            c.execute("INSERT INTO files VALUES (NULL, '1', 'Glow.avi', '0', '320x240', 'MPEG', '1000', '0', 'English', NULL)")
            c.execute("INSERT INTO files VALUES (NULL, '1', 'Glow.avi', '0', '320x240', 'MPEG', '1000', '0', 'English', NULL)")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def get_movies_data(self):
        try:
            c = self.conn.cursor()
            sql = "SELECT * FROM movies"
            c.execute(sql)
            result = [c.fetchone() for i in range(10)]
            return result
        except sqlite3.Error as e:
            print(e)

    def get_list_data(self):
        try:
            result = []

            if self.cursor_list == None:
                self.cursor_list = self.conn.cursor()
                sql = "SELECT * FROM files INNER JOIN movies ON files.movie_id = movies.id"
                self.cursor_list.execute(sql)
            else:
                result.append(self.list_last_element)

            result += [self.cursor_list.fetchone() for i in range(2)]
            self.list_last_element = result[-1]

            if None in result:
                self.cursor_list = None

            return result
        except sqlite3.Error as e:
            print(e)
