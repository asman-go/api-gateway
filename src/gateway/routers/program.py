from fastapi import APIRouter, Body, Response
from typing import Annotated, List

from asman.domains.bugbounty_programs.use_cases import (
    CreateProgramUseCase,
    DeleteProgramUseCase,
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    UpdateProgramUseCase,
    AddAssetsUseCase,
    RemoveAssetsUseCase,
)
from asman.domains.bugbounty_programs.api import (
    ProgramData,
    Program,
    AssetType,
    Asset,
    AddAssetsRequest,
    RemoveAssetsRequest,
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

    return programs


@router.get('/{program_id}')
async def read_by_id(program_id: int):
    config = PostgresConfig()
    use_case = ReadProgramByIdUseCase(None, config)
    program = await use_case.execute(program_id)

    return program


@router.delete('/{program_id}')
async def delete(program_id: int):
    config = PostgresConfig()
    use_case = DeleteProgramUseCase(None, config)
    status = await use_case.execute(program_id)

    return Response(status_code=200) if status else Response(status_code=409) 


@router.post('/')
async def create(program: Annotated[ProgramData, Body(embed=True)]):
    config = PostgresConfig()
    use_case = CreateProgramUseCase(None, config)
    # print('Create program', program)

    program_id = await use_case.execute(program)

    return {
        'id': program_id,
    }


@router.post('/{program_id}/run')
async def run(program_id: int):
    config = PostgresConfig()

    assets = filter(
        lambda asset: asset.type == AssetType.ASSET_WEB and asset.in_scope and asset.is_paid,
        (
            await ReadProgramByIdUseCase(None, config)
            .execute(program_id)
        ).data.assets
    )

    return assets


@router.put('/{program_id}')
async def update(program_id, program: Annotated[ProgramData, Body(embed=True)]):
    config = PostgresConfig()
    use_case = UpdateProgramUseCase(None, config)

    updated_program = await use_case.execute(Program(
        id=program_id,
        data=program,
    ))

    return updated_program


@router.put('/{program_id}/assets')
async def add_assets(program_id, assets: Annotated[List[Asset], Body(embed=True)]):
    config = PostgresConfig()
    use_case = AddAssetsUseCase(None, config)

    await use_case.execute(AddAssetsRequest(program_id=program_id, assets=assets))

    return Response(status_code=201)


@router.put('/{program_id}/assets/remove')
async def remove_assets(program_id, assets: Annotated[List[Asset], Body(embed=True)]):
    config = PostgresConfig()
    use_case = RemoveAssetsUseCase(None, config)

    await use_case.execute(RemoveAssetsRequest(program_id=program_id, assets=assets))

    return Response(status_code=200)
