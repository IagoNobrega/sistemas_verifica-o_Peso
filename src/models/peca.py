from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Peca(db.Model):
    __tablename__ = 'pecas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    peso_unitario = db.Column(db.Float, nullable=False)  # em kg
    quantidade_padrao = db.Column(db.Integer, nullable=False)  # peças por caixa
    tolerancia_peso = db.Column(db.Float, nullable=False, default=0.1)  # tolerância em kg
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Peca {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'peso_unitario': self.peso_unitario,
            'quantidade_padrao': self.quantidade_padrao,
            'tolerancia_peso': self.tolerancia_peso,
            'ativo': self.ativo
        }

class Verificacao(db.Model):
    __tablename__ = 'verificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    peca_id = db.Column(db.Integer, db.ForeignKey('pecas.id'), nullable=False)
    peso_medido = db.Column(db.Float, nullable=False)  # em kg
    quantidade_calculada = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'OK', 'FALTANDO', 'SOBRANDO'
    data_verificacao = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    observacoes = db.Column(db.Text)
    codigo_verificacao = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamento
    peca = db.relationship('Peca', backref=db.backref('verificacoes', lazy=True))
    
    def __repr__(self):
        return f'<Verificacao {self.codigo_verificacao}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'peca_id': self.peca_id,
            'peca_nome': self.peca.nome if self.peca else None,
            'peso_medido': self.peso_medido,
            'quantidade_calculada': self.quantidade_calculada,
            'status': self.status,
            'data_verificacao': self.data_verificacao.isoformat() if self.data_verificacao else None,
            'observacoes': self.observacoes,
            'codigo_verificacao': self.codigo_verificacao
        }

