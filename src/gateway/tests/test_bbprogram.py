import pytest
import pydantic
from typing import List

from copy import deepcopy
from asman.domains.bugbounty_programs.api import (
    ProgramData,
    Program,
    Asset,
    AssetType,
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
def program_data_delete():
    return ProgramData(
        program_name='Name',
        program_site='https://example.com/',
        platform='test',
        assets=[],
        notes='Notes',
    )


@pytest.fixture
def program_assets():
    return [
        Asset(
            value='example.com',
            type=AssetType.ASSET_WEB,
            in_scope=True,
            is_paid=False,
        ),
        Asset(
            value='192.168.0.1',
            type=AssetType.ASSET_IP,
            in_scope=True,
            is_paid=True,
        ),
        Asset(
            value='https://api.example.com/',
            type=AssetType.ASSET_API,
            in_scope=False,
            is_paid=False,
        ),
    ]


@pytest.fixture
def program_id(private_client, program_data):
    response = private_client.post(
        '/program',
        json={
            'program': program_data.model_dump(),
        },
    )
    response = response.json()

    return response['id']


@pytest.fixture
def program_id_to_delete(private_client, program_data_delete):
    response = private_client.post(
        '/program',
        json={
            'program': program_data_delete.model_dump(),
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
    assert isinstance(response, list)


def test_program_delete(private_client, program_id_to_delete):
    response = private_client.get(f'/program/{program_id_to_delete}')

    program = response.json()

    assert program

    response = private_client.delete(f'/program/{program_id_to_delete}')

    assert response.status_code == 200

    response = private_client.get(f'/program/{program_id_to_delete}')

    program = response.json()

    assert not program


def test_add_assets(private_client, program_id, program_assets):
    all_programs = private_client.get('/program').json()
    print('progs', all_programs)
    print('id', program_id)

    assets = pydantic.TypeAdapter(List[Asset]).validate_python(program_assets)
    response = private_client.put(
        f'/program/{program_id}/assets',
        json={
            'assets': [asset.model_dump() for asset in assets]
        }
    )

    assert response.status_code == 201

    program = pydantic.TypeAdapter(Program).validate_python(
        private_client.get(f'/program/{program_id}').json()
    )

    for asset in assets:
        assert asset in program.data.assets


def test_remove_assets(private_client, program_id, program_assets):
    assets = pydantic.TypeAdapter(List[Asset]).validate_python(program_assets)
    assets_req = [asset.model_dump() for asset in assets]
    response = private_client.put(
        f'/program/{program_id}/assets',
        json={
            'assets': assets_req
        }
    )

    assert response.status_code == 201

    program_before = pydantic.TypeAdapter(Program).validate_python(
        private_client.get(f'/program/{program_id}').json()
    )

    response = private_client.put(
        f'/program/{program_id}/assets/remove',
        json={
            'assets': assets_req[1:]
        }
    )
    assert response.status_code == 200

    program_after = pydantic.TypeAdapter(Program).validate_python(
        private_client.get(f'/program/{program_id}').json()
    )

    assert len(program_before.data.assets) > len(program_after.data.assets)
