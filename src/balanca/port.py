import serial
import requests
from balanca.api import get_balanca_parametros

def openPort(nome_balanca):
    try:
        parametros = get_balanca_parametros(nome_balanca)
        param_porta = parametros.get('porta')
        param_baudrate = parametros.get('baudrate') 
        param_bytesize = parametros.get('bytesize') 
        param_parity = parametros.get('parity') 
        param_stopbits = parametros.get('stopbits') 
        param_timeout = parametros.get('timeout')   
        ser = serial.Serial(param_porta, baudrate=param_baudrate, bytesize=param_bytesize,
                            parity=param_parity, stopbits=param_stopbits, timeout=param_timeout)
        return ser
    except requests.exceptions.RequestException as e:
        print(f"Erro ao abrir porta serial: {e}")
        return False
