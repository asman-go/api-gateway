from .bbprogram import router as ProgramRouter
from .dev_checks import router as DevChecksRouter
from .example import router as ExampleRouter


__all__ = [
    ProgramRouter,
    DevChecksRouter,
    ExampleRouter,
]
