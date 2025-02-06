import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

load_dotenv();

app = Flask(__name__, static_folder="../Notas-Frontend/static", template_folder="../Notas-Frontend")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, origins = ["https://notas-frontend-tau.vercel.app"])

print("Conexão com o banco de dados realizada com sucesso!")


class Nota(db.Model):
    __tablename__ = 'NOTAS_GERAIS'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)


@app.route('/')
def home():
    return send_from_directory(app.template_folder, "index.html")


@app.route('/notas')
def select():
    try:
        notas = Nota.query.all()
        lista_notas = [{"id": nota.id, "titulo": nota.titulo, "descricao": nota.descricao, "data": nota.data_criacao} for nota in notas]

        return jsonify(lista_notas)
    except SQLAlchemyError as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        registro = request.get_json()
        titulo = registro.get('titulo')
        descricao = registro.get('descricao')

        if not titulo or not descricao:
            return jsonify({'erro': 'Título e descrição são obrigatórios'}), 400

        nova_nota = Nota(titulo=titulo, descricao=descricao, data_criacao=db.func.now())
        db.session.add(nova_nota)
        db.session.commit()

        return jsonify({'mensagem': 'Dados registrados com sucesso'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@app.route('/excluir', methods=['DELETE'])
def excluir_dados():
    try:
        registro = request.get_json()
        id_nota = registro.get('id')

        if not id_nota:
            return jsonify({'erro': 'Preencha o campo'}), 400

        nota = Nota.query.get(id_nota)
        if nota:
            db.session.delete(nota)
            db.session.commit()
            return jsonify({'mensagem': 'Registro deletado com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Nota não encontrada'}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@app.route('/excluir_all', methods=['DELETE'])
def excluir_all():
    try:
        db.session.query(Nota).delete()
        db.session.commit()

        return jsonify({'mensagem': 'Todos os registros foram deletados com sucesso!'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@app.route('/editar', methods=['PUT'])
def editar_dados():
    try:
        registro = request.get_json()
        id_nota = registro.get('id')
        titulo = registro.get('titulo')
        descricao = registro.get('descricao')

        if not id_nota or not titulo or not descricao:
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

        nota = Nota.query.get(id_nota)
        if nota:
            nota.titulo = titulo
            nota.descricao = descricao
            db.session.commit()
            return jsonify({'mensagem': 'Registro atualizado com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Nota não encontrada'}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@app.route('/favicon.ico')
def favicon():
    return "", 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)