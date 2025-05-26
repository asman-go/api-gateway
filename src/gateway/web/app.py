import os
from jinja2 import Template, Environment, FileSystemLoader
from fastapi import FastAPI, Body, Request, Response
from fastapi.responses import HTMLResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from typing import Annotated

from asman.domains.bugbounty_programs.use_cases import (
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    GetAssetsUseCase,
)
from asman.domains.bugbounty_programs.api import (
    ProgramId,
    SearchByID,
)


GOOGLE_CLIENT_ID = '516328938379-j07g02tq8n1e71dom6irfrj72o3qp8l5.apps.googleusercontent.com'
jinja_env = Environment(
    autoescape=True,
    loader=FileSystemLoader('src/gateway/web/templates')
)
app = FastAPI()
# app.root_path = '/web'


def render_page(template_path: str, data: dict) -> str:
    main_template = jinja_env.get_template('index.html')
    child_template = jinja_env.get_template(template_path)

    child_rendered_template = child_template.render(**data)
    rendered = main_template.render(**{'main': child_rendered_template})

    return rendered


@app.get('/', response_class=HTMLResponse)
def main():
    # print('WEB LOGGER AAAAAAAA', os.getcwd())
    template = jinja_env.get_template('index.html')
    data = {'main': 'Hello, World!'}
    rendered = template.render(**data)

    return rendered


@app.get('/programs/{id}', response_class=HTMLResponse)
async def program(id: int):
    program = await ReadProgramByIdUseCase().execute(
        SearchByID(id=id),
    )
    data = program.model_dump()
    assets = await GetAssetsUseCase().execute(
        ProgramId(program_id=id)
    )

    assets_template = jinja_env.get_template('components/assets.html')
    rendered_assets = assets_template.render(**{'assets': assets})
    data['assets'] = rendered_assets

    return render_page('pages/program.html', data)


@app.get('/programs', response_class=HTMLResponse)
async def programs():
    programs_data = await ReadProgramUseCase().execute()
    programs_template = jinja_env.get_template('components/programs.html')
    rendered_programs = programs_template.render(**{'programs': programs_data})

    return render_page('pages/programs.html', {'programs': rendered_programs})


@app.post('/auth/google')
def auth_google(token: Annotated[str, Body(embed=True)], response: Response):
    id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
    # Опускаю проверки для теста, TODO
    print('UserInfo', id_info['sub'], id_info['email'])
    user_emails = [
        'murami.ike@gmail.com',
    ]
    if id_info['email'] in user_emails:
        # set session: временный вариант для тестов
        response.set_cookie('session', 'user-api-key')

    return {}


@app.get('/login', response_class=HTMLResponse)
def login():
    data = {
        'CLIENT_ID': GOOGLE_CLIENT_ID,
    }

    return render_page('pages/login.html', data)


@app.get('/auth/logout')
def logout(response: Response):
    response.set_cookie('session')
    return {}
