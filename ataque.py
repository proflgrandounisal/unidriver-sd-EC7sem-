import socket
import json
import threading
import time

HOST = 'localhost'
PORT = 5000

def tentar_pegar_motorista(id_passageiro):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        pedido = {
            "acao": "SOLICITAR_CORRIDA", 
            "passageiro": f"Passageiro_{id_passageiro}",
            "relogio": 1
        }
        
        s.sendall(json.dumps(pedido).encode('utf-8'))
        resp = s.recv(1024)
        dados = json.loads(resp.decode('utf-8'))
        
        print(f"[{id_passageiro}] Resultado: {dados['status']} - {dados.get('msg')}")
        s.close()
    except:
        pass

print("🔥 INICIANDO ATAQUE DE CONCORRÊNCIA...")
threads = []
for i in range(5): # 5 passageiros ao mesmo tempo
    t = threading.Thread(target=tentar_pegar_motorista, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
