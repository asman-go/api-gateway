import pytest
import pydantic
from typing import List

from asman.domains.bugbounty_programs.api import (
    NewProgram,
    Asset,
    AssetId,
)


def test_get_assets(private_client, program_with_assets):
    response = private_client.get(f'/program/{program_with_assets}/assets')
    assert response.status_code == 200

    assets = pydantic.TypeAdapter(List[Asset]).validate_python(response.json())

    assert assets
    assert len(assets) > 0


def test_add_assets(private_client, program_id, new_assets):
    response = private_client.post(
        f'/program/{program_id}/assets',
        json={
            'assets': [
                new_asset.model_dump()
                for new_asset in new_assets
            ]
        }
    )

    assert response.status_code == 200

    ids = pydantic.TypeAdapter(List[AssetId]).validate_python(response.json())

    assert ids
    assert len(ids) == len(new_assets)


def test_remove_assets(private_client, program_with_assets):
    response = private_client.delete(f'/program/{program_with_assets}/assets')
    assert response.status_code == 200

    ids = pydantic.TypeAdapter(List[AssetId]).validate_python(response.json())
    assert ids
    assert len(ids) > 0
