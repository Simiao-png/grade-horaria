from flask import jsonify, session

from models.db import db
from models.disciplina import Disciplina
from models.escola import Escola


def obter_escola_id():
    escola_id = session.get("escola_id")

    if escola_id:
        return int(escola_id)

    escola = (
        db.session.query(Escola)
        .order_by(Escola.id)
        .first()
    )

    return escola.id if escola else None


def disciplina_para_dict(disciplina):
    return {
        "id": disciplina.id,
        "escola_id": disciplina.escola_id,
        "nome": disciplina.nome,
        "cor": disciplina.cor or "#2563EB",
        "ativo": disciplina.ativo
    }


def buscar_disciplina_duplicada(
    escola_id,
    nome,
    ignorar_id=None
):
    query = Disciplina.query.filter(
        Disciplina.escola_id == escola_id,
        db.func.lower(
            db.func.trim(Disciplina.nome)
        ) == nome.strip().lower()
    )

    if ignorar_id is not None:
        query = query.filter(
            Disciplina.id != ignorar_id
        )

    return query.first()


def listar_disciplinas():
    escola_id = obter_escola_id()

    query = Disciplina.query

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    disciplinas = (
        query
        .order_by(Disciplina.nome)
        .all()
    )

    return jsonify([
        disciplina_para_dict(d)
        for d in disciplinas
    ])


def buscar_disciplina(id):
    escola_id = obter_escola_id()

    query = Disciplina.query.filter_by(id=id)

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    disciplina = query.first()

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada"
        }), 404

    return jsonify(
        disciplina_para_dict(disciplina)
    )


def criar_disciplina(dados):
    dados = dados or {}

    escola_id = obter_escola_id()

    if not escola_id:
        return jsonify({
            "erro": (
                "Cadastre uma escola antes de "
                "cadastrar disciplinas."
            )
        }), 400

    nome = str(
        dados.get("nome", "")
    ).strip()

    if not nome:
        return jsonify({
            "erro": "Informe o nome da disciplina."
        }), 400

    duplicada = buscar_disciplina_duplicada(
        escola_id,
        nome
    )

    if duplicada:
        return jsonify({
            "erro": (
                f'A disciplina "{nome}" '
                "já está cadastrada."
            )
        }), 409

    disciplina = Disciplina(
        escola_id=escola_id,
        nome=nome,
        cor=dados.get(
            "cor",
            "#2563EB"
        ),
        ativo=dados.get(
            "ativo",
            True
        )
    )

    db.session.add(disciplina)
    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina criada com sucesso!"
    }), 201


def atualizar_disciplina(id, dados):
    dados = dados or {}

    escola_id = obter_escola_id()

    query = Disciplina.query.filter_by(id=id)

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    disciplina = query.first()

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada"
        }), 404

    nome = str(
        dados.get(
            "nome",
            disciplina.nome
        )
    ).strip()

    if not nome:
        return jsonify({
            "erro": "Informe o nome da disciplina."
        }), 400

    duplicada = buscar_disciplina_duplicada(
        disciplina.escola_id,
        nome,
        ignorar_id=disciplina.id
    )

    if duplicada:
        return jsonify({
            "erro": (
                f'A disciplina "{nome}" '
                "já está cadastrada."
            )
        }), 409

    disciplina.nome = nome
    disciplina.cor = dados.get(
        "cor",
        disciplina.cor
    )
    disciplina.ativo = dados.get(
        "ativo",
        disciplina.ativo
    )

    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina atualizada com sucesso!"
    })


def deletar_disciplina(id):
    escola_id = obter_escola_id()

    query = Disciplina.query.filter_by(id=id)

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    disciplina = query.first()

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada"
        }), 404

    db.session.delete(disciplina)
    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina deletada com sucesso!"
    })


def alternar_status_disciplina(id):
    escola_id = obter_escola_id()

    query = Disciplina.query.filter_by(id=id)

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    disciplina = query.first()

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada"
        }), 404

    disciplina.ativo = not disciplina.ativo

    db.session.commit()

    return jsonify({
        "mensagem": (
            "Status da disciplina atualizado com sucesso!"
        ),
        "ativo": disciplina.ativo
    })