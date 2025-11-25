import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

from main import app
import database.models as models



@pytest.fixture(scope="session")
def test_engine():
    load_dotenv(".env.test", override=True)
    
    TEST_DB_URL = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )

    engine = create_engine(TEST_DB_URL)
    models.init_db(TEST_DB_URL)

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    return engine


@pytest.fixture(scope="session")
def TestSessionLocal(test_engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )


@pytest.fixture()
def db(TestSessionLocal, test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)


    def override_get_db():
        yield session
    models.get_db = override_get_db

    yield session

    transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture
def client():
    return TestClient(app)
