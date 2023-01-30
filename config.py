class Config:
    """
    Run app from localhost (container 'redis' and 'postgr' are running)
        uvicorn main:app --reload
    """

    # DATABASE_ADDRESS = 'localhost:5433'
    # REDIS_ADDRESS = 'localhost'
    """
    Run app from docker container
        docker-compose up
        or
        docker-compose up --build
    """
    DATABASE_ADDRESS = "postgres:5432"
    REDIS_ADDRESS = "redis"
    """Database url"""
    DATABASE_URL = f"postgresql://postgres:password@{DATABASE_ADDRESS}/fastapi_database"
