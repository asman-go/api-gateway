import pytest
from copy import deepcopy
from asman.domains.bugbounty_programs.api import (
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
def program_id(private_client, program_data):
    response = private_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )
    response = response.json()
    print('program_id response:', response)
    return response['id']


@pytest.fixture
def program_id_to_delete(private_client, program_data):
    response = private_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )
    response = response.json()

    return response['id']


def test_program_create(private_client, program_data):
    response = private_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )

    assert response.status_code == 200

    response = response.json()

    assert 'id' in response
    assert isinstance(response['id'], int)


def test_program_read(private_client, program_id):
    response = private_client.get(f'/program/{program_id}')

    assert response.status_code == 200

    assert Program(**response.json())


def test_program_update(private_client, program_id, program_data):
    new_program_data = deepcopy(program_data)
    new_program_data.program_name = 'NEW_VALUE'

    response = private_client.put(f'/program/{program_id}', json={
        'program': new_program_data.model_dump(),
    })

    assert response.status_code == 200
    assert Program(**response.json())

    program = Program(**response.json())

    assert program.id == program_id
    assert program.data.program_name == 'NEW_VALUE'


def test_program_read_all(private_client):
    response = private_client.get('/program')

    assert response.status_code == 200
    response = response.json()
    assert 'programs' in response
    assert isinstance(response['programs'], list)


def test_program_delete(private_client, program_id_to_delete):
    response = private_client.get(f'/program/{program_id_to_delete}')

    program = response.json()

    assert program

    response = private_client.delete(f'/program/{program_id_to_delete}')

    assert response.status_code == 200

    response = private_client.get(f'/program/{program_id_to_delete}')

    program = response.json()

    assert not program
