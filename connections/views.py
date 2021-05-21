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


#Second Objective

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


#Second Objective

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

#Bonus Objective
@blueprint.route('/mutual_friends/<person_id>/<target_id>', methods=['GET'])
def get_mutual_friends(person_id, target_id):
    first_list = []
    first_list_target = []
    first_list_mutual_friends = []

    con1 = Connection.query.filter(Connection.from_person_id == person_id).filter(
        Connection.connection_type == 'friend')
    if con1 is not None:
        for i in con1:
            dict1 = {i.from_person_id: i.to_person_id}
            first_list.append(dict1)
    con2 = Connection.query.filter(Connection.from_person_id == target_id).filter(
        Connection.connection_type == 'friend')
    if con2 is not None:
        for j in con2:
            dict2 = {j.from_person_id: j.to_person_id}
            first_list_target.append(dict2)
    for k, l in zip(first_list, first_list_target):
        for key, value in k.items():
            if value == l[key]:
                first_list_mutual_friends.append(value)
    second_list = []
    second_list_target = []
    second_list_mutual_friends = []
    con3 = Connection.query.filter(Connection.from_person_id == target_id).filter(
        Connection.connection_type == 'friend')
    if con3 is not None:
        for i in con3:
            dict3 = {i.from_person_id: i.to_person_id}
            second_list.append(dict3)

    con4 = Connection.query.filter(Connection.from_person_id == person_id).filter(
        Connection.connection_type == 'friend')
    if con4 is not None:
        for j in con2:
            dict4 = {j.from_person_id: j.to_person_id}
            second_list_target.append(dict4)
    for k, l in zip(second_list, second_list_target):
        for key, value in k.items():
            if value == l[key]:
                second_list_mutual_friends.append(value)

    overall_friends = first_list_mutual_friends + second_list_mutual_friends

    try:
        l=[]
        if overall_friends is not None:
            for m in overall_friends:
                people = Person.query.filter(Person.id == m)
                if people is not None:

                    print(PersonSchema.jsonify(people))
                    l.append(PersonSchema.jsonify(people))

    except NoResultFound:
        return {"message": "No mutual Friends"}, 200
    return  json.dumps(l), HTTPStatus.OK
