from .auth import router as AuthRouter
from .program import router as ProgramRouter
from .dev_checks import router as DevChecksRouter
from .example import router as ExampleRouter


__all__ = [
    AuthRouter,
    ProgramRouter,
    DevChecksRouter,
    ExampleRouter,
]
