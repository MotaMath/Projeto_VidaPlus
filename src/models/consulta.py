from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    data_hora = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # presencial, telemedicina
    status = db.Column(db.String(20), default='agendada')  # agendada, realizada, cancelada
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    paciente_id = db.Column(db.String(36), db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.String(36), db.ForeignKey('profissionais_saude.id'), nullable=False)
    
    # Relacionamentos
    prontuario = db.relationship('Prontuario', backref='consulta', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'tipo': self.tipo,
            'status': self.status,
            'observacoes': self.observacoes,
            'paciente_id': self.paciente_id,
            'profissional_id': self.profissional_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

