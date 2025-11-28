import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.admin import functions, schemas
from app.database import Base, get_db
from app.main import app

# Unit tests

SQLALCHEMY_DATABASE_URL_UNIT = "sqlite:///./test_admin_unit.db"
engine_unit = create_engine(SQLALCHEMY_DATABASE_URL_UNIT, connect_args={"check_same_thread": False})
TestingSessionLocal_unit = sessionmaker(autocommit=False, autoflush=False, bind=engine_unit)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine_unit)
    session = TestingSessionLocal_unit()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine_unit)

def test_create_admin(db):
    admin_data = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "Marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpasstest",
    }

    admin_schema = schemas.AdminCreate(**admin_data)
    created_admin = functions.create_admin(db, admin_schema)

    assert created_admin.email == admin_data["email"]
    assert created_admin.nome == admin_data["nome"]

def test_update_admin(db):
    admin_data = schemas.AdminCreate(
        nome="Anthony",
        email="anthony@admin.com",
        cpf="555.666.777-88",
        telefone="8888-0000",
        password="adminupdatepass"
    )
    created_admin = functions.create_admin(db, admin_data)

    update_data = schemas.AdminUpdate(
        nome="Atualizado",
        email="atualizado@admin.com",
        telefone="1111-2222"
    )

    updated_admin = functions.update_admin(db, created_admin.id, update_data)

    assert updated_admin.nome == "Atualizado"
    assert updated_admin.email == "atualizado@admin.com"
    assert updated_admin.telefone == "1111-2222"

def test_delete_admin(db):
    admin_data = schemas.AdminCreate(
        nome="Anthony",
        email="anthony@admin.com",
        cpf="555.666.777-88",
        telefone="8888-0000",
        password="adminupdatepass"
    )
    created_admin = functions.create_admin(db, admin_data)

    deleted = functions.delete_admin(db, created_admin.id)
    assert deleted is not None

    assert db.query(functions.models.Admin).filter_by(id=created_admin.id).first() is None

def test_get_admin_by_cpf(db):
    admin_data = schemas.AdminCreate(
        nome="Anthony",
        email="anthony@admin.com",
        cpf="555.666.777-88",
        telefone="8888-0000",
        password="admingetcpfpass"
    )
    functions.create_admin(db, admin_data)
    fetched = functions.get_admin_by_cpf(db, "555.666.777-88")

    assert fetched is not None
    assert fetched.email == "anthony@admin.com"
    assert fetched.cpf == "555.666.777-88"

def test_get_admin_by_email(db):
    admin_data = schemas.AdminCreate(
        nome="Peter",
        email="peter@admin.com",
        cpf="444.111.999-88",
        telefone="6785-1234",
        password="admingetemailpass"
    )
    functions.create_admin(db, admin_data)
    fetched = functions.get_admin_by_email(db, "peter@admin.com")

    assert fetched is not None
    assert fetched.email == "peter@admin.com"
    assert fetched.cpf == "444.111.999-88"

# Integration tests
# ---------------------------
# Database setup for integration tests
# ---------------------------
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
    Base.metadata.drop_all(bind=engine_integration)

client = TestClient(app)

@pytest.fixture
def admin_headers():
    login_res = requests.post(
        "http://localhost:8001/auth/token",
        data={"username": "testadmin@example.com", "password": "testadminpass"}
    )
    login_res.raise_for_status()
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_admin_endpoint(admin_headers):
    payload = {
        "nome": "Bobert",
        "email": "bob@admin.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass"
    }

    response = client.post("/admins/", json=payload, headers=admin_headers)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["cpf"] == payload["cpf"]

def test_update_admin_endpoint(admin_headers):
    payload = {
        "nome": "Bobert",
        "email": "bob@admin.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass"
    }
    response = client.post("/admins/", json=payload, headers=admin_headers)
    admin_id = response.json()["id"]

    update_payload = {"nome": "PostUpdate", "telefone": "0000-1111"}
    response = client.put(f"/admins/{admin_id}", json=update_payload, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "PostUpdate"
    assert data["telefone"] == "0000-1111"

def test_delete_admin_endpoint(admin_headers):
    payload = {
        "nome": "Bobert",
        "email": "bob@admin.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobadminintpass"
    }
    response = client.post("/admins/", json=payload, headers=admin_headers)
    admin_id = response.json()["id"]

    response = client.delete(f"/admins/{admin_id}", headers=admin_headers)
    assert response.status_code == 200

    response = client.get(f"/admins/{admin_id}", headers=admin_headers)
    assert response.status_code in (404, 400)

@pytest.fixture
def admin_payload_email():
    return {
        "nome": "Pattrick",
        "email": "pat@admin.com",
        "cpf": "332.654.358-88",
        "telefone": "1596-4445",
        "password": "patadmingetpass"
    }

@pytest.fixture
def admin_payload_cpf():
    return {
        "nome": "Pattrick2",
        "email": "anotherpat@admin.com",
        "cpf": "332.654.358-88",
        "telefone": "1596-4445",
        "password": "patadmingetpass"
    }

def test_register_admin(admin_headers, admin_payload_email):
    response = client.post("/admins/", json=admin_payload_email, headers=admin_headers)
    assert response.status_code in (200, 201)
    result = response.json()
    assert result["email"] == "pat@admin.com"
    assert result["cpf"] == "332.654.358-88"

def test_register_admin_duplicate_email(admin_headers, admin_payload_email):
    client.post("/admins/", json=admin_payload_email, headers=admin_headers)
    response = client.post("/admins/", json=admin_payload_email, headers=admin_headers)
    assert response.status_code == 400
    assert "Email already registered" in response.text

def test_register_admin_duplicate_cpf(admin_headers, admin_payload_cpf):
    client.post("/admins/", json=admin_payload_cpf, headers=admin_headers)

    duplicate_cpf_payload = admin_payload_cpf.copy()
    duplicate_cpf_payload["email"] = "yetanotherpat@admin.com"
    response = client.post("/admins/", json=duplicate_cpf_payload, headers=admin_headers)
    assert response.status_code == 400
    assert "CPF already registered" in response.text