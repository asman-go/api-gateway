from fastapi import APIRouter, Body
from typing import Annotated

from asman.domains.bugbounty_programs.use_cases import (
    CreateProgramUseCase,
    DeleteProgramUseCase,
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    UpdateProgramUseCase,
)
from asman.domains.bugbounty_programs.api import (
    ProgramId,
    ProgramData,
    Program,
)

from asman.core.adapters.db import PostgresConfig


router = APIRouter()

"""
Задачи:

1. Работа с информацией о бб программе
2. 

"""

@router.get('/')
async def read_all():
    config = PostgresConfig()
    use_case = ReadProgramUseCase(None, config)
    programs = await use_case.execute()

    return {
        'programs': programs,
    }


@router.get('/{program_id}')
async def read_by_id(program_id: int):
    config = PostgresConfig()
    use_case = ReadProgramByIdUseCase(None, config)
    program = await use_case.execute(ProgramId(id=program_id))

    return {
        'program': program,
    }


@router.delete('/{program_id}')
async def delete(program_id: int):
    config = PostgresConfig()
    use_case = DeleteProgramUseCase(None, config)
    status = await use_case.execute(ProgramId(id=program_id))

    return {
        'status': status,
    }


@router.post('/')
async def create(program: Annotated[ProgramData, Body(embed=True)]):
    config = PostgresConfig()
    use_case = CreateProgramUseCase(None, config)
    # print('Create program', program)

    program_id = await use_case.execute(program)

    return {
        'id': program_id.id,
    }


@router.put('/{program_id}')
async def update(program_id, program: Annotated[ProgramData, Body(embed=True)]):
    config = PostgresConfig()
    use_case = UpdateProgramUseCase(None, config)

    updated_program = await use_case.execute(Program(
        id=ProgramId(id=program_id),
        data=program,
    ))

    return {
        'program': updated_program,
    }
