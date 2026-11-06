from flask import Flask, jsonify, request

app = Flask(__name__)

# "Banco de dados" em memória (reinicia quando o servidor reinicia)
tarefas = [
    {"id": 1, "titulo": "Estudar Flask", "concluida": False},
    {"id": 2, "titulo": "Fazer o exercício 9.1", "concluida": True},
]
proximo_id = 3


def buscar_tarefa(tarefa_id):
    return next((t for t in tarefas if t["id"] == tarefa_id), None)


@app.route("/")
def hello_world():
    return jsonify({"mensagem": "Hello, World!", "api": "/tarefas"})


# GET /tarefas -> lista todas
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas), 200


# GET /tarefas/<id> -> busca uma
@app.route("/tarefas/<int:tarefa_id>", methods=["GET"])
def obter_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa), 200


# POST /tarefas -> cria
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    global proximo_id
    dados = request.get_json(silent=True)
    if not dados or "titulo" not in dados:
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400

    nova = {
        "id": proximo_id,
        "titulo": dados["titulo"],
        "concluida": bool(dados.get("concluida", False)),
    }
    tarefas.append(nova)
    proximo_id += 1
    return jsonify(nova), 201


# PUT /tarefas/<id> -> atualiza
@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "Envie um JSON no corpo da requisição"}), 400

    if "titulo" in dados:
        tarefa["titulo"] = dados["titulo"]
    if "concluida" in dados:
        tarefa["concluida"] = bool(dados["concluida"])
    return jsonify(tarefa), 200


# DELETE /tarefas/<id> -> remove
@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def remover_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    tarefas.remove(tarefa)
    return jsonify({"mensagem": f"Tarefa {tarefa_id} removida"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)