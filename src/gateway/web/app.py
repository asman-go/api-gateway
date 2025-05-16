import os
from jinja2 import Template, Environment, FileSystemLoader
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


jinja_env = Environment(
    autoescape=True,
    loader=FileSystemLoader('src/gateway/web/templates')
)
app = FastAPI()
app.root_path = '/web'


@app.get('/', response_class=HTMLResponse)
def main():
    print('WEB LOGGER AAAAAAAA', os.getcwd())
    template = jinja_env.get_template('index.html')
    data = {}
    rendered = template.render(**data)

    return rendered
