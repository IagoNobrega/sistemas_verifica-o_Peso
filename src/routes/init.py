from flask import Blueprint, request, jsonify
from src.models.peca import db, Peca

init_bp = Blueprint('init', __name__)

@init_bp.route('/init-data', methods=['POST'])
def inicializar_dados():
    """Inicializa o banco de dados com peças de exemplo"""
    try:
        # Verifica se já existem peças cadastradas
        if Peca.query.count() > 0:
            return jsonify({'message': 'Dados já foram inicializados'}), 200
        
        # Peças de exemplo baseadas na descrição do usuário
        pecas_exemplo = [
            {'nome': 'M1 Zipa', 'peso_unitario': 1.0, 'quantidade_padrao': 12, 'tolerancia_peso': 0.2},
            {'nome': 'MDL', 'peso_unitario': 1.0, 'quantidade_padrao': 12, 'tolerancia_peso': 0.2},
            {'nome': 'TZ Max', 'peso_unitario': 0.85, 'quantidade_padrao': 10, 'tolerancia_peso': 0.15},
            {'nome': 'PR Standard', 'peso_unitario': 0.75, 'quantidade_padrao': 15, 'tolerancia_peso': 0.1},
            {'nome': 'XL Heavy', 'peso_unitario': 1.5, 'quantidade_padrao': 8, 'tolerancia_peso': 0.3},
            {'nome': 'Mini Compact', 'peso_unitario': 0.5, 'quantidade_padrao': 20, 'tolerancia_peso': 0.1},
            {'nome': 'Super Plus', 'peso_unitario': 1.2, 'quantidade_padrao': 10, 'tolerancia_peso': 0.25},
            {'nome': 'Eco Light', 'peso_unitario': 0.6, 'quantidade_padrao': 18, 'tolerancia_peso': 0.12}
        ]
        
        for peca_data in pecas_exemplo:
            peca = Peca(**peca_data)
            db.session.add(peca)
        
        db.session.commit()
        
        return jsonify({
            'message': f'{len(pecas_exemplo)} peças foram criadas com sucesso',
            'pecas': [peca.nome for peca in Peca.query.all()]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

