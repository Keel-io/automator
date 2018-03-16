import psycopg2
import sys
import os

# Reference to testing.postgresql database instance
db = None

# Connection to the database used to set the database state before running each
# test
db_con = None

# Map of database connection parameters passed to the functions we're testing
db_conf = None

class Cleaner:
    def __init__(self, database_url, ):
        ''' Constructor for this class. '''

        self.database_url = database_url

    def runInstaller(self):
        # The installer code goes here
        con = psycopg2.connect(self.database_url)
        cur = con.cursor()
        cur.execute("CREATE TABLE automator_logs (id SERIAL PRIMARY KEY, category VARCHAR(150), start_time TIMESTAMP, end_time TIMESTAMP, error TEXT);")
        cur.execute("CREATE TABLE automator_queries (id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150), description VARCHAR(150),  status VARCHAR(150), code TEXT, created_at TIMESTAMP, updated_at TIMESTAMP, rank INTEGER);")
        con.commit()
        con.close()
        print('Automator was successfully installed.')

    def runUninstaller(self):
        # The uninstaller code goes here
        con = psycopg2.connect(self.database_url)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS automator_logs, automator_queries;")
        con.commit()
        con.close()
        print('Automator was successfully uninstalled')

    def runQueries(self, category='All'):
        # The code below executes the SQL queries in table 'automator_queries' using a single Postgres Transaction.
        all_sql_queries = """
            DO
            $do$
              declare
                r record;
            BEGIN
                FOR r IN SELECT * FROM automator_queries WHERE status = 'Live' ORDER BY rank
                LOOP
                    EXECUTE format(r.code);
            END LOOP;
            END
            $do$;
        """

        sql_queries_in_category = """
            DO
            $do$
            declare
              r record;
            BEGIN
              FOR r IN SELECT * FROM automator_queries WHERE category = '%s' AND status = 'Live' ORDER BY rank
              LOOP
                  EXECUTE format(r.code);
            END LOOP;
            END
            $do$;
        """

        con = psycopg2.connect(self.database_url)
        cur = con.cursor()

        cur.execute("INSERT INTO automator_logs (category, start_time) VALUES ('%s', current_timestamp )" % category)

        try:
            if category == 'All':
                cur.execute(all_sql_queries)
            else:
                cur.execute(sql_queries_in_category % 'Users')

                print('Queries Ran!')
            cur.execute("UPDATE automator_logs SET start_time = current_timestamp WHERE id = (SELECT max(id) FROM automator_logs);", category)
            con.commit()

        except Exception as inst:
            con.commit()
            cur.execute("UPDATE automator_logs SET error = inst WHERE id = (SELECT max(id) FROM automator_logs);", category)
            con.commit()

        con.close()
