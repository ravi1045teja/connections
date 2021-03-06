import factory
from factory import Faker, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from connections.database import db
from connections.models.connection import Connection
from connections.models.person import Person


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class PersonFactory(BaseFactory):
    """Person factory."""

    email = Sequence(lambda n: f'person{n}@example.com')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    date_of_birth = Faker('date')

    class Meta:
        model = Person


class ConnectionFactory(BaseFactory):
    """Connection factory."""
    from_person = factory.SubFactory(PersonFactory)
    to_person = factory.SubFactory(PersonFactory)
    connection_type = 'friend'

    class Meta:
        model = Connection




