from fastapi import APIRouter, Body, Response, Path
from typing import Annotated, List, Sequence

from asman.domains.bugbounty_programs.use_cases import (
    AddAssetsUseCase,
    GetAssetsUseCase,
    RemoveAssetsUseCase,
)
from asman.domains.bugbounty_programs.api import (
    ProgramId,
    Asset,
    AssetId,
    NewAsset,
    AddAssetsRequest,
)


router = APIRouter()


@router.get('/')
async def get_assets(program_id: int) -> Sequence[Asset]:
    return (
        await GetAssetsUseCase()
            .execute(
                ProgramId(
                    program_id=program_id,
                )
            )
    )


@router.post('/')
async def add_assets(program_id: int, assets: Annotated[List[NewAsset], Body(embed=True)]) -> Sequence[AssetId]:
    return (
        await AddAssetsUseCase()
            .execute(
                AddAssetsRequest(
                    program_id=program_id,
                    assets=assets,
                )
            )
    )


@router.delete('/')
async def remove_assets(program_id: int) -> Sequence[AssetId]:
    return (
        await RemoveAssetsUseCase()
            .execute(
                ProgramId(
                    program_id=program_id,
                )
            )
    )
