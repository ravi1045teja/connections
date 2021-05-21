
from tests.factories import PersonFactory

from connections.models.connection import Connection


def test_can_udpate_connection(db, testapp):
    person_from = PersonFactory(first_name='Dostoevsky')
    person_to = PersonFactory(first_name='Nietzsche')
    db.session.commit()
    payload = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'coworker',
    }
    res1 = testapp.post('/connections', json=payload)
    patch_uri = '/connections/' + str(res1.json['id']) + '/friend'
    res = testapp.patch(patch_uri, json=payload)
    print(res.json)

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'friend'

