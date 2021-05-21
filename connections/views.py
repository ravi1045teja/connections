from http import HTTPStatus
import json

import sqlalchemy
from flask import Blueprint, jsonify, request
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from webargs.flaskparser import use_args
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connection():
    connection_schema = ConnectionSchema(many=True)
    people_schema = PersonSchema(many=True)
    connection = Connection.query.all()
    res = []
    ids = []

    for con in connection:
        dict1 = {}
        from_per = Person.query.filter(Person.id == con.from_person_id).one()
        to_per = Person.query.filter(Person.id == con.to_person_id).one()
        ids.append(con.id)
        dict1['id'] = con.id
        dict1['from_person'] = {"id": from_per.id, "first_person": from_per.first_name,
                                "last_name": from_per.last_name, "email": from_per.email}
        dict1['to_person'] = {"id": to_per.id, "first_person": to_per.first_name,
                              "last_name": to_per.last_name, "email": to_per.email}
        dict1['connection_type'] = con.connection_type.value

        res.append(dict1)

    print(json.dumps(res))

    return jsonify(res), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>/<connection_type>', methods=['PATCH'])
def update_connection(connection_id, connection_type):
    try:

        print(connection_type)
        con = Connection.query.filter(Connection.id == connection_id).one()
    except NoResultFound:
        return {"message": "Connection could not be found."}, 400
    enum_list = [i.value for i in ConnectionType]
    if connection_type in enum_list:
        con.connection_type = connection_type
        con.save()
    else:
        return {"message": "invalid Connection type"}, 400

    return ConnectionSchema().jsonify(con), HTTPStatus.CREATED
