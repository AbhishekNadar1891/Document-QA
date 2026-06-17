from pathlib import Path
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = Field(default=None, env="OPENAI_API_KEY")
    OPENROUTER_API_KEY: str | None = Field(default=None, env="OPENROUTER_API_KEY")
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    LLM_MODEL: str = Field(default="gpt-3.5-turbo", env="LLM_MODEL")
    TOP_K: int = Field(default=5, env="TOP_K")
    MIN_SIMILARITY: float = Field(default=0.65, env="MIN_SIMILARITY")
    MAX_UPLOAD_SIZE: int = Field(default=50 * 1024 * 1024, env="MAX_UPLOAD_SIZE")
    DATABASE_URL: str = Field(default="sqlite:///./data/rag.db", env="DATABASE_URL")
    VECTOR_DIR: Path = Field(default=Path("./data/vectorstore"), env="VECTOR_DIR")
    DATA_DIR: Path = Field(default=Path("./data"), env="DATA_DIR")
    LOG_FILE: Path = Field(default=Path("./logs/app.log"), env="LOG_FILE")
    RATE_LIMIT: str = Field(default="20/minute", env="RATE_LIMIT")
    ALLOWED_EXTENSIONS: set[str] = Field(default={"pdf", "docx", "txt"})
    PAGE_SIZE: int = Field(default=700, env="CHUNK_SIZE")
    PAGE_OVERLAP: int = Field(default=100, env="CHUNK_OVERLAP")
    VECTOR_INDEX_FILE: Path = Field(default=Path("./data/vectorstore/faiss.index"), env="VECTOR_INDEX_FILE")
    VECTOR_METADATA_FILE: Path = Field(default=Path("./data/vectorstore/metadata.json"), env="VECTOR_METADATA_FILE")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
