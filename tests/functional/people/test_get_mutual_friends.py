from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_get_people_mutual(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    mutual_friends = PersonFactory.create_batch(3)
    connection1_email = {}
    connection2_email = {}
    l1 = []
    l2 = []
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        connection1_email[instance.email] = f.email

        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')
        connection2_email[target.email] = f.email
    db.session.commit()

    db.session.commit()

    connection1_emails_friend = list(connection1_email.values())
    connection2_emails_friend = list(connection2_email.values())

    for f in connection2_emails_friend:
        if f in connection1_emails_friend:
            flag = 1
        else:
            flag = 0
    if flag == 1:
        res = testapp.get('/people')

        assert res.status_code == HTTPStatus.OK

        assert len(res.json) == 5
        for person in res.json:
            for field in EXPECTED_FIELDS:
                assert field in person
    else:
        # If the above statement fails then make the test case fail
        assert 2 == 3
