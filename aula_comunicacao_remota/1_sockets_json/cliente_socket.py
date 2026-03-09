import socket
import json

HOST = 'localhost'
PORT = 6000

def solicitar_servico():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    
    # Objeto nativo da linguagem (Dicionário)
    pedido = {
        "cliente": "Aluno UNISAL",
        "servico": "Calculo de Taxa",
        "valor_base": 100.0
    }
    
    # Marshalling: Transformando o objeto em fluxo de bytes
    payload = json.dumps(pedido).encode('utf-8')
    print("[*] Enviando dados serializados...")
    cliente.sendall(payload)
    
    # Unmarshalling da resposta
    resposta_bytes = cliente.recv(1024)
    resposta = json.loads(resposta_bytes.decode('utf-8'))
    
    print(f"[*] Resposta do Servidor: {resposta}")
    cliente.close()

if __name__ == "__main__":
    solicitar_servico()
