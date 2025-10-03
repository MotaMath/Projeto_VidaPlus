from flask import Blueprint, request, jsonify
from src.models.consulta import Consulta, db
from src.models.paciente import Paciente
from src.models.profissional import ProfissionalSaude
from datetime import datetime

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas', methods=['POST'])
def criar_consulta():
    try:
        data = request.get_json()
        
        # Validação básica
        required_fields = ['data_hora', 'tipo', 'paciente_id', 'profissional_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        # Verificar se paciente e profissional existem
        paciente = Paciente.query.get(data['paciente_id'])
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        profissional = ProfissionalSaude.query.get(data['profissional_id'])
        if not profissional:
            return jsonify({'error': 'Profissional não encontrado'}), 404
        
        # Converter data e hora
        data_hora = datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00'))
        
        consulta = Consulta(
            data_hora=data_hora,
            tipo=data['tipo'],
            paciente_id=data['paciente_id'],
            profissional_id=data['profissional_id'],
            observacoes=data.get('observacoes')
        )
        
        db.session.add(consulta)
        db.session.commit()
        
        return jsonify(consulta.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/consultas/<consulta_id>', methods=['GET'])
def obter_consulta(consulta_id):
    try:
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            return jsonify({'error': 'Consulta não encontrada'}), 404
        
        return jsonify(consulta.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/consultas', methods=['GET'])
def listar_consultas():
    try:
        consultas = Consulta.query.all()
        return jsonify([consulta.to_dict() for consulta in consultas])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/consultas/<consulta_id>', methods=['PUT'])
def atualizar_consulta(consulta_id):
    try:
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            return jsonify({'error': 'Consulta não encontrada'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'status' in data:
            consulta.status = data['status']
        if 'observacoes' in data:
            consulta.observacoes = data['observacoes']
        
        db.session.commit()
        
        return jsonify(consulta.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/consultas/<consulta_id>', methods=['DELETE'])
def cancelar_consulta(consulta_id):
    try:
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            return jsonify({'error': 'Consulta não encontrada'}), 404
        
        consulta.status = 'cancelada'
        db.session.commit()
        
        return jsonify({'message': 'Consulta cancelada com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

