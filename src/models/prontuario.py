from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Prontuario(db.Model):
    __tablename__ = 'prontuarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    paciente_id = db.Column(db.String(36), db.ForeignKey('pacientes.id'), nullable=False)
    consulta_id = db.Column(db.String(36), db.ForeignKey('consultas.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conteudo': self.conteudo,
            'paciente_id': self.paciente_id,
            'consulta_id': self.consulta_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

