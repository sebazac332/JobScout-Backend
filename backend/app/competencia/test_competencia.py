import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.competencia import functions as competencia_functions, schemas as competencia_schemas
from app.database import Base, get_db
from app.main import app

# Unit tests

SQLALCHEMY_DATABASE_URL_UNIT = "sqlite:///./test_user_unit.db"
engine_unit = create_engine(SQLALCHEMY_DATABASE_URL_UNIT, connect_args={"check_same_thread": False})
TestingSessionLocal_unit = sessionmaker(autocommit=False, autoflush=False, bind=engine_unit)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine_unit)
    session = TestingSessionLocal_unit()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine_unit)

def test_create_competencia(db):
    competencia_data = {
        "nome": "Java intermedio"
    }

    competencia_schema = competencia_schemas.CompetenciaCreate(**competencia_data)
    created_competencia = competencia_functions.create_competencia(db, competencia_schema)

    assert created_competencia.nome == competencia_data["nome"]

def test_get_competencias(db):
    competencia_data_1 = competencia_schemas.CompetenciaCreate(
        nome="Python avancado"
    )
    competencia_data_2 = competencia_schemas.CompetenciaCreate(
        nome="React"
    )
    competencia_functions.create_competencia(db, competencia_data_1)
    competencia_functions.create_competencia(db, competencia_data_2)

    competencias = competencia_functions.get_competencias(db)
    assert len(competencias) == 2
    comps = [competencia.nome for competencia in competencias]
    assert "Python avancado" in comps
    assert "React" in comps

# Integration tests

SQLALCHEMY_DATABASE_URL_INTEGRATION = "sqlite:///./test_admin_integration.db"
engine_integration = create_engine(SQLALCHEMY_DATABASE_URL_INTEGRATION, connect_args={"check_same_thread": False})
TestingSessionLocal_integration = sessionmaker(autocommit=False, autoflush=False, bind=engine_integration)

def override_get_db():
    db = TestingSessionLocal_integration()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine_integration)
    yield
    TestingSessionLocal_integration().close_all()
    Base.metadata.drop_all(bind=engine_integration)

client = TestClient(app)

def test_create_competencia_endpoint():
    payload = {
        "nome": "Metodologias ageis"
    }

    response = client.post("/competencias/", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["nome"] == payload["nome"]

def test_list_competencias_endpoint():
    competencia_payloads = [
        {
            "nome": "NodeJS"
        },
        {
            "nome": "Rust intermedio"            
        }
    ]

    for comp in competencia_payloads:
        response = client.post("/competencias/", json=comp)
        assert response.status_code == 200 or response.status_code == 201

    response = client.get("/competencias/")
    assert response.status_code == 200
    competencias = response.json()

    assert isinstance(competencias, list)
    assert len(competencias) >= 2

    names = [competencia["nome"] for competencia in competencias]
    assert "NodeJS" in names
    assert "Rust intermedio" in names