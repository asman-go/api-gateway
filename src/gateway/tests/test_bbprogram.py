import pytest
from copy import deepcopy
from asman.domains.bugbounty_programs.api import (
    ProgramId,
    ProgramData,
    Program,
)


@pytest.fixture
def program_data():
    return ProgramData(
        program_name='Name',
        program_site='https://example.com/',
        platform='test',
        assets=[],
        notes='Notes',
    )


@pytest.fixture
def program_id(user_client, program_data):
    response = user_client.post(
        '/app/program',
        json={
            'program': program_data.model_dump(),
        },
    )
    response = response.json()
    print('program_id response:', response)
    return response['id']


@pytest.fixture
def program_id_to_delete(user_client, program_data):
    response = user_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )
    response = response.json()

    return response['id']


def test_program_create(user_client, program_data):
    response = user_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )

    assert response.status_code == 200

    response = response.json()

    assert 'id' in response
    assert isinstance(response['id'], int)


def test_program_read(user_client, program_id):
    response = user_client.get(f'/program/{program_id}')

    assert response.status_code == 200

    response = response.json()

    assert 'program' in response

    program = response['program']

    assert Program(**program)


def test_program_update(user_client, program_id, program_data):
    new_program_data = deepcopy(program_data)
    new_program_data.program_name = 'NEW_VALUE'

    response = user_client.put(f'/program/{program_id}', json={
        'program': new_program_data.model_dump(),
    })

    assert response.status_code == 200

    response = response.json()

    assert 'program' in response

    program = response['program']

    assert Program(**program)

    program = Program(**program)

    assert program.id.id == program_id
    assert program.data.program_name == 'NEW_VALUE'


def test_program_read_all(user_client):
    response = user_client.get('/program')

    assert response.status_code == 200
    response = response.json()
    assert 'programs' in response
    assert isinstance(response['programs'], list)


def test_program_delete(user_client, program_id_to_delete):
    response = user_client.get(f'/program/{program_id_to_delete}')

    response = response.json()
    program = response['program']

    assert program

    response = user_client.delete(f'/program/{program_id_to_delete}')

    assert response.status_code == 200
    assert response.json() == {
        'status': True
    }

    response = user_client.get(f'/program/{program_id_to_delete}')

    response = response.json()
    program = response['program']

    assert not program
