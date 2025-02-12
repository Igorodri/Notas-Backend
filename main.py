from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2

app = Flask(__name__, static_folder="../Notas-Frontend/static", template_folder="../Notas-Frontend")

CORS(app);

DATABASE_URL = "postgresql://neondb_owner:npg_HA3pm7QItTkd@ep-aged-cell-a5ztp2ol.us-east-2.aws.neon.tech/neondb?sslmode=require"


conexao = psycopg2.connect(DATABASE_URL)


print("Conexão com o banco de dados realizada com sucesso!")

@app.route('/')
def home():
    return send_from_directory(app.template_folder, "index.html")

@app.route('/notas')
def select():

    cursor = conexao.cursor()

    try:
        cursor.execute('SELECT * FROM "NOTAS_GERAIS"')
        notas = cursor.fetchall()
        
        lista_notas = [{"id": nota[0], "titulo": nota[1], "descricao": nota[2], "data": nota[3]} for nota in notas]

        return jsonify(lista_notas)

    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": str(e)}), 500

    finally:
        cursor.close() 

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        registro = request.get_json()
        titulo = registro.get('titulo')
        descricao = registro.get('descricao')

        if not titulo or not descricao:
            return jsonify({'erro': 'Título e descrição são obrigatórios'}), 400

        cursor = conexao.cursor()

        cursor.execute('INSERT INTO "NOTAS_GERAIS" (titulo, descricao, data_criacao) VALUES (%s, %s, NOW())', (titulo, descricao))
        conexao.commit()

        return jsonify({'mensagem': 'Dados registrados com sucesso'}), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

    finally:
        cursor.close()

@app.route('/excluir', methods=['DELETE'])
def excluir_dados():
    try:
        request_data = request.get_json()
        registro_id = request_data.get('id')

        if not registro_id:
            return jsonify({'erro': 'Id não encontrado'}), 400

        cursor = conexao.cursor()

        cursor.execute('DELETE FROM "NOTAS_GERAIS" WHERE id = %s', (registro_id,))
        conexao.commit()

        return jsonify({'mensagem': 'Dado excluído com sucesso'}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

    finally:
        cursor.close()

@app.route('/excluir_all', methods=['DELETE'])
def excluir_all():
    try:
        cursor = conexao.cursor()

        cursor.execute('DELETE FROM "NOTAS_GERAIS"')
        conexao.commit()

        return jsonify({'mensagem': 'Todos os dados foram deletados com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()

@app.route('/editar', methods=['PUT'])
def editar_dados():
    try:
        request_data = request.get_json()
        edit_id = request_data.get('id')
        novo_titulo = request_data.get('titulo')
        nova_descricao = request_data.get('descricao')

        if not edit_id or not novo_titulo or not nova_descricao:
            return jsonify({'erro': 'Id, título e descrição são obrigatórios'}), 400

        cursor = conexao.cursor()

        cursor.execute('UPDATE "NOTAS_GERAIS" SET titulo = %s, descricao = %s WHERE id = %s', (novo_titulo, nova_descricao, edit_id))
        conexao.commit()

        return jsonify({'mensagem': 'Dados alterados com sucesso!'}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
            cursor.close();



@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
