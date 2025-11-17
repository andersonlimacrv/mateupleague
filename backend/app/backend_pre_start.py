import logging
import time
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log
from app.core.database.db import async_get_db_session
from .logging_config import InterceptHandler
from app.core.config import settings

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 10 * 1  # 1 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    """
    Initialize the database connection by trying to execute a simple SELECT 1 statement.
    This function uses tenacity to retry the connection attempt until the database is ready.
    If the connection cannot be established after the maximum number of retries, it raises an OperationalError.
    """
    try:
        async for session in async_get_db_session():
            # Try to create a session to check if the database is awake
            await session.execute(select(1))
    except OperationalError as e:
        logger.error("Database initialization failed: %s", e)
        raise e


async def create_admin_first_user() -> None:
    """
    Create a default admin user if it does not exist.
    """
    async for session in async_get_db_session():
        from app.models.user import User
        from app.schemas.user import UserRoleEnum
        from app.core.security import get_password_hash

        result = await session.execute(
            select(User).where(User.username == settings.ROOT_USERNAME)
        )
        admin_first_user = result.scalars().first()
        if not admin_first_user:
            admin_first_user = User(
                username=settings.ROOT_USERNAME,
                email=settings.ROOT_EMAIL,
                password=get_password_hash(settings.ROOT_PASSWORD),
                role=UserRoleEnum.admin,
                is_active=True,
            )
            session.add(admin_first_user)
            await session.commit()
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists.")


async def async_main() -> None:
    """
    Main initialization function that logs the start and completion of the service initialization.
    Calls the init function to ensure the database is ready before proceeding.
    """
    start_time = time.time()
    logger.info("Initializing service...")
    try:
        await init()
        if(settings.ADD_ROOT_USER):
            logger.info("Creating admin user...")
            await create_admin_first_user()
        elif(settings.ADD_ROOT_USER == False):
            logger.info("Admin user not created.")
        elapsed_time = time.time() - start_time
        logger.info("Service successfully initialized in %.2f seconds.", elapsed_time)
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(
            "Service initialization failed after %.2f seconds. Error: %s",
            elapsed_time,
            str(e),
        )
