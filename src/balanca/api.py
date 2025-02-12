import requests
import os 
from dotenv import load_dotenv

""" definir variável de ambiente BUILD_ENV para development ou production
    set BUILD_ENV=development 
    set BUILD_ENV=production

    compilar o arquivo balancaService.py
    pyinstaller --onefile balancaService.py
""" 

build_env = os.getenv("BUILD_ENV", "development").strip()   
if build_env == "development":
    print("Build Environment: development")    
    base_url = "http://localhost:8080/balanca"
elif build_env == "production":
    print("Build Environment: production")    
    base_url = "http://172.16.90.2:8080/balanca"
else:
    print("Build Environment: development") 
    base_url = "http://localhost:8080/balanca"


headers = {'Content-Type': 'application/json'}

def get_balanca_parametros(nome_balanca):
    url = f"{base_url}/parametros?nomeBalanca={nome_balanca}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar parâmetros da balança: {e}")
        return None

def get_leitura_liberada(nome_balanca):
    """Verifica se a leitura da balança está liberada."""
    url = f"{base_url}/leitura-liberada?nomeBalanca={nome_balanca}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        leitura_liberada = data.get("leituraLiberada", 0) 
        return leitura_liberada == 1
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar status da balança: {e}")
        return False

def salvar_pesagem(peso, nome_balanca):
    """Envia o peso lido para o servidor."""
    url = f"{base_url}/pesagem"
    payload = {"nomeBalanca": nome_balanca, "peso": peso.strip()}

    try:
        requests.post(url, json=payload, headers=headers)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar peso: {e}")
        return False        

def salvar_status(status, desr_status, nome_balanca):
    """Envia o status da balança para o servidor."""
    url = f"{base_url}/status"
    payload = {"nomeBalanca": nome_balanca, "statusBalanca": status, "descrStatusBalanca": desr_status}

    try:
        requests.post(url, json=payload, headers=headers)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar peso: {e}")
        return False        
