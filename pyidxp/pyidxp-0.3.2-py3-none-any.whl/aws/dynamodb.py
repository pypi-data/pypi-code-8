from boto.dynamodb2 import connect_to_region as dynamo_connect_to_region
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from time import sleep
from .base import Base


class DynamoDB(Base):
    def __init__(self, configs):
        self.local_key = 'dynamodb_local'
        self.connect(configs)

    def connect_fake(self):
        self.conn = DynamoDBConnection(
            aws_access_key_id='foo',
            aws_secret_access_key='bar',
            host='localhost',
            port=8000,
            is_secure=False)

    def connect_real(self, configs):
        self.conn = dynamo_connect_to_region(
            configs['aws']['region'],
            aws_access_key_id=configs['aws']['access_key'],
            aws_secret_access_key=configs['aws']['secret_key'])

    def get_table(self, table_name, keys=('id', 'timestamp')):
        if table_name in self.conn.list_tables()['TableNames']:
            table = Table(table_name, connection=self.conn)
            # Bug: https://github.com/boto/boto/issues/2826
            table.describe()
            return table
        table = Table.create(
            table_name,
            schema=[HashKey(keys[0]), RangeKey(keys[1])],
            throughput={'read': 5, 'write': 15},
            connection=self.conn)
        while table.describe()['Table']['TableStatus'] != 'ACTIVE':
            sleep(1)
        return table

    def update_table(self, table, throughput):
        if self.conn.host == 'localhost':
            return
        self.wait_until_table_is_active(table)
        table.update(throughput=throughput)
        self.wait_until_table_is_active(table)

    def wait_until_table_is_active(self, table):
        while table.describe()['Table']['TableStatus'] != 'ACTIVE':
            sleep(1)
