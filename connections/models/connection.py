import enum

from sqlalchemy.orm import relationship

from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.person import Person


class ConnectionType(enum.Enum):
    mother = 'mother'
    father = 'father'
    son = 'son'
    daughter = 'daughter'
    husband = 'husband'
    wife = 'wife'
    brother = 'brother'
    sister = 'sister'
    friend = 'friend'
    coworker = 'coworker'


# Modified class for test_mutual_friends.py to work with
# SubFactory
# Added relationship for both foreign keys
class Connection(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    from_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    from_person = relationship("Person", foreign_keys='Connection.from_person_id')

    to_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_person = relationship("Person", foreign_keys='Connection.to_person_id')
    connection_type = db.Column(db.Enum(ConnectionType), nullable=False)
