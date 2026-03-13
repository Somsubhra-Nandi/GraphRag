from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "GraphRAG Knowledge Engine"

    DATA_PATH: str = "data/documents"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    OPENAI_API_KEY: str

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50

    class Config:
        env_file = ".env"


settings = Settings()