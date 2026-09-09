import os
import tempfile


# Must be set before app/database modules are imported by test files.
TEST_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    f"sitelink-scout-test-{os.getpid()}.db",
)

os.environ["SITELINK_DATABASE_URL"] = (
    f"sqlite:///{TEST_DB_PATH}"
)


import pytest

from app.database import Base, engine

# Ensure model metadata is registered.
from app.models.measurement import Measurement  # noqa: F401


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()

    try:
        os.remove(TEST_DB_PATH)
    except FileNotFoundError:
        pass
