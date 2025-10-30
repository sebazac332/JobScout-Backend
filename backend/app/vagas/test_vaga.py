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

def test_create_vaga(db):
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

    vaga_data = {
        "titulo": "Vaga estagio",
        "descricao": "Uma vaga de estagio simples",
        "modalidade": "Estagio",
        "salario": 200.50,
        "no_vagas": 5,
        "empresa_id": 1
    }

    admin_schema = admin_schemas.AdminCreate(**admin_data)
    created_admin = admin_functions.create_admin(db, admin_schema)

    empresa_schema = empresa_schemas.EmpresaCreate(**empresa_data)
    created_empresa = empresa_functions.create_empresa(db, empresa_schema)

    vaga_schema = vagas_schemas.VagaCreate(**vaga_data)
    created_vaga = vagas_functions(db, vaga_schema)

    assert created_vaga.titulo == vaga_data["titulo"]
    assert created_vaga.descricao == vaga_data["descricao"]
    assert created_vaga.ceempresa_idp == vaga_data["empresa_id"]

def test_update_vaga(db):
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
    vaga_data = vagas_schemas.VagaCreate(
        titulo="Vaga estagio",
        descricao="Uma vaga de estagio simples",
        modalidade="Estagio",
        salario=200.50,
        no_vagas=5,
        empresa_id=1
    )

    admin_functions.create_admin(db, admin_data)
    empresa_functions.create_empresa(db, empresa_data)
    created_vaga = vagas_functions.create_vaga(db, vaga_data)

    update_data = empresa_schemas.EmpresaUpdate(
        titulo="Vaga atualizada",
        modalidade="Permanente",
        salario=350.5
    )

    updated_vaga = vagas_functions.update_vaga(db, created_vaga.id, update_data)

    assert updated_vaga.titulo == "Vaga atualizada"
    assert updated_vaga.modalidade == "Permanente"
    assert updated_vaga.salario == 350.5

def test_delete_vaga(db):
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
    vaga_data = vagas_schemas.VagaCreate(
        titulo="Vaga estagio",
        descricao="Uma vaga de estagio simples",
        modalidade="Estagio",
        salario=200.50,
        no_vagas=5,
        empresa_id=1
    )

    admin_functions.create_admin(db, admin_data)
    empresa_functions.create_empresa(db, empresa_data)
    created_vaga = vagas_functions.create_vaga(db, vaga_data)

    deleted = vagas_functions.delete_vaga(db, created_vaga.id)
    assert deleted is not None

    assert db.query(vagas_functions.models.Vagaemprego).filter_by(id=created_vaga.id).first() is None

def test_get_vagas_by_empresa(db):
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

    vaga_data = vagas_schemas.VagaCreate(
        titulo="Vaga estagio",
        descricao="Uma vaga de estagio simples",
        modalidade="Estagio",
        salario=200.50,
        no_vagas=5,
        empresa_id=1
    )

    admin_functions.create_admin(db, admin_data)
    empresa_functions.create_empresa(db, empresa_data)
    vagas_functions.create_vagaemprego(db, vaga_data)

    fetched = vagas_functions.get_vagas_by_empresa(db, 1)

    assert fetched is not None
    assert fetched.titulo == "Vaga estagio"
    assert fetched.descricao == "Uma vaga de estagio simples"
    assert fetched.empresa_id == 1

def test_add_and_remove_competencia_from_vaga(db):
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
    vaga_data = vagas_schemas.VagaCreate(
        titulo="Vaga estagio",
        descricao="Uma vaga de estagio simples",
        modalidade="Estagio",
        salario=200.50,
        no_vagas=5,
        empresa_id=1
    )
    comp_data = competencia_schemas.CompetenciaCreate(
        nome="Python Avançado"
    )

    admin = admin_functions.create_admin(db, admin_data)
    empresa = empresa_functions.create_empresa(db, empresa_data)
    vaga = vagas_functions.create_vaga(db, vaga_data)
    comp = competencia_functions.create_competencia(db, comp_data)

    result_add = vagas_functions.add_competencia_to_vaga(db, vaga.id, comp.id)
    assert result_add["message"] == "Competência adicionada à vaga com sucesso"
    assert comp in vaga.competencias

    with pytest.raises(Exception) as exc_info:
        vagas_functions.add_competencia_to_vaga(db, vaga.id, comp.id)
    assert "Competência já associada" in str(exc_info.value)

    result_remove = vagas_functions.remove_competencia_from_vaga(db, vaga.id, comp.id)
    assert result_remove["message"] == "Competência removida da vaga com sucesso"
    assert comp not in vaga.competencias

    with pytest.raises(Exception) as exc_info:
        vagas_functions.remove_competencia_from_vaga(db, vaga.id, comp.id)
    assert "Competência não associada" in str(exc_info.value)

def test_get_vaga_competencia(db):
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

    vaga_data = vagas_schemas.VagaCreate(
        titulo="Vaga estagio",
        descricao="Uma vaga de estagio simples",
        modalidade="Estagio",
        salario=200.50,
        no_vagas=5,
        empresa_id=1
    )

    comp_data = competencia_schemas.CompetenciaCreate(
        nome="Python Avançado"
    )

    admin = admin_functions.create_admin(db, admin_data)
    empresa =empresa_functions.create_empresa(db, empresa_data)
    comp = competencia_functions.create_competencia(db, comp_data)
    vaga = vagas_functions.create_vagaemprego(db, vaga_data)
    vagas_functions.add_competencia_to_vaga(db, vaga.id, comp.id)

    fetched = vagas_functions.get_vaga_competencias(db, 1)

    assert fetched is not None
    assert fetched.nome == "Python Avançado"

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

def test_create_vaga_endpoint():
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

    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payload = {
        "titulo": "Vaga estagio",
        "descricao": "Uma vaga de estagio simples",
        "modalidade": "Estagio",
        "salario": 200.50,
        "no_vagas": 5,
        "empresa_id": empresa_id
    }

    vaga_response = client.post("/vagas/", json=vaga_payload)
    assert vaga_response.status_code == 200 or vaga_response.status_code == 201

    data = vaga_response.json()
    assert data["nome"] == "Vaga estagio"
    assert data["descricao"] == "Uma vaga de estagio simples"
    assert data["empresa_id"] == empresa_id

def test_update_vaga_endpoint():
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

    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payload = {
        "titulo": "Vaga estagio",
        "descricao": "Uma vaga de estagio simples",
        "modalidade": "Estagio",
        "salario": 200.50,
        "no_vagas": 5,
        "empresa_id": empresa_id
    }

    vaga_response = client.post("/vagas/", json=vaga_payload)
    assert vaga_response.status_code == 200 or vaga_response.status_code == 201
    vaga_id = vaga_response.json()["id"]

    update_payload = {"titulo": "PostUpdate", "descricao": "Nova vaga atualizada"}
    response = client.put(f"/vagas/{vaga_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "PostUpdate"
    assert data["descricao"] == "Nova vaga atualizada"


def test_delete_vaga_endpoint():
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

    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payload = {
        "titulo": "Vaga estagio",
        "descricao": "Uma vaga de estagio simples",
        "modalidade": "Estagio",
        "salario": 200.50,
        "no_vagas": 5,
        "empresa_id": empresa_id
    }

    vaga_response = client.post("/vagas/", json=vaga_payload)
    assert vaga_response.status_code == 200 or vaga_response.status_code == 201
    vaga_id = vaga_response.json()["id"]

    response = client.delete(f"/vagas/{vaga_id}")
    assert response.status_code == 200

    response = client.get(f"/vagas/{vaga_id}")
    assert response.status_code in (404, 400)

def test_list_vagas_by_empresa_endpoint():
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

    empresa_payload = {
        "nome": "TechCorp",
        "descricao": "Empresa de tecnologia",
        "cidade": "São Paulo",
        "cep": "01000-000",
        "no_empregados": 50,
        "anos_func": 10,
        "admin_id": admin_id
    }
        
    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payloads = [
        {
            "titulo": "Vaga estagio",
            "descricao": "Uma vaga de estagio simples",
            "modalidade": "Estagio",
            "salario": 200.50,
            "no_vagas": 5,
            "empresa_id": empresa_id
        },
        {
            "titulo": "Vaga software",
            "descricao": "Uma vaga de software",
            "modalidade": "Permanente",
            "salario": 300,
            "no_vagas": 2,
            "empresa_id": empresa_id
        }
    ]

    for vaga_payload in vaga_payloads:
        vaga_response = client.post("/vagas/", json=vaga_payload)
        assert vaga_response.status_code == 200 or vaga_response.status_code == 201

    response_vagas_list = client.get(f"/vagas/empresa/{empresa_id}")
    assert response_vagas_list.status_code == 200
    vagas = response_vagas_list.json()

    assert isinstance(vagas, list)
    assert len(vagas) >= 2

    titulos = [vaga["titulo"] for vaga in vagas]
    assert "Vaga estagio" in titulos
    assert "Vaga software" in titulos

    response_no_vagas = client.get("/vagas/empresa/9999")
    assert response_no_vagas.status_code == 404
    assert response_no_vagas.json()["detail"] == "No vagas found for this empresa"

def test_apply_to_vaga_endpoint():
    user_payload = {
        "nome": "Carlos",
        "email": "carlos@user.com",
        "cpf": "231.443.234-90",
        "telefone": "2234-1123",
        "password": "userapplypass",
        "area_trabalho": "engenharia aeroespacial",
        "nivel_educacao": "superior"
    }
    user_response = client.post("/users/", json=user_payload)
    assert user_response.status_code == 200 or user_response.status_code == 201
    user_id = user_response.json()["id"]

    admin_payload = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpass"
    }
    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payload = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasília",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": admin_id
    }
    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payload = {
        "titulo": "Vaga teste",
        "descricao": "vaga para testar apply",
        "modalidade": "estagio",
        "salario": 200.0,
        "no_vagas": 10,
        "empresa_id": empresa_id
    }
    vaga_response = client.post("/vagas/", json=vaga_payload)
    assert vaga_response.status_code == 200 or vaga_response.status_code == 201
    vaga_id = vaga_response.json()["id"]

    response = client.post(f"/vagas/{vaga_id}/apply/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User applied successfully!"

def test_vagas_add_list_remove_competencia():
    admin_payload = {
        "nome": "Marcus",
        "cpf": "123.456.789-00",
        "email": "marcus@admin.com",
        "telefone": "9999-9999",
        "password": "adminpass"
    }
    admin_response = client.post("/admins/", json=admin_payload)
    assert admin_response.status_code == 200 or admin_response.status_code == 201
    admin_id = admin_response.json()["id"]

    empresa_payload = {
        "nome": "EmpresaCorp",
        "descricao": "Empresa para testes",
        "cidade": "Brasília",
        "cep": "12345678-12",
        "no_empregados": 15,
        "anos_func": 3,
        "admin_id": admin_id
    }
    empresa_response = client.post("/empresas/", json=empresa_payload)
    assert empresa_response.status_code == 200 or empresa_response.status_code == 201
    empresa_id = empresa_response.json()["id"]

    vaga_payload = {
        "titulo": "Vaga teste",
        "descricao": "vaga para testar apply",
        "modalidade": "estagio",
        "salario": 200.0,
        "no_vagas": 10,
        "empresa_id": empresa_id
    }
    vaga_response = client.post("/vagas/", json=vaga_payload)
    assert vaga_response.status_code == 200 or vaga_response.status_code == 201
    vaga_id = vaga_response.json()["id"]

    comp_payload = {"nome": "Python Avançado"}
    comp_response = client.post("/competencias/", json=comp_payload)
    comp_id = comp_response.json()["id"]

    add_resp = client.post(f"/vagas/{vaga_id}/competencias/{comp_id}")
    assert add_resp.status_code == 200 or add_resp.status_code == 201
    assert "Competência adicionada" in add_resp.text

    list_resp = client.get(f"/vagas/{vaga_id}/competencias")
    assert list_resp.status_code == 200 or list_resp.status_code == 201
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Python Avançado"

    remove_resp = client.delete(f"/vagas/{vaga_id}/competencias/{comp_id}")
    assert remove_resp.status_code == 200 or remove_resp.status_code == 201
    assert "Competência removida" in remove_resp.text

    list_resp_deleted = client.get(f"/vagas/{vaga_id}/competencias")
    assert list_resp_deleted.status_code == 200 or list_resp_deleted.status_code == 201
    assert list_resp_deleted.json() == []