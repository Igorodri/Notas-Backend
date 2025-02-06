from flask import Flask, render_template, jsonify, request, send_from_directory
import pymysql

app = Flask(__name__, static_folder="../Notas-Frontend/static", template_folder="../Notas-Frontend");

conexao = pymysql.connect(
    host='127.0.0.1',
    database='notas',
    port=3306,
    user='root',
    password=''
)

print("Conexão com o banco de dados realizada com sucesso!");

@app.route('/')
def home():
    page = send_from_directory(app.template_folder, "index.html")
    return page;

@app.route('/notas')
def select():
    cursor = conexao.cursor()

    try:
        
        cursor.execute("SELECT * FROM NOTAS_GERAIS")
        notas = cursor.fetchall()  

        lista_notas = [{"id": nota[0], "titulo": nota[1], "descricao": nota[2], "data": nota[3]} for nota in notas]

        return jsonify(lista_notas)
    except Exception as e:
        return jsonify({"erro": str(e)})
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
        cursor.execute("INSERT INTO NOTAS_GERAIS (titulo, descricao, data_criacao) VALUES (%s, %s, NOW())", (titulo, descricao))
        conexao.commit()

        return jsonify({'mensagem': 'Dados registrados com sucesso'}), 201 

    except Exception as e:
        return jsonify({'erro': 'Erro ao registrar dados'}), 500  
    finally:
        cursor.close()
  


@app.route('/excluir', methods=['DELETE'])
def excluir_dados():
    try:
        registro = request.get_json();
        id = registro.get('id');

        if not id:
            return jsonify({'erro': 'Preencha o campo'});

        cursor = conexao.cursor();
        cursor.execute('DELETE FROM NOTAS_GERAIS WHERE ID = %s', (id));
        conexao.commit();
        cursor.close();

        return jsonify({'mensagem': 'Registros deletados com sucesso!'});

    except Exception as e:
        return jsonify({'Erro': 'Erro na exclusão dos dados'}),500
    finally:
        cursor.close()


@app.route('/excluir_all', methods=['DELETE'])
def excluir_all():
    try:
        cursor = conexao.cursor();
        cursor.execute('TRUNCATE TABLE NOTAS_GERAIS');
        conexao.commit();
        cursor.close();

        return jsonify({'mensagem': 'Todos os registros foram deletados com sucesso!'});

    except Exception as e:
        return jsonify({'Erro': 'Erro na exclusão dos dados'}),500
    finally:
        cursor.close()
    

        
    

@app.route('/editar')
def editar_dados():
    return 0;






@app.route('/favicon.ico')
def favico():
    return "", 204;

if __name__ == "__main__":
    app.run(debug=True);
    
        


