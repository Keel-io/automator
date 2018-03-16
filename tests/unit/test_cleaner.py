import psycopg2
from datetime import date
from tests import *
from tests.helpers import *
from nose.tools import eq_
from automator import Cleaner
import testing.postgresql
import mock


class TestCleaner(unittest.TestCase):

    def setUp(self):
        """ Module level set-up called once before any tests in this file are
        executed.  Creates a temporary database and sets it up """
        global db, db_con, db_conf
        db = testing.postgresql.Postgresql()
        # Get a map of connection parameters for the database which can be passed
        # to the functions being tested so that they connect to the correct
        # database
        db_conf = db.url()
        # Create a connection which can be used by our test functions to set and
        # query the state of the database
        db_con = psycopg2.connect(db_conf)
        # Commit changes immediately to the database
        db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def test_runInstaller(self):
        # Attempt to setup the database
        myCleaner = Cleaner(db_conf)
        myCleaner.runInstaller()

        # Inspect the state of the database and make some assertions
        with db_con.cursor() as cur:
            # Check if a table named automator_logs was created
            cur.execute("""SELECT * from public.automator_logs;""")

            # Check if a table named automator_queries was created
            cur.execute("""SELECT * from public.automator_queries;""")

            # Make sure a table named automator doesn't exist
            try:
                cur.execute("""SELECT * from public.automator;""")
                self.assertEqual(False, True)
            except psycopg2.Error as e:
                self.assertEqual(True, True)

    def test_runUnInstaller(self):
        # Attempt to setup the database
        myCleaner = Cleaner(db_conf)
        myCleaner.runUninstaller()

        # Inspect the state of the database and make some assertions
        with db_con.cursor() as cur:
            # Make sure a table named automator doesn't exist
            try:
                cur.execute("""SELECT * from public.automator_logs;""")
                self.assertEqual(False, True)
            except psycopg2.Error as e:
                self.assertEqual(True, True)

            # Make sure a table named automator doesn't exist
            try:
                cur.execute("""SELECT * from public.automator_queries;""")
                self.assertEqual(False, True)
            except psycopg2.Error as e:
                self.assertEqual(True, True)

    def test_runQueries_all_categories(self):
        # Ensure the database is in a known state
        with db_con.cursor() as cur:
            cur.execute(slurp('./tests/fixtures/state_1-5.sql'))

        # Attempt to setup the database
        myCleaner = Cleaner(db_conf)
        myCleaner.runQueries()

        # Inspect the state of the database and make some assertions
        with db_con.cursor() as cur:

            # Check the rows in the table after insert has been called
            cur.execute("""SELECT name FROM public.users;""")
            rows = cur.fetchall()
            # Using the eq_ function from nose.tools allows us to assert that
            # complex types are equal. Here we are saying that we expect a single
            # row with a single value of 42
            eq_(rows, [('John',)])

    def test_runQueries_specific_category(self):
        # Ensure the database is in a known state
        with db_con.cursor() as cur:
            cur.execute(slurp('./tests/fixtures/state_1-5.sql'))

        # Attempt to setup the database
        myCleaner = Cleaner(db_conf)
        myCleaner.runQueries('Users')

        # Inspect the state of the database and make some assertions
        with db_con.cursor() as cur:

            # Check the rows in the table after insert has been called
            cur.execute("""SELECT name FROM public.users;""")
            rows = cur.fetchall()
            # Using the eq_ function from nose.tools allows us to assert that
            # complex types are equal. Here we are saying that we expect a single
            # row with a single value of 42
            eq_(rows, [('Andrew',)])

    def tearDown(self):
        """ Called after all of the tests in this file have been executed to close
        the database connecton and destroy the temporary database """
        db_con.close()
        db.stop()

def slurp(path):
    """ Reads and returns the entire contents of a file """
    with open(path, 'r') as f:
        return f.read()
