import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.empresa import functions as empresa_functions, schemas as empresa_schemas
from app.admin import functions as admin_functions, schemas as admin_schemas
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

def test_create_empresa(db):
    admin_data = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "Marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpasstest",
    }

    empresa_data = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasilia",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": 1
    }

    admin_schema = admin_schemas.AdminCreate(**admin_data)
    created_admin = admin_functions.create_admin(db, admin_schema)

    empresa_schema = empresa_schemas.EmpresaCreate(**empresa_data)
    created_empresa = empresa_functions.create_empresa(db, empresa_schema)

    assert created_empresa.nome == empresa_data["nome"]
    assert created_empresa.cep == empresa_data["cep"]

def test_update_empresa(db):
    admin_data = admin_schemas.AdminCreate(
        nome="Marcus",
        cpf="123.456.789-00",
        email="Marcus@admin.com",
        telefone="9999-9999",
        password="adminpasstest"
    )

    empresa_data = empresa_schemas.EmpresaCreate(
        nome="EmpresaCorp",
        descricao="Empresa para testes",
        cidade="Brasilia",
        cep="12345678-12",
        no_empregados=15,
        anos_func=3,
        admin_id=1
    )

    admin_functions.create_admin(db, admin_data)
    created_empresa = empresa_functions.create_empresa(db, empresa_data)

    update_data = empresa_schemas.EmpresaUpdate(
        nome="AtualizaCorp",
        descricao="Empresa atualizada",
        cidade="Floreanopolis"
    )

    updated_empresa = empresa_functions.update_empresa(db, created_empresa.id, update_data)

    assert updated_empresa.nome == "AtualizaCorp"
    assert updated_empresa.descricao == "Empresa atualizada"
    assert updated_empresa.cidade == "Floreanopolis"

def test_delete_empresa(db):
    admin_data = admin_schemas.AdminCreate(
        nome="Marcus",
        cpf="123.456.789-00",
        email="Marcus@admin.com",
        telefone="9999-9999",
        password="adminpasstest"
    )

    empresa_data = empresa_schemas.EmpresaCreate(
        nome="EmpresaCorp",
        descricao="Empresa para testes",
        cidade="Brasilia",
        cep="12345678-12",
        no_empregados=15,
        anos_func=3,
        admin_id=1
    )
    admin_functions.create_admin(db, admin_data)
    created_empresa = empresa_functions.create_empresa(db, empresa_data)

    deleted = empresa_functions.delete_user(db, created_empresa.id)
    assert deleted is not None

    assert db.query(empresa_functions.models.Empresa).filter_by(id=created_empresa.id).first() is None

def test_get_empresas(db):
    admin_data = admin_schemas.AdminCreate(
        nome="Marcus",
        cpf="123.456.789-00",
        email="Marcus@admin.com",
        telefone="9999-9999",
        password="adminpasstest"
    )

    empresa_data = empresa_schemas.EmpresaCreate(
        nome="EmpresaCorp",
        descricao="Empresa para testes",
        cidade="Brasilia",
        cep="12345678-12",
        no_empregados=15,
        anos_func=3,
        admin_id=1
    )
    admin_functions.create_admin(db, admin_data)
    empresa_functions.create_empresa(db, empresa_data)

    empresas = empresa_functions.get_empresas(db)
    assert len(empresas) == 1
    names = [empresa.nome for empresa in empresas]
    assert "EmpresaCorp" in names

def test_get_empresas_by_admin(db):
    admin_data = admin_schemas.AdminCreate(
        nome="Marcus",
        cpf="123.456.789-00",
        email="Marcus@admin.com",
        telefone="9999-9999",
        password="adminpasstest"
    )

    empresa_data = empresa_schemas.EmpresaCreate(
        nome="EmpresaCorp",
        descricao="Empresa para testes",
        cidade="Brasilia",
        cep="12345678-12",
        no_empregados=15,
        anos_func=3,
        admin_id=1
    )
    admin_functions.create_admin(db, admin_data)
    empresa_functions.create_empresa(db, empresa_data)

    fetched = empresa_functions.get_empresas_by_admin(db, 1)

    assert fetched is not None
    assert fetched.nome == "EmpresaCorp"
    assert fetched.cep == "12345678-12"

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

def test_create_empresa_endpoint():
    admin_payload = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "Marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpasstest",
    }

    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payload = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasilia",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": admin_id
    }

    response = client.post("/empresas/", json=empresa_payload)
    assert response.status_code == 200 or response.status_code == 201

    data = response.json()
    assert data["nome"] == "EmpresaCorp"
    assert data["descricao"] == "Empresa para testes"
    assert data["admin_id"] == admin_id

def test_update_empresa_endpoint():
    admin_payload = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "Marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpasstest",
    }

    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payload = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasilia",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": admin_id
    }

    response = client.post("/empresas/", json=empresa_payload)
    assert response.status_code == 200 or response.status_code == 201
    empresa_id = response.json()["id"]

    update_payload = {"nome": "PostUpdate", "descricao": "Nova empresa atualizada"}
    response = client.put(f"/empresas/{empresa_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "PostUpdate"
    assert data["descricao"] == "Nova empresa atualizada"


def test_delete_empresa_endpoint():
    admin_payload = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "Marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpasstest",
    }

    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payload = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasilia",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": admin_id
    }

    response = client.post("/empresas/", json=empresa_payload)
    assert response.status_code == 200 or response.status_code == 201
    empresa_id = response.json()["id"]

    response = client.delete(f"/empresas/{empresa_id}")
    assert response.status_code == 200

    response = client.get(f"/empresas/{empresa_id}")
    assert response.status_code in (404, 400)

def test_list_empresas_endpoint():
    admin_payload = {
        "nome": "Lucas",
        "cpf": "555.666.777-00",
        "email": "lucas@admin.com",
        "telefone": "1234-5678",
        "password": "lucaspass"
    }

    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payloads = [
        {
            "nome": "TechCorp",
            "descricao": "Empresa de tecnologia",
            "cidade": "São Paulo",
            "cep": "01000-000",
            "no_empregados": 50,
            "anos_func": 10,
            "admin_id": admin_id
        },
        {
            "nome": "EducaPlus",
            "descricao": "Empresa de educação",
            "cidade": "Rio de Janeiro",
            "cep": "20000-000",
            "no_empregados": 30,
            "anos_func": 5,
            "admin_id": admin_id
        }
    ]

    for emp in empresa_payloads:
        response = client.post("/empresas/", json=emp)
        assert response.status_code == 200 or response.status_code == 201

    response = client.get("/empresas/")
    assert response.status_code == 200
    empresas = response.json()

    assert isinstance(empresas, list)
    assert len(empresas) >= 2

    names = [empresa["nome"] for empresa in empresas]
    assert "TechCorp" in names
    assert "EducaPlus" in names