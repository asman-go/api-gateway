import pytest
import pytest_asyncio
import pydantic
from typing import List

from asman.domains.bugbounty_programs.api import (
    NewProgram,
    Program,
    ProgramId,
    NewAsset,
    Asset,
    AssetType,
    ProgramNotFound,
)
from asman.domains.bugbounty_programs.use_cases import (
    CreateProgramUseCase,
)


@pytest_asyncio.fixture
async def program_id_to_delete(new_program_delete) -> int:
    _program_id = await CreateProgramUseCase().execute(new_program_delete)
    return _program_id.program_id


def test_add_program(private_client, new_program):
    response = private_client.post(
        '/program',
        json={
            'program': new_program.model_dump(),
        },
    )

    assert response.status_code == 200

    program_id = pydantic.TypeAdapter(ProgramId).validate_python(response.json())

    assert program_id


def test_get_program(private_client, program_id):
    response = private_client.get(f'/program/{program_id}')

    assert response.status_code == 200

    program = pydantic.TypeAdapter(Program).validate_python(response.json())

    assert program
    assert program.id == program_id


def test_update_program(private_client, program_id, new_program):
    new_updated_program = new_program.model_copy(deep=True)
    new_updated_program.program_name = 'NEW_VALUE'

    response = private_client.put(f'/program/{program_id}', json={
        'program': new_updated_program.model_dump(),
    })

    assert response.status_code == 200

    updated_program_id = pydantic.TypeAdapter(ProgramId).validate_python(response.json())

    assert updated_program_id
    assert updated_program_id.program_id == program_id


def test_get_programs(private_client):
    response = private_client.get('/program')

    assert response.status_code == 200

    programs = pydantic.TypeAdapter(List[Program]).validate_python(response.json())

    assert programs


def test_remove_programs(private_client, program_id_to_delete):
    program = pydantic.TypeAdapter(Program).validate_python(
        private_client.get(f'/program/{program_id_to_delete}').json()
    )

    assert program.id
    assert program.id == program_id_to_delete

    response = private_client.delete(f'/program/{program_id_to_delete}')
    assert response.status_code == 200

    removed_program_id = pydantic.TypeAdapter(ProgramId).validate_python(response.json())
    assert removed_program_id.program_id == program_id_to_delete

    with pytest.raises(ProgramNotFound):
        response = private_client.get(f'/program/{program_id_to_delete}')
        print('Response', response.json())
