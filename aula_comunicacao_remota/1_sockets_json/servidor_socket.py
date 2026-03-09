import socket
import json

HOST = 'localhost'
PORT = 6000

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    
    print(f"[*] Servidor Socket ouvindo na porta {PORT}...")
    
    while True:
        conn, addr = servidor.accept()
        print(f"[+] Conexão de {addr}")
        
        # 1. Recebe o fluxo de bytes puro da rede
        dados_bytes = conn.recv(1024)
        if dados_bytes:
            # 2. Unmarshalling: Decodifica os bytes e converte de JSON para Dicionário Python
            mensagem = json.loads(dados_bytes.decode('utf-8'))
            print(f"[*] Objeto recebido na memória: {mensagem}")
            
            # Processamento local
            resposta_dit = {"status": "Sucesso", "servico": mensagem["servico"], "taxa": 15.50}
            
            # 3. Marshalling: Converte o Dicionário para JSON e depois codifica para Bytes
            conn.sendall(json.dumps(resposta_dit).encode('utf-8'))
            
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()
