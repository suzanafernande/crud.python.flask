"""Testes de integração para a API users"""
import unittest
import requests
from faker import Faker

faker = Faker()

base_url = 'http://127.0.0.1:5000'  # Altere conforme necessário

def test_get_data():
    """
    Testa a rota GET /users para recuperar dados do usuário.
    Verifica se a resposta tem o código de status 200 e se contém informações esperadas sobre o usuário.
    """
    response = requests.get(f'{base_url}/users')
    user = response.json()

    assert response.status_code == 200
    assert 'age' in user[0]
    assert 'email' in user[0]
    assert 'id' in user[0]
    assert 'name' in user[0]

def test_post_data():
    """
    Testa a rota POST /users para adicionar um novo usuário.
    Verifica se a resposta tem o código de status 200 e se o resultado indica que o novo usuário foi adicionado.
    """
    data = {'id': f'{faker.uuid4()}', 'name': f'{faker.name()}', 'email': f'{faker.email()}'}
    response = requests.post(f'{base_url}/users', json=data)
    result = response.json()

    assert response.status_code == 200
    assert result['message'] == 'Novo usuário adicionado.'

def test_delete_data():
    """
    Testa a rota DELETE /users para excluir um usuário.
    Verifica se a resposta tem o código de status 200 e se o resultado indica que o usuário foi excluído com sucesso.
    """
    id = faker.uuid4()

    user_creation = {'id': f'{id}', 'name': f'{faker.name()}', 'email': f'{faker.email()}'}
    response = requests.post(f'{base_url}/users', json=user_creation)

    user_delete = {'id': f'{id}'}
    response = requests.delete(f'{base_url}/users', json=user_delete)
    result = response.json()

    assert response.status_code == 200
    assert result['message'] == f'Usuário com ID {id} deletado com sucesso'

def test_put_data():
    """
    Testa a rota PUT /users para atualizar dados do usuário.
    Verifica se a resposta tem o código de status 200 e se o resultado indica que os dados foram atualizados.
    """
    data = {'id': '1', 'name': 'Updated Name', 'email': 'updated.email@example.com'}
    response = requests.put(f'{base_url}/users', json=data)
    result = response.json()
    assert response.status_code == 200
    assert result['message'] == 'Método PUT - atualizar dados'

if __name__ == '__main__':
    unittest.main()
