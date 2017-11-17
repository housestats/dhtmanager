import datetime

from pony.orm import Database, Required, Optional, PrimaryKey
from pony.orm import db_session  # NOQA

db = Database()


class Device(db.Entity):
    id = PrimaryKey(str)
    last_seen = Required(datetime.datetime,
                         default=datetime.datetime.utcnow)
    address = Optional(str)
    ota_mode = Required(bool)


def bind(user, password, host, database):
    db.bind(provider='postgres',
            user=user,
            password=password,
            host=host,
            database=database)

    db.generate_mapping(create_tables=True)
