from tests.factories import PersonFactory, ConnectionFactory


def test_get_people_mutual(db):
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





