import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.user import functions as user_functions, schemas as user_schemas
from app.vagas import functions as vagas_functions, schemas as vagas_schemas
from app.empresa import functions as empresa_functions, schemas as empresa_schemas
from app.admin import functions as admin_functions, schemas as admin_schemas
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

def test_create_user(db):
    user_data = {
        "nome": "Pablo",
        "cpf": "444.222.091-11",
        "email": "pablo@user.com",
        "telefone": "6784-4765",
        "password": "userpasstest",
        "area_trabalho": "software",
        "nivel_educacao": "superior"
    }

    user_schema = user_schemas.UserCreate(**user_data)
    created_user = user_functions.create_user(db, user_schema)

    assert created_user.email == user_data["email"]
    assert created_user.nome == user_data["nome"]

def test_get_user_by_cpf(db):
    user_data = user_schemas.UserCreate(
        nome="Maria",
        email="maria@user.com",
        cpf="764.123.987-45",
        telefone="3466-1234",
        password="usergetcpfpass",
        area_trabalho = "engenharia civil",
        nivel_educacao = "superior"
    )
    user_functions.create_user(db, user_data)
    fetched = user_functions.get_user_by_cpf(db, "764.123.987-45")

    assert fetched is not None
    assert fetched.email == "maria@user.com"
    assert fetched.cpf == "764.123.987-45"

def test_get_user_by_email(db):
    user_data = user_schemas.UserCreate(
        nome="Jane",
        email="jane@user.com",
        cpf="456.897.345-11",
        telefone="3456-1234",
        password="usergetemailpass",
        area_trabalho = "engenharia automotiva",
        nivel_educacao = "superior"
    )
    user_functions.create_user(db, user_data)
    fetched = user_functions.get_user_by_email(db, "jane@user.com")

    assert fetched is not None
    assert fetched.email == "jane@user.com"
    assert fetched.cpf == "456.897.345-11"

def test_get_users(db):
    user_data_1 = user_schemas.UserCreate(
        nome="Jane",
        email="jane@user.com",
        cpf="456.897.345-11",
        telefone="3456-1234",
        password="usergetpass",
        area_trabalho = "engenharia automotiva",
        nivel_educacao = "superior"
    )
    user_data_2 = user_schemas.UserCreate(
        nome="Jane2",
        email="jane2@user.com",
        cpf="456.333.444-11",
        telefone="3456-543",
        password="usergetpass",
        area_trabalho = "engenharia automotiva",
        nivel_educacao = "superior"
    )
    user_functions.create_user(db, user_data_1)
    user_functions.create_user(db, user_data_2)

    users = user_functions.get_users(db)
    assert len(users) == 2
    names = [user.nome for user in users]
    assert "Jane" in names
    assert "Jane2" in names

def test_apply_to_vaga(db):
    user_data = user_schemas.UserCreate(
        nome="Carlos",
        email="carlos@user.com",
        cpf="231.443.234-90",
        telefone="2234-1123",
        password="userapplypass",
        area_trabalho = "engenharia aeroespacial",
        nivel_educacao = "superior"
    )
    admin_data = admin_schemas.AdminCreate(
        nome="Anthony",
        email="anthony@admin.com",
        cpf="555.666.777-88",
        telefone="8888-0000",
        password="admingetcpfpass"
    )
    empresa_data = empresa_schemas.EmpresaCreate(
        nome = "Teste",
        descricao = "Empresa de teste",
        cidade = "Brasilia",
        cep = "1234567-89",
        no_empregados = 15,
        anos_func = 5,
        admin_id = 1
    )
    vaga_data = vagas_schemas.VagaCreate(
        titulo = "vaga teste",
        descricao = "vaga para testar",
        modalidade = "estagio",
        salario = 200,
        no_vagas = 10,
        empresa_id = 1
    )
    user = user_functions.create_user(db, user_data)
    admin = admin_functions.create_admin(db, admin_data)
    empresa = empresa_functions.create_empresa(db, empresa_data)
    vaga = vagas_functions.create_vaga(db, vaga_data)

    result = user_functions.apply_to_vaga(db, user.id, vaga.id)
    assert result["message"] == "User applied successfully!"
    assert user in vaga.candidatos

def test_add_and_remove_competencia(db):
    user_data = user_schemas.UserCreate(
        nome="Carlos",
        email="carlos@user.com",
        cpf="231.443.234-90",
        telefone="2234-1123",
        password="userapplypass",
        area_trabalho = "engenharia aeroespacial",
        nivel_educacao = "superior"
    )
    comp_data = competencia_schemas.CompetenciaCreate(
        nome = "Java avancado"
    )
    user = user_functions.create_user(db, user_data)
    comp = competencia_functions.create_competencia(db, comp_data)

    add_result = user_functions.add_competencia_to_user(db, user.id, comp.id)
    assert add_result["message"] == "Competência adicionada ao usuário com sucesso"
    assert comp in user.competencias

    remove_result = user_functions.remove_competencia_from_user(db, user.id, comp.id)
    assert remove_result["message"] == "Competência removida do usuário com sucesso"
    assert comp not in user.competencias

def test_get_user_competencias(db):
    user_data = user_schemas.UserCreate(
        nome="Carlos",
        email="carlos@user.com",
        cpf="231.443.234-90",
        telefone="2234-1123",
        password="userapplypass",
        area_trabalho = "engenharia aeroespacial",
        nivel_educacao = "superior"
    )
    comp_data = competencia_schemas.CompetenciaCreate(
        nome = "Java avancado"
    )
    user = user_functions.create_user(db, user_data)
    comp = competencia_functions.create_competencia(db, comp_data)

    comps = competencia_functions.get_user_competencias(db, user.id)
    assert len(comps) == 1
    assert comps[0].nome == "Java avancado"

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

def test_create_user_endpoint():
    payload = {
        "nome": "Bobert",
        "email": "bob@user.com",
        "cpf": "987.654.321-00",
        "telefone": "8888-8888",
        "password": "bobuserintpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["cpf"] == payload["cpf"]

@pytest.fixture
def user_payload_email():
    return {
        "nome": "Pattrick",
        "email": "pat@user.com",
        "cpf": "332.654.358-88",
        "telefone": "1596-4445",
        "password": "patusergetpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

@pytest.fixture
def user_payload_cpf():
    return {
        "nome": "Pattrick2",
        "email": "pat2@user.com",
        "cpf": "332.654.358-88",
        "telefone": "1596-4445",
        "password": "patusergetpass",
        "area_trabalho": "Vendas",
        "nivel_educacao": "superior"
    }

def test_user_email(user_payload_email):
    response = client.post("/users/", json=user_payload_email)
    assert response.status_code == 200 or response.status_code == 201
    result = response.json()
    assert result["email"] == "pat@user.com"
    assert result["cpf"] == "332.654.358-88"

def test_register_user_duplicate_email(user_payload_email):
    client.post("/users/", json=user_payload_email)
    response = client.post("/users/", json=user_payload_email)
    assert response.status_code == 400
    assert "Email already registered" in response.text

def test_register_user_duplicate_cpf(user_payload_cpf):
    client.post("/users/", json=user_payload_cpf)
    response = client.post("/users/", json=user_payload_cpf)
    assert response.status_code == 400
    assert "CPF already registered" in response.text

def test_user_add_list_remove_competencia():
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

    comp_payload = {"nome": "Python Avançado"}
    comp_response = client.post("/competencias/", json=comp_payload)
    comp_id = comp_response.json()["id"]

    add_resp = client.post(f"/users/{user_id}/competencias/{comp_id}")
    assert add_resp.status_code == 200 or add_resp.status_code == 201
    assert "Competência adicionada" in add_resp.text

    list_resp = client.get(f"/users/{user_id}/competencias")
    assert list_resp.status_code == 200 or list_resp.status_code == 201
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Python Avançado"

    remove_resp = client.delete(f"/users/{user_id}/competencias/{comp_id}")
    assert remove_resp.status_code == 200 or remove_resp.status_code == 201
    assert "Competência removida" in remove_resp.text

    list_resp_deleted = client.get(f"/users/{user_id}/competencias")
    assert list_resp_deleted.status_code == 200 or list_resp_deleted.status_code == 201
    assert list_resp_deleted.json() == []