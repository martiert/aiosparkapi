import aiosparkapi.api.people


def test_person_representation_of_all_known_properties():
    person = {
        'id': 'some id',
        'emails': ['john.andersen@example.com', 'john.andersen@gmail.com'],
        'displayName': 'John Andersen',
        'nickName': 'JohnA',
        'firstName': 'John',
        'lastName': 'Andersen',
        'avatar': 'http://ciscospark/johnanders.avatar',
        'orgId': 'some org id',
        'roles': ['first role', 'second role'],
        'licenses': ['license'],
        'created': '2015-10-18T14:26:16.000Z',
        'timezone': 'America/Denver',
        'lastActivity': '2015-10-18T14:26:16.028Z',
        'status': 'active',
        'invitePending': False,
        'loginEnabled': True,
        'type': 'person',
    }

    result = aiosparkapi.api.people.Person(person)

    assert result.id == person['id']
    assert result.emails == person['emails']
    assert result.displayName == person['displayName']
    assert result.nickName == person['nickName']
    assert result.firstName == person['firstName']
    assert result.lastName == person['lastName']
    assert result.avatar == person['avatar']
    assert result.orgId == person['orgId']
    assert result.roles == person['roles']
    assert result.licenses == person['licenses']
    assert result.created == person['created']
    assert result.type == person['type']
    assert result.timezone == person['timezone']
    assert result.lastActivity == person['lastActivity']
    assert result.status == person['status']
    assert result.invitePending == person['invitePending']
    assert result.loginEnabled == person['loginEnabled']


def test_person_representation_of_only_required_fields():
    person = {
        'id': 'some id',
        'emails': ['john.andersen@example.com', 'john.andersen@gmail.com'],
        'displayName': 'John Andersen',
        'firstName': 'John',
        'lastName': 'Andersen',
        'avatar': 'http://ciscospark/johnanders.avatar',
        'orgId': 'some org id',
        'created': '2015-10-18T14:26:16.000Z',
        'lastActivity': '2015-10-18T14:26:16.028Z',
        'status': 'active',
        'type': 'person',
    }

    result = aiosparkapi.api.people.Person(person)

    assert result.id == person['id']
    assert result.emails == person['emails']
    assert result.displayName == person['displayName']
    assert result.firstName == person['firstName']
    assert result.lastName == person['lastName']
    assert result.avatar == person['avatar']
    assert result.orgId == person['orgId']
    assert result.type == person['type']
    assert result.lastActivity == person['lastActivity']
    assert result.status == person['status']
    assert result.created == person['created']
    assert result.nickName is None
    assert result.timezone is None
    assert result.invitePending is None
    assert result.loginEnabled is None
    assert result.roles is None
    assert result.licenses is None


def test_person_unknown_entry():
    person = {
        'id': 'some id',
        'emails': ['john.andersen@example.com', 'john.andersen@gmail.com'],
        'displayName': 'John Andersen',
        'firstName': 'John',
        'lastName': 'Andersen',
        'avatar': 'http://ciscospark/johnanders.avatar',
        'orgId': 'some org id',
        'created': '2015-10-18T14:26:16.000Z',
        'lastActivity': '2015-10-18T14:26:16.028Z',
        'status': 'active',
        'type': 'person',
        'unknown': 'foo',
    }

    result = aiosparkapi.api.people.Person(person)
    assert result.unknown == person['unknown']


def test_person_equality():
    person = {
        'id': 'some id',
        'emails': ['john.andersen@example.com', 'john.andersen@gmail.com'],
        'displayName': 'John Andersen',
        'firstName': 'John',
        'lastName': 'Andersen',
        'avatar': 'http://ciscospark/johnanders.avatar',
        'orgId': 'some org id',
        'created': '2015-10-18T14:26:16.000Z',
        'lastActivity': '2015-10-18T14:26:16.028Z',
        'status': 'active',
        'type': 'person',
        'unknown': 'foo',
    }

    result = aiosparkapi.api.people.Person(person)
    other = aiosparkapi.api.people.Person(person)

    assert result == person
    assert other == result
