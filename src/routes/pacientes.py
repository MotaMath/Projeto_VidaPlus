from flask import Blueprint, request, jsonify
from src.models.paciente import Paciente, db
from datetime import datetime

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['POST'])
def criar_paciente():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('cpf'):
            return jsonify({'error': 'Nome e CPF são obrigatórios'}), 400
        
        # Verificar se CPF já existe
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'error': 'CPF já cadastrado'}), 400
        
        # Converter data de nascimento
        data_nascimento = None
        if data.get('data_nascimento'):
            data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        paciente = Paciente(
            nome=data['nome'],
            data_nascimento=data_nascimento,
            cpf=data['cpf'],
            endereco=data.get('endereco'),
            telefone=data.get('telefone'),
            email=data.get('email') # type: ignore
        )
        db.session.add(paciente)
        db.session.commit()
        
        return jsonify(paciente.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pacientes_bp.route('/pacientes/<paciente_id>', methods=['GET'])
def obter_paciente(paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        return jsonify(paciente.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pacientes_bp.route('/pacientes', methods=['GET'])
def listar_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify([paciente.to_dict() for paciente in pacientes])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pacientes_bp.route('/pacientes/<paciente_id>', methods=['PUT'])
def atualizar_paciente(paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos
        if 'nome' in data:
            paciente.nome = data['nome']
        if 'endereco' in data:
            paciente.endereco = data['endereco']
        if 'telefone' in data:
            paciente.telefone = data['telefone']
        if 'email' in data:
            paciente.email = data['email']
        
        db.session.commit()
        
        return jsonify(paciente.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pacientes_bp.route('/pacientes/<paciente_id>', methods=['DELETE'])
def deletar_paciente(paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        db.session.delete(paciente)
        db.session.commit()
        
        return jsonify({'message': 'Paciente deletado com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

