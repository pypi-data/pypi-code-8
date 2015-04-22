from __future__ import print_function

import psycopg2


class Database(object):
    """A class to connect and save vehicles and positions to the database.
    The names of tables are hardcoded.'"""

    def __init__(self, database, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(
            "dbname=%s user=%s password=%s host=%s port=%s" %
            (database, user, password, host, port))
        self.cursor = self.conn.cursor()
        self.cursor.execute("SET TIME ZONE 'UTC';")

    def create_tables(self):
        SQL = """CREATE TABLE vehicles_car (
            id integer NOT NULL,
            plate character varying(15) NOT NULL
            );
            CREATE SEQUENCE vehicles_car_id_seq  START WITH 1 INCREMENT BY 1
                NO MINVALUE NO MAXVALUE CACHE 1;
            ALTER TABLE ONLY vehicles_car ALTER COLUMN id
                SET DEFAULT nextval('vehicles_car_id_seq'::regclass);
            CREATE TABLE vehicles_status (
                id integer NOT NULL,
                "position" geometry(Point,4326) NOT NULL,
                date timestamp with time zone NOT NULL,
                velocity integer NOT NULL,
                turned_on boolean NOT NULL,
                car_id integer NOT NULL
            );
            CREATE SEQUENCE vehicles_status_id_seq START WITH 1 INCREMENT BY 1
                NO MINVALUE NO MAXVALUE CACHE 1;
            ALTER TABLE ONLY vehicles_status ALTER COLUMN id
                SET DEFAULT nextval('vehicles_status_id_seq'::regclass);
            """
        self.cursor.execute(SQL)
        self.conn.commit()

    def add_vehicle(self, vehicle_id, vehicle_plate):
        """Insert a vehicle in the table vehicles_car of the database."""

        SQL = "select * FROM vehicles_car where vehicles_car.id = %s;"
        data = (vehicle_id, )
        self.cursor.execute(SQL, data)

        if len(self.cursor.fetchall()) == 0:
            SQL = "INSERT INTO vehicles_car (id, plate) VALUES (%s, %s);"
            data = (vehicle_id, vehicle_plate, )
            self.cursor.execute(SQL, data)
            self.conn.commit()
            print("Created vehicle with id %s" % vehicle_id)

    def add_status(self, vehicle_id, lng, lat, date, velocity, turned_on):
        """Insert a new status of a vehicle in the database."""

        SQL = """INSERT INTO vehicles_status \
            (car_id, position, date, velocity, turned_on) VALUES \
            (%s, ST_GeomFromText('POINT(%s %s)', 4326), %s, %s, %s);"""
        data = (vehicle_id, lng, lat, date, velocity, turned_on, )
        self.cursor.execute(SQL, data)
        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.cursor.close()
        self.conn.close()