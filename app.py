import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Carregue as credenciais do Firebase a partir do arquivo JSON
cred = credentials.Certificate("crud-api-python-1cc3c-firebase-adminsdk-5gkwb-5f7935158f.json")

def initialize_db():
    firebase_admin.initialize_app(cred)
    # Inicialize o Firestore (banco de dados NoSQL do Firebase)
    db = firestore.client()
    return db

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_data():
    db = initialize_db()
    users_ref = db.collection("users")
    users = users_ref.stream()
    all_users = []
    for user in users:
        user_data = user.to_dict()
        all_users.append(user_data)
    firebase_admin.delete_app(firebase_admin.get_app())
    return jsonify(all_users)

@app.route('/users', methods=['POST'])
def post_data():
    db = initialize_db()

    user_data = request.get_json()

    # Verifique se já existe um usuário com o mesmo ID
    existing_user = db.collection("users").where("id", "==", user_data["id"]).stream()

    try:
        if any(existing_user):
            return jsonify({'message':f"Ja existe um usuario com o ID {user_data['id']}. Nao foi possivel adicionar o novo usuario."})
        else:
            # Adicione o novo usuário à coleção 'users'
            users_ref = db.collection("users")
            users_ref.add(user_data)
            return jsonify({'message':"Novo usuário adicionado."})
    except Exception as e:
        return jsonify({'message':f"Erro ao adicionar usuario: {e}"})
    finally:
        # Certifique-se de finalizar o aplicativo do Firebase, mesmo em caso de erro
        firebase_admin.delete_app(firebase_admin.get_app())

# Rota para o método DELETE
@app.route('/users', methods=['DELETE'])
def delete_data():
    db = initialize_db()
    user_data = request.get_json()
    user_id = user_data["id"]

    # Realiza uma consulta para encontrar o documento com o campo 'id' correspondente
    users_ref = db.collection("users")
    query = users_ref.where("id", "==", user_id)

    # Obtém os resultados da consulta
    user_documents = query.stream()
    try:
        # Exclui o documento se encontrado
        for user_doc in user_documents:
            user_doc.reference.delete()
            return jsonify({"message": f"Usuário com ID {user_id} deletado com sucesso"})

        return jsonify({"message": f"Usuário com ID {user_id} não encontrado"}), 404
    except Exception as e:
        return jsonify({'message':f"Erro ao deletar usuario: {e}"})
    finally:
        # Certifique-se de finalizar o aplicativo do Firebase, mesmo em caso de erro
        firebase_admin.delete_app(firebase_admin.get_app())


# Rota para o método PUT
@app.route('/users', methods=['PUT'])
def put_data():
    return jsonify({'message': 'Método PUT - atualizar dados'})

if __name__ == '__main__':
    app.run(debug=True)