import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.api import (
    AssetType,
    NewProgram,
    NewAsset,
    AddAssetsRequest,
)
from asman.domains.bugbounty_programs.use_cases import (
    CreateProgramUseCase,
    AddAssetsUseCase,
)

from asman.core.adapters.tests import facebook_config
from asman.core.adapters.db.postgresql.tests import init_postgres_envs
from asman.core.adapters.db.dynamodb.tests import init_dynamodb_envs

from .conftest_config import (
    api_config, api_key_config, app_config
)

from .conftest_clients import (
    gateway_app,
    admin_client, integrations_client, public_client, private_client,
)


@pytest.fixture
def new_program():
    return NewProgram(
        program_name='Name',
        program_site='https://example.com/',
        platform='test',
        notes='Notes',
    )


@pytest.fixture
def new_program_delete():
    return NewProgram(
        program_name='Name',
        program_site='https://example.com/',
        platform='test',
        notes='Notes',
    )


@pytest.fixture
def new_assets():
    return [
        NewAsset(
            value='example.com',
            type=AssetType.ASSET_WEB,
            in_scope=True,
            is_paid=False,
        ),
        NewAsset(
            value='192.168.0.1',
            type=AssetType.ASSET_IP,
            in_scope=True,
            is_paid=True,
        ),
        NewAsset(
            value='https://api.example.com/',
            type=AssetType.ASSET_API,
            in_scope=False,
            is_paid=False,
        ),
    ]


@pytest_asyncio.fixture
async def program_id(new_program) -> int:
    _new_program_id = await CreateProgramUseCase().execute(new_program)
    return _new_program_id.program_id


@pytest_asyncio.fixture
async def program_with_assets(program_id, new_assets) -> int:
    await AddAssetsUseCase().execute(AddAssetsRequest(
        program_id=program_id,
        assets=new_assets,
    ))
    return program_id