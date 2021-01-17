from app.core.config import db_settings
from gino_starlette import Gino

db = Gino(
    dsn=db_settings.DATABASE_URL,
    pool_min_size=db_settings.DB_POOL_MIN_SIZE,
    pool_max_size=db_settings.DB_POOL_MAX_SIZE,
    echo=db_settings.DB_ECHO,
    ssl=db_settings.DB_SSL,
    use_connection_for_request=db_settings.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=db_settings.DB_RETRY_LIMIT,
    retry_interval=db_settings.DB_RETRY_INTERVAL,
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
