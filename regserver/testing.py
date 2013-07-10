from django.test.simple import DjangoTestSuiteRunner

class DatabaselessTestRunner(DjangoTestSuiteRunner):
    """ A test suite runner that does not setup and tear down a database. """

    def setup_databases(self):
        pass

    def teardown_databases(self, *args):
        pass
