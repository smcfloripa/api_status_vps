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
                "cpu_usage": f"{cpu_percent}%",
                "mem_usage": f"{mem_usage} MB"
            })
    except Exception as e:
        docker_info = {"error": str(e)}

    return {
        "docker": docker_info
    }

# Função para obter informações sobre o consumo de recursos do PHP
def get_php_info():
    php_processes = [process for process in psutil.process_iter(attrs=['pid', 'name']) if 'php' in process.info['name']]
    php_info = []

    for php_process in php_processes:
        pid = php_process.info['pid']
        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent()
        mem_percent = process.memory_percent()
        php_info.append({
            "pid": pid,
            "cpu_percent": f"{cpu_percent}%",
            "mem_percent": f"{mem_percent}%"
        })

    return {
        "php": php_info
    }

# Função para obter informações sobre o consumo de recursos do MariaDB
def get_mariadb_info():
    mariadb_processes = [process for process in psutil.process_iter(attrs=['pid', 'name']) if 'mysqld' in process.info['name']]
    mariadb_info = []

    for mariadb_process in mariadb_processes:
        pid = mariadb_process.info['pid']
        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent()
        mem_percent = process.memory_percent()
        mariadb_info.append({
            "pid": pid,
            "cpu_percent": f"{cpu_percent}%",
            "mem_percent": f"{mem_percent}%"
        })

    return {
        "mariadb": mariadb_info
    }

# Função para obter informações sobre o consumo de recursos do Nginx
def get_nginx_info():
    try:
        # Use o comando 'ps aux' para listar todos os processos e 'grep nginx' para filtrar apenas os relacionados ao Nginx.
        nginx_process_info = subprocess.check_output('ps aux | grep nginx', shell=True, stderr=subprocess.STDOUT)
        nginx_info = nginx_process_info.decode()
    except subprocess.CalledProcessError as e:
        nginx_info = {"error": str(e)}

    return {
        "nginx": nginx_info
    }

# Função para obter informações sobre o espaço em disco em MB
def get_disk_space():
    disk_usage = psutil.disk_usage('/')
    return {
        "disk_total": f"{disk_usage.total / (1024 * 1024):.2f} MB",
        "disk_used": f"{disk_usage.used / (1024 * 1024):.2f} MB",
        "disk_free": f"{disk_usage.free / (1024 * 1024):.2f} MB"
    }

# Função para obter informações sobre a quantidade de acessos externos e consumo de banda em MB
external_access_count = 0
bandwidth_usage = 0  # Em MB

@app.route('/external_access', methods=['GET'])
def external_access():
    global external_access_count
    global bandwidth_usage

    # Lógica para registrar o acesso externo, você pode ajustar isso com base na sua implementação real.
    external_access_count += 1
    # Simulando um consumo de banda de 1 MB por acesso.
    bandwidth_usage += 1

    return "External Access Recorded"

def get_external_access():
    return {
        "external_access_count": external_access_count,
        "bandwidth_usage": f"{bandwidth_usage} MB"
    }

# Função para verificar atualizações com `apt`
def check_apt_update():
    try:
        apt_update_info = subprocess.check_output('apt update', shell=True, stderr=subprocess.STDOUT)
        return apt_update_info.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}"

@app.route('/api', methods=['GET'])
@basic_auth.required  # Requer autenticação básica para acessar esta rota
def get_info():
    # Coleta de informações
    system_info = get_system_info()
    pm2_info = get_pm2_info()
    docker_info = get_docker_info()
    php_info = get_php_info()
    mariadb_info = get_mariadb_info()
    nginx_info = get_nginx_info()

    # Obter a hora atual em Brasília
    current_time = get_current_time_in_brasilia()

    # Preparar dados para retorno como JSON
    data = {
        "data_hora_brasilia": current_time,
        "processador": system_info["processador"],
        "memoria": system_info["memoria"],
        **pm2_info,
        **docker_info,
        **php_info,
        **mariadb_info,
        **nginx_info,
        **get_disk_space(),
        **get_external_access(),
        "apt_update": check_apt_update()
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
