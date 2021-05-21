import pytest
from tests.factories import ConnectionFactory, PersonFactory


def test_mutual_friends(db):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)

    ConnectionFactory.create_batch(5, to_person=target)

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

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    connection1_emails_friend = list(connection1_email.values())
    connection2_emails_friend = list(connection2_email.values())

    # Check whether the instance and target ids friend connections have same email ids,
    # by doing so we can deduce that instance and target are mutual friends
    for f in connection2_emails_friend:
        assert f in connection1_emails_friend
