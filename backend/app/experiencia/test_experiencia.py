import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.experiencia import functions as experiencia_functions, schemas as experiencia_schemas
from app.user import functions as user_functions, schemas as user_schemas
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

def test_create_experiencia(db):
    user_data = {
        "nome": "Pablo",
        "cpf": "444.222.091-11",
        "email": "pablo@user.com",
        "telefone": "6784-4765",
        "password": "userpasstest",
        "area_trabalho": "software",
        "nivel_educacao": "superior"
    }

    experiencia_data = {
        "empresa": "Empresa teste",
        "cargo": "Cargo teste",
        "anos": 5,
        "user_id": 1
    }

    user_schema = user_schemas.UserCreate(**user_data)
    created_user = user_functions.create_user(db, user_schema)

    experiencia_schema = experiencia_schemas.ExperienciaCreate(**experiencia_data)
    created_experiencia = experiencia_functions.create_experiencia(db, experiencia_schema)

    assert created_experiencia.empresa == experiencia_data["empresa"]
    assert created_experiencia.cargo == experiencia_data["cargo"]
    assert created_experiencia.anos == experiencia_data["anos"]

def test_update_experiencia(db):
    user_data = user_schemas.UserCreate(
        nome = "Mark",
        cpf = "123.386.455-11",
        email = "mark@user.com",
        telefone = "6328-4432",
        password = "userpasstest",
        area_trabalho = "vendas",
        nivel_educacao = "superior"
    )

    experiencia_data = experiencia_schemas.ExperienciaCreate(
        empresa = "Empresa teste",
        cargo = "Cargo teste",
        anos = 5,
        user_id = 1
    )

    user_functions.create_user(db, user_data)
    created_experiencia = experiencia_functions.create_experiencia(db, experiencia_data)

    update_data = experiencia_schemas.ExperienciaUpdate(
        empresa="AtualizaCorp",
        cargo="Cargo novo",
        anos=10
    )

    updated_experiencia = experiencia_functions.update_experiencia(db, created_experiencia.id, update_data)

    assert updated_experiencia.empresa == "AtualizaCorp"
    assert updated_experiencia.cargo == "Cargo novo"
    assert updated_experiencia.anos == 10

def test_delete_experiencia(db):
    user_data = user_schemas.UserCreate(
        nome = "Mark",
        cpf = "123.386.455-11",
        email = "mark@user.com",
        telefone = "6328-4432",
        password = "userpasstest",
        area_trabalho = "vendas",
        nivel_educacao = "superior"
    )

    experiencia_data = experiencia_schemas.ExperienciaCreate(
        empresa = "Empresa teste",
        cargo = "Cargo teste",
        anos = 5,
        user_id = 1
    )

    user_functions.create_user(db, user_data)
    created_experiencia = experiencia_functions.create_experiencia(db, experiencia_data)

    deleted = experiencia_functions.delete_experiencia(db, created_experiencia.id)
    assert deleted is not None

    assert db.query(experiencia_functions.models.Experiencia).filter_by(id=created_experiencia.id).first() is None

def test_get_experiencias_by_user(db):
    user_data = user_schemas.UserCreate(
        nome = "Mark",
        cpf = "123.386.455-11",
        email = "mark@user.com",
        telefone = "6328-4432",
        password = "userpasstest",
        area_trabalho = "vendas",
        nivel_educacao = "superior"
    )

    experiencia_data = experiencia_schemas.ExperienciaCreate(
        empresa = "Empresa teste",
        cargo = "Cargo teste",
        anos = 5,
        user_id = 1
    )
    user_functions.create_user(db, user_data)
    experiencia_functions.create_experiencia(db, experiencia_data)

    fetched = experiencia_functions.get_experiencias_by_user(db, 1)

    assert fetched is not None
    assert fetched.empresa == "Empresa teste"
    assert fetched.cargo == "Cargo teste"
    assert fetched.anos == 5

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

def test_create_experiencia_endpoint():
    user_payload = {
        "nome": "Bobert",
        "email": "bob@user.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

    experiencia_payload = {
        "empresa": "Empresa teste",
        "cargo": "Cargo teste",
        "anos": 5,
        "user_id": 1
    }

    response_user = client.post("/users/", json=user_payload)
    assert response_user.status_code == 200 or response_user.status_code == 201
    data_user = response_user.json()
    assert data_user["email"] == user_payload["email"]
    assert data_user["cpf"] == user_payload["cpf"]

    response_experiencia = client.post("/experiencias/", json=experiencia_payload)
    assert response_experiencia.status_code == 200 or response_experiencia.status_code == 201
    data_experiencia = response_experiencia.json()
    assert data_experiencia["empresa"] == experiencia_payload["empresa"]
    assert data_experiencia["cargo"] == experiencia_payload["cargo"]
    assert data_experiencia["anos"] == experiencia_payload["anos"]

def test_update_empresa_endpoint():
    user_payload = {
        "nome": "Bobert",
        "email": "bob@user.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

    response_user = client.post("/users/", json=user_payload)
    assert response_user.status_code == 200 or response_user.status_code == 201
    user_id = response_user.json()["id"]

    experiencia_payload = {
        "empresa": "Empresa teste",
        "cargo": "Cargo teste",
        "anos": 5,
        "user_id": user_id
    }

    response_experiencia = client.post("/experiencias/", json=experiencia_payload)
    assert response_experiencia.status_code == 200 or response_experiencia.status_code == 201
    experiencia_id = response_experiencia.json()["id"]

    update_payload = {"empresa": "PostUpdate", "cargo": "Cargo novo"}
    response = client.put(f"/experiencias/{experiencia_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["empresa"] == "PostUpdate"
    assert data["cargo"] == "Cargo novo"


def test_delete_empresa_endpoint():
    user_payload = {
        "nome": "Bobert",
        "email": "bob@user.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

    response_user = client.post("/users/", json=user_payload)
    assert response_user.status_code == 200 or response_user.status_code == 201
    user_id = response_user.json()["id"]

    experiencia_payload = {
        "empresa": "Empresa teste",
        "cargo": "Cargo teste",
        "anos": 5,
        "user_id": user_id
    }

    response_experiencia = client.post("/experiencias/", json=experiencia_payload)
    assert response_experiencia.status_code == 200 or response_experiencia.status_code == 201
    experiencia_id = response_experiencia.json()["id"]

    response = client.delete(f"/experiencias/{experiencia_id}")
    assert response.status_code == 200

    response = client.get(f"/experiencias/{experiencia_id}")
    assert response.status_code in (404, 400)

def test_get_experiencia_user():
    user_payload = {
        "nome": "Carlos",
        "email": "carlos@user.com",
        "cpf": "231.443.234-90",
        "telefone": "2234-1123",
        "password": "userapplypass",
        "area_trabalho": "engenharia aeroespacial",
        "nivel_educacao": "superior",
    }
    user_response = client.post("/users/", json=user_payload)
    user_id = user_response.json()["id"]

    experiencia_payload = {
        "empresa": "Empresa teste",
        "cargo": "Cargo teste",
        "anos": 5,
        "user_id": 1
    }

    experiencia_response = client.post("/experiencias/", json=experiencia_payload)
    experiencia_id = experiencia_response.json()["id"]

    list_resp = client.get(f"/user/{user_id}/")
    assert list_resp.status_code == 200 or list_resp.status_code == 201
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["empresa"] == "Empresa teste"
    assert data[0]["cargo"] == "Cargo teste"
    assert data[0]["anos"] == 5