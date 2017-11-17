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

    @property
    def last_seen_interval(self):
        return (datetime.datetime.utcnow() - self.last_seen).total_seconds()

    def to_dict(self):
        d = super().to_dict()
        d['last_seen_interval'] = self.last_seen_interval
        return d


def bind(user, password, host, database):
    db.bind(provider='postgres',
            user=user,
            password=password,
            host=host,
            database=database)

    db.generate_mapping(create_tables=True)
