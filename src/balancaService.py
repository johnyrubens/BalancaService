import time
import argparse
from balanca.api import get_leitura_liberada, salvar_pesagem, salvar_status
from balanca.port import openPort

def main():
    parser = argparse.ArgumentParser(description='Lê dados enviados pela balança pela porta serial')

    # Adicionando o argumento 'nomeBalanca'
    parser.add_argument('nomeBalanca', type=str, help='Nome da balança a ser usada')

    # Parsing os argumentos
    args = parser.parse_args()

    try:
      ser = openPort(args.nomeBalanca)
      if ser is False:
          salvar_status(9, f"Não foi possivel abrir porta serial {args.nomeBalanca}. {str(e)}", args.nomeBalanca)    
          return
    except Exception as e: 
      salvar_status(9, f"Não foi possivel abrir porta serial {args.nomeBalanca}. {str(e)}", args.nomeBalanca)    
      return

    salvar_status(1, "Serviço com Porta Serial iniciado", args.nomeBalanca)    

    try:
      while True:
          try:
            leitura_liberada = get_leitura_liberada(args.nomeBalanca)
            if leitura_liberada:
                peso = ser.readline().decode().strip()
                if peso: 
                  status, valor, unidade = peso.split(",")
                  if status == "ST":
                    print(f"__pesagem__: {valor}")
                    salvar_pesagem(valor, args.nomeBalanca)
                  elif status == "GS":
                    salvar_status(9, "Peso instável", args.nomeBalanca)
                  elif status == "OL":
                    #print(f"__OLpesagem__: {valor}")
                    salvar_status(9, "Sobrepeso detectado", args.nomeBalanca)
                  elif  status == "Er":
                    salvar_status(9, "Erro na balança. Verifique o equipamento.", args.nomeBalanca)
                  else:  
                    salvar_status(9, "Balança desligada", args.nomeBalanca)
            else:
                print("Leitura não liberada")       

            time.sleep(1) 
          except Exception as e:
              salvar_status(9, 'A operação de E/S foi anulada devido a uma saída de thread ou a uma requisição de aplicativo.Verifique conexão com a balança', args.nomeBalanca)
              break

    except KeyboardInterrupt:
        salvar_status(9, "Serviço com Porta Serial da Balança encerrado", args.nomeBalanca)
        print(f"programa encerrado")

if __name__ == "__main__":
    main()
          