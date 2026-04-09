from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "chimera"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/chimera"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    AWS_ACCESS_KEY_ID: str = "admin"
    AWS_SECRET_ACCESS_KEY: str = "password123"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "chimera-uploads"
    AWS_ENDPOINT_URL: str = "http://localhost:9000"

settings = Settings()