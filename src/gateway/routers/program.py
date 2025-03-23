from fastapi import APIRouter, Body, Response
from typing import Annotated, List

from asman.domains.bugbounty_programs.use_cases import (
    GetAssetsUseCase,
    CreateProgramUseCase,
    DeleteProgramUseCase,
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    UpdateProgramUseCase,
    AddAssetsUseCase,
    RemoveAssetsUseCase,
)
from asman.domains.services.use_cases import DomainsFromCertsUseCase
from asman.domains.bugbounty_programs.api import (
    NewProgram,
    ProgramId,
    Program,
    AssetType,
    Asset,
    NewAsset,
    AddAssetsRequest,
    RemoveAssetsRequest,
    SearchByID,
)

from asman.domains.services.api import check_domain


router = APIRouter()

"""
Задачи:

1. Работа с информацией о бб программе
2. 

"""

@router.get('/')
async def read_all():
    use_case = ReadProgramUseCase()
    programs = await use_case.execute()

    return programs


@router.get('/{program_id}')
async def read_by_id(program_id: int):
    use_case = ReadProgramByIdUseCase()
    program = await use_case.execute(
        SearchByID(id=program_id)
    )

    return program


@router.delete('/{program_id}')
async def delete(program_id: int):
    use_case = DeleteProgramUseCase()
    deleted_program_id = await use_case.execute(
        SearchByID(id=program_id)
    )

    return Response(status_code=200) if deleted_program_id.program_id else Response(status_code=409) 


@router.post('/')
async def create(program: Annotated[NewProgram, Body(embed=True)]):
    use_case = CreateProgramUseCase()
    # print('Create program', program)

    program_id = await use_case.execute(program)

    return {
        'id': program_id.program_id,
    }


def normalize_domain(domain: str) -> str:
    if domain.startswith('*.'):
        return domain[2:]

    if domain.startswith('.'):
        return domain[1:]

    return domain


@router.post('/{program_id}/run')
async def run(program_id: int):
    
    assets = await GetAssetsUseCase().execute(
        ProgramId(program_id=program_id)
    )
    assets = filter(
        lambda asset: (
            asset.type == AssetType.ASSET_WEB
            and asset.in_scope and asset.is_paid
            and check_domain(asset.value)
        ),
        assets
    )
    domains = map(
        lambda asset: normalize_domain(asset.value),
        assets
    )
    crtsh_usecase = DomainsFromCertsUseCase()
    new_domains = await crtsh_usecase.execute(list(domains))

    return new_domains


@router.put('/{program_id}')
async def update(program_id, program: Annotated[NewProgram, Body(embed=True)]):
    use_case = UpdateProgramUseCase()

    updated_program_id = await use_case.execute(Program(
        id=program_id,
        **program.model_dump(),
    ))

    return updated_program_id


@router.put('/{program_id}/assets')
async def add_assets(program_id, assets: Annotated[List[NewAsset], Body(embed=True)]):
    use_case = AddAssetsUseCase()

    added_assets =  await use_case.execute(AddAssetsRequest(program_id=program_id, assets=assets))

    return Response(status_code=201)


# @router.put('/{program_id}/assets/remove')
# async def remove_assets(program_id, assets: Annotated[List[Asset], Body(embed=True)]):
#     use_case = RemoveAssetsUseCase()

#     await use_case.execute(RemoveAssetsRequest(program_id=program_id, assets=assets))

#     return Response(status_code=200)
