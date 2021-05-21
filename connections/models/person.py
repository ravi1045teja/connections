from datetime import date
import re
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates


from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True,  nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    # For test_create_person_validations
    # db.CheckConstraint doesnt support MySQL Database (
    # https://docs.sqlalchemy.org/en/14/core/constraints.html#check-constraint) and tried with
    # validators, It goes into 500 error Which is validating perfectly But while asserting in
    # test file, we are only checking for 400 error Road block faced here

    # @validates('date_of_birth')
    # def validate_date_of_birth(self, key, value):
    #     assert value < date.today()
    #     return value
    #
    # @validates('email')
    # def validate_email(self, key, value):
    #     assert re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', value)
    #     return value
