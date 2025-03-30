from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


ENABLE_UTC = 'ENABLE_UTC'
TIMEZONE = 'TIMEZONE'
RESULT_BACKEND = 'RESULT_BACKEND'
BROKER_URL = 'BROKER_URL'
WORKER_SEND_TASK_EVENTS = 'WORKER_SEND_TASK_EVENTS'


# https://docs.celeryq.dev/en/stable/userguide/configuration.html#configuration
class CeleryConfig(BaseSettings):

    enable_utc: bool = Field(default=True, alias=ENABLE_UTC)
    timezone: str = Field(default='Europe/London', alias=TIMEZONE)
    
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend
    result_backend: str = Field(default='redis://localhost', alias=RESULT_BACKEND)
    
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-url
    broker_url: str = Field(default='redis://localhost', alias=BROKER_URL)
    
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
    # https://flower.readthedocs.io/en/latest/install.html#installation
    worker_send_task_events: bool = Field(default=False, alias=WORKER_SEND_TASK_EVENTS)


class AppConfig(BaseModel):
    name: str = Field(default='mycelery')
