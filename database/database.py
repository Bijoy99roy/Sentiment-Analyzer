from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from utils.all_utils import read_yaml

class DataBase:
    def __init__(self):
        config = read_yaml('config/config.yaml')
        self.cloud_config = {
            'secure_connect_bundle': config['DATABASE']['CASSANDRA_FILE_PATH']
        }
        self.auth_provider = PlainTextAuthProvider(config['DATABASE']['CLIENTID'], config['DATABASE']['CLIENTSECRET'])
        self.session = None

    def connect_db(self):
        """
        Connecting to the database
        """
        try:
            cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
            self.session = cluster.connect()
        except Exception as e:
            raise e

    def insert_data(self, table_name, date, time, tweet, sentiment):
        """
        :param table_name: name of the respective table
        :param date: current date
        :param time: current time
        :param tweet: tweet to insert
        :param sentiment: Sentiment of the tweet
        """

        try:
            if self.is_connected():
                query = self.session.prepare(
                    f"INSERT INTO data.{table_name}(id, cur_date, cur_time, tweet, sentiment) VALUES(uuid(),?,?,?,?)")
                self.session.execute(query, [date, time, tweet, sentiment])
            else:
                raise Exception('Database not connected')
        except Exception as e:
            raise e

    def read_data(self, table_name):
        """
        Read data from database
        :param table_name: name of table to access
        :return: retrieved data
        """

        try:
            if self.is_connected():
                data = self.session.execute(f"select * from log.{table_name}")
            else:
                raise Exception('Database not connected')
            return data
        except Exception as e:
            raise e

    def create_tables(self):
        """
        Create table if don't exist
        """

        try:
            table = self.session.execute("SELECT * FROM system_schema.tables WHERE keyspace_name = 'data';")
            if table:
                return
            else:
                self.session.execute(
                    "CREATE TABLE data.dataset(id uuid , \
                    cur_date date, cur_time time, tweet text, sentiment varchar, PRIMARY KEY(id)) ;")

        except Exception as e:
            raise e

    def is_connected(self):
        """
        Check is database is connected
        :return: True- Connected
                 False- Not Connected
        """

        try:
            if self.session:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def close_connection(self):
        """
        Close database connection
        """

        try:
            if not self.session.is_shutdown:
                self.session.shutdown()
        except Exception as e:
            raise e