from fastapi import APIRouter, Body, Response
from typing import Annotated, Sequence

from asman.domains.bugbounty_programs.use_cases import (
    GetAssetsUseCase,
    CreateProgramUseCase,
    DeleteProgramUseCase,
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    UpdateProgramUseCase,
)
from asman.domains.services.use_cases import DomainsFromCertsUseCase
from asman.domains.bugbounty_programs.api import (
    NewProgram,
    ProgramId,
    Program,
    AssetType,
    SearchByID,
)

from asman.gateway.core.utils import normalize_domain
from asman.domains.services.api import check_domain
from .assets import router as AssetRouter


"""
Задачи:

1. Работа с информацией о бб программе
2. 

"""


router = APIRouter()
router.include_router(AssetRouter, prefix='/{program_id}/assets')


@router.get('/')
async def get_programs() -> Sequence[Program]:
    return await ReadProgramUseCase().execute()


@router.get('/{program_id}')
async def get_program(program_id: int) -> Program:
    return (
        await ReadProgramByIdUseCase()
            .execute(
                SearchByID(
                    id=program_id,
                )
            )
    )


@router.delete('/{program_id}')
async def remove_program(program_id: int) -> ProgramId:
    deleted_program_id = await DeleteProgramUseCase().execute(
        SearchByID(id=program_id)
    )

    return deleted_program_id


@router.post('/')
async def add_program(program: Annotated[NewProgram, Body(embed=True)]) -> ProgramId:
    use_case = CreateProgramUseCase()

    return await use_case.execute(program)


@router.put('/{program_id}')
async def update_program(program_id, program: Annotated[NewProgram, Body(embed=True)]) -> ProgramId:
    updated_program_id = await UpdateProgramUseCase().execute(Program(
        id=program_id,
        **program.model_dump(),
    ))

    return updated_program_id


@router.post('/{program_id}/run')
async def run(program_id: int):
    
    assets = await GetAssetsUseCase().execute(
        ProgramId(program_id=program_id)
    )
    print('Assets to recon 1:', list(assets))
    assets = filter(
        lambda asset: (
            asset.type == AssetType.ASSET_WEB
            and asset.in_scope and asset.is_paid
            and check_domain(asset.value)
        ),
        assets
    )
    print('Assets to recon 2:', list(assets))
    domains = map(
        lambda asset: normalize_domain(asset.value),
        assets
    )
    # crtsh_usecase = DomainsFromCertsUseCase()
    # new_domains = await crtsh_usecase.execute(list(domains))
    # return new_domains

    print('Domains to recon:', list(domains))
    print('Assets to recon:', list(assets))

    return {}
