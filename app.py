from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
import psutil
import subprocess
import docker
import json
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

# Configuração da autenticação básica
app.config['BASIC_AUTH_USERNAME'] = 'user'  # Substitua pelo nome de usuário desejado
app.config['BASIC_AUTH_PASSWORD'] = 'senha'   # Substitua pela senha desejada
basic_auth = BasicAuth(app)

# Função para obter a hora atual em Brasília
def get_current_time_in_brasilia():
    brasilia = timezone('America/Sao_Paulo')
    return datetime.now(brasilia).strftime('%Y-%m-%d %H:%M:%S %Z%z')

# Função para obter informações sobre o sistema
def get_system_info():
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    return {
        "processador": f"{cpu_usage}%",
        "memoria": f"{memory_usage}%"
    }

# Função para obter informações sobre os processos gerenciados pelo PM2
def get_pm2_info():
    try:
        pm2_process_info = subprocess.run(['pm2', 'jlist'], stdout=subprocess.PIPE)
        pm2_info = pm2_process_info.stdout.decode()
        pm2_info = json.loads(pm2_info)
    except Exception as e:
        pm2_info = {"error": str(e)}

    return {
        "pm2": pm2_info
    }

# Função para obter informações sobre os contêineres Docker em execução
def get_docker_info():
    try:
        docker_client = docker.from_env()
        containers = docker_client.containers.list()
        docker_info = []

        for container in containers:
            container_stats = container.stats(stream=False)
            container_name = container.name
            cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
            mem_usage = container_stats['memory_stats']['usage'] / (1024 * 1024)  # Converter para MB

            docker_info.append({
                "container": container_name,
                "status": container.status,
                "cpu_usage": cpu_percent,
                "mem_usage": mem_usage
            })
    except Exception as e:
        docker_info = {"error": str(e)}

    return {
        "docker": docker_info
    }

@app.route('/api', methods=['GET'])
@basic_auth.required  # Requer autenticação básica para acessar esta rota
def get_info():
    # Coleta de informações
    system_info = get_system_info()
    pm2_info = get_pm2_info()
    docker_info = get_docker_info()

    # Obter a hora atual em Brasília
    current_time = get_current_time_in_brasilia()

    # Preparar dados para retorno como JSON
    data = {
        "data_hora_brasilia": current_time,
        "processador": system_info["processador"],
        "memoria": system_info["memoria"],
        **pm2_info,
        **docker_info
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
