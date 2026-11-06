from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "SQLForge Engine API"
    VERSION: str = "1.0.0"
    DEFAULT_TIMEOUT_SECONDS: float = 2.0
    MAX_OUTPUT_ROWS: int = 1000
    MAX_QUERY_LENGTH_CHARS: int = 10000
    PROGRESS_HANDLER_OPCODES: int = 5000

settings = Settings()

