import datetime

from pony.orm import Database, Required, Optional, PrimaryKey
from pony.orm import db_session  # NOQA

db = Database()


class HybridPropertyMixin():
    '''This will include class properties defined with `@property`
    in the result of the to_dict() method.'''

    def to_dict(self):
        d = super().to_dict()

        for attr in dir(self.__class__):
            if isinstance(getattr(self.__class__, attr), property):
                d[attr] = getattr(self, attr)

        return d


class Device(HybridPropertyMixin, db.Entity):
    id = PrimaryKey(str)
    last_seen = Required(datetime.datetime,
                         default=datetime.datetime.utcnow)
    address = Optional(str)
    ota_mode = Required(bool)

    @property
    def last_seen_interval(self):
        return (datetime.datetime.utcnow() - self.last_seen).total_seconds()


def bind(host=None,
         user=None,
         password=None,
         database=None):
    db.bind(provider='postgres',
            user=user,
            password=password,
            host=host,
            database=database)

    db.generate_mapping(create_tables=True)
