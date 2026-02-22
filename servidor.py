import socket
import threading
import json
import time

# --- CONFIGURAÇÕES ---
HOST = '0.0.0.0'  # Ouve em todas as interfaces de rede
PORT = 5000       # Porta de comunicação

# --- ESTADO GLOBAL (MEMÓRIA COMPARTILHADA) ---
# Simula que só existe UM motorista disponível no sistema
motorista_disponivel = True
nome_motorista = "Seu Zé (Fiat Uno com Escada)"

# --- CONTROLE DE CONCORRÊNCIA (MUTEX) - SPRINT 2 ---
# Sem este Lock, dois clientes poderiam pegar o motorista ao mesmo tempo!
lock_motorista = threading.Lock()

# --- RELÓGIO LÓGICO (LAMPORT) - SPRINT 3 ---
relogio_servidor = 0

def atender_cliente(conn, endereco):
    global relogio_servidor, motorista_disponivel
    
    print(f"[{endereco}] Conectado.")

    try:
        while True:
            # 1. Recebe os bytes (bloqueante)
            dados_bytes = conn.recv(1024)
            if not dados_bytes: 
                break

            # 2. Unmarshalling (Bytes -> JSON -> Dicionário)
            mensagem = json.loads(dados_bytes.decode('utf-8'))
            
            # 3. Atualiza Relógio de Lamport (Max(Local, Recebido) + 1)
            relogio_cliente = mensagem.get('relogio', 0)
            relogio_servidor = max(relogio_servidor, relogio_cliente) + 1
            
            acao = mensagem.get('acao')
            print(f"[CLOCK: {relogio_servidor}] Cliente pede: {acao}")

            resposta = {}

            # --- ZONA CRÍTICA (INICIO) ---
            if acao == 'SOLICITAR_CORRIDA':
                with lock_motorista: # TRAVA O RECURSO
                #if True: #simular ataque.
                    if motorista_disponivel:
                        print(f"--- Processando pedido de {endereco} ---")
                        time.sleep(3) # Simula tempo de processamento (para testar concorrencia)
                        
                        motorista_disponivel = False
                        resposta = {
                            "status": "ACEITO", 
                            "msg": f"Motorista {nome_motorista} a caminho!",
                            "relogio": relogio_servidor
                        }
                        
                        # Libera o motorista após 10s (simulação)
                        threading.Timer(10, liberar_motorista).start()
                    else:
                        resposta = {
                            "status": "NEGADO", 
                            "msg": "Motorista ocupado. Tente novamente.",
                            "relogio": relogio_servidor
                        }
                # O Lock é liberado automaticamente aqui
            # --- ZONA CRÍTICA (FIM) ---
            
            else:
                resposta = {"status": "ERRO", "msg": "Comando desconhecido"}

            # 4. Marshalling e Envio (Dicionário -> JSON -> Bytes)
            conn.sendall(json.dumps(resposta).encode('utf-8'))

    except Exception as e:
        print(f"Erro com cliente {endereco}: {e}")
    finally:
        conn.close()
        print(f"[{endereco}] Desconectado.")

def liberar_motorista():
    global motorista_disponivel, relogio_servidor
    with lock_motorista:
        motorista_disponivel = True
        relogio_servidor += 1
        print(f"[CLOCK: {relogio_servidor}] Motorista liberado e pronto para a próxima!")

def iniciar():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"🚖 Central UniDriver OUVINDO na porta {PORT}...")

    while True:
        # Aceita nova conexão e cria uma Thread para ela
        conn, addr = servidor.accept()
        t = threading.Thread(target=atender_cliente, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    iniciar()
