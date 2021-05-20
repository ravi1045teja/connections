import pytest
from tests.factories import ConnectionFactory, PersonFactory

from connections.schemas import ConnectionSchema


def test_mutual_friends(db):
    print(db)
    instance = PersonFactory()
    print(instance.email)
    target = PersonFactory()

    # some decoy connections (not mutual)

    con = ConnectionFactory(from_person=instance, to_person=target,
                            connection_type='friend')
    print(con.from_person_id)

    # ConnectionFactory.create_batch(5)

    mutual_friends = PersonFactory.create_batch(3)
    friend1 = []
    friend2 = []

    for f in mutual_friends:
        dict1 = {}
        dict2 = {}

        con1 = ConnectionFactory(from_person=instance, to_person=f,
                                 connection_type='friend')
        print(con1.from_person_id)

        dict1[con1.from_person_id] = con1.to_person_id
        print(dict1)

        friend1.append(dict1)

        con2 = ConnectionFactory(from_person=target, to_person=f,
                                 connection_type='friend')
        dict2[con2.from_person_id] = con2.to_person_id
        friend2.append(dict2)


    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    #db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    print([f.id for f in mutual_friends])

    print(friend1)
    print(friend2)
    assert len(friend1)+len(friend2) == 3
    # for f in results:
    #     assert f.id in expected_mutual_friend_ids
