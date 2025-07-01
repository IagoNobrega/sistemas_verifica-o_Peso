from flask import Blueprint, request, jsonify
from src.models.peca import db, Peca, Verificacao
import random
import string
from datetime import datetime

peca_bp = Blueprint('peca', __name__)

@peca_bp.route('/pecas', methods=['GET'])
def listar_pecas():
    """Lista todas as peças ativas"""
    try:
        pecas = Peca.query.filter_by(ativo=True).all()
        return jsonify([peca.to_dict() for peca in pecas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@peca_bp.route('/pecas', methods=['POST'])
def criar_peca():
    """Cria uma nova peça"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        if not data.get('peso_unitario') or data.get('peso_unitario') <= 0:
            return jsonify({'error': 'Peso unitário deve ser maior que zero'}), 400
        if not data.get('quantidade_padrao') or data.get('quantidade_padrao') <= 0:
            return jsonify({'error': 'Quantidade padrão deve ser maior que zero'}), 400
        
        # Verifica se já existe uma peça com o mesmo nome
        peca_existente = Peca.query.filter_by(nome=data['nome']).first()
        if peca_existente:
            return jsonify({'error': 'Já existe uma peça com este nome'}), 400
        
        peca = Peca(
            nome=data['nome'],
            peso_unitario=float(data['peso_unitario']),
            quantidade_padrao=int(data['quantidade_padrao']),
            tolerancia_peso=float(data.get('tolerancia_peso', 0.1))
        )
        
        db.session.add(peca)
        db.session.commit()
        
        return jsonify(peca.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@peca_bp.route('/pecas/<int:peca_id>', methods=['PUT'])
def atualizar_peca(peca_id):
    """Atualiza uma peça existente"""
    try:
        peca = Peca.query.get_or_404(peca_id)
        data = request.get_json()
        
        if 'nome' in data:
            peca.nome = data['nome']
        if 'peso_unitario' in data:
            peca.peso_unitario = float(data['peso_unitario'])
        if 'quantidade_padrao' in data:
            peca.quantidade_padrao = int(data['quantidade_padrao'])
        if 'tolerancia_peso' in data:
            peca.tolerancia_peso = float(data['tolerancia_peso'])
        
        db.session.commit()
        return jsonify(peca.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@peca_bp.route('/pecas/<int:peca_id>', methods=['DELETE'])
def deletar_peca(peca_id):
    """Desativa uma peça (soft delete)"""
    try:
        peca = Peca.query.get_or_404(peca_id)
        peca.ativo = False
        db.session.commit()
        return jsonify({'message': 'Peça desativada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def gerar_codigo_verificacao():
    """Gera um código único para a verificação"""
    return 'VER-' + ''.join(random.choices(string.digits, k=6))

@peca_bp.route('/verificar', methods=['POST'])
def verificar_peso():
    """Realiza a verificação de peso de uma peça"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('peca_id'):
            return jsonify({'error': 'ID da peça é obrigatório'}), 400
        if not data.get('peso_medido') or data.get('peso_medido') <= 0:
            return jsonify({'error': 'Peso medido deve ser maior que zero'}), 400
        
        peca = Peca.query.get_or_404(data['peca_id'])
        peso_medido = float(data['peso_medido'])
        
        # Calcula a quantidade de peças baseada no peso
        quantidade_calculada = round(peso_medido / peca.peso_unitario)
        
        # Calcula o peso esperado para a quantidade calculada
        peso_esperado = quantidade_calculada * peca.peso_unitario
        
        # Determina o status baseado na tolerância
        diferenca = abs(peso_medido - peso_esperado)
        if diferenca <= peca.tolerancia_peso:
            status = 'OK'
        elif peso_medido < peso_esperado:
            status = 'FALTANDO'
        else:
            status = 'SOBRANDO'
        
        # Gera código único para a verificação
        codigo_verificacao = gerar_codigo_verificacao()
        while Verificacao.query.filter_by(codigo_verificacao=codigo_verificacao).first():
            codigo_verificacao = gerar_codigo_verificacao()
        
        # Cria o registro de verificação
        verificacao = Verificacao(
            peca_id=peca.id,
            peso_medido=peso_medido,
            quantidade_calculada=quantidade_calculada,
            status=status,
            observacoes=data.get('observacoes', ''),
            codigo_verificacao=codigo_verificacao
        )
        
        db.session.add(verificacao)
        db.session.commit()
        
        resultado = {
            'verificacao': verificacao.to_dict(),
            'peso_esperado': peso_esperado,
            'diferenca': diferenca,
            'tolerancia': peca.tolerancia_peso
        }
        
        return jsonify(resultado), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@peca_bp.route('/verificacoes', methods=['GET'])
def listar_verificacoes():
    """Lista as verificações mais recentes"""
    try:
        limit = request.args.get('limit', 50, type=int)
        verificacoes = Verificacao.query.order_by(Verificacao.data_verificacao.desc()).limit(limit).all()
        return jsonify([verificacao.to_dict() for verificacao in verificacoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@peca_bp.route('/verificacoes/<codigo_verificacao>', methods=['GET'])
def obter_verificacao(codigo_verificacao):
    """Obtém uma verificação específica pelo código"""
    try:
        verificacao = Verificacao.query.filter_by(codigo_verificacao=codigo_verificacao).first_or_404()
        return jsonify(verificacao.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Simulação de leitura da balança
@peca_bp.route('/balanca/peso', methods=['GET'])
def obter_peso_balanca():
    """Simula a leitura do peso da balança"""
    try:
        # Em um sistema real, aqui seria feita a comunicação com a balança
        # Por enquanto, vamos simular um peso aleatório
        peso_simulado = round(random.uniform(8.0, 15.0), 2)
        return jsonify({'peso': peso_simulado, 'unidade': 'kg'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

