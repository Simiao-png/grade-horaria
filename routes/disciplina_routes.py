from flask import Blueprint, request, render_template

from services.disciplina_service import (
    listar_disciplinas,
    buscar_disciplina,
    criar_disciplina,
    atualizar_disciplina,
    deletar_disciplina,
    alternar_status_disciplina
)

disciplina_bp = Blueprint("disciplina", __name__)


@disciplina_bp.route("/disciplinas/tela")
def tela_disciplinas():
    resposta = listar_disciplinas()
    disciplinas = resposta.get_json()

    return render_template(
        "disciplinas.html",
        disciplinas=disciplinas
    )


@disciplina_bp.route("/disciplinas", methods=["GET"])
def listar():
    return listar_disciplinas()


@disciplina_bp.route("/disciplinas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_disciplina(id)


@disciplina_bp.route("/disciplinas", methods=["POST"])
def criar():
    return criar_disciplina(request.get_json())


@disciplina_bp.route("/disciplinas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_disciplina(
        id,
        request.get_json()
    )


@disciplina_bp.route("/disciplinas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_disciplina(id)


@disciplina_bp.route(
    "/disciplinas/<int:id>/status",
    methods=["PATCH"]
)
def alternar_status(id):
    return alternar_status_disciplina(id)