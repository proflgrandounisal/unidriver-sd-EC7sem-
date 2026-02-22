import socket
import json
import time
import random

# --- CONFIGURAÇÕES ---
# Se for testar em PCs diferentes, coloque o IP do servidor aqui
HOST = 'localhost' 
PORT = 5000

# --- RELÓGIO LÓGICO DO CLIENTE ---
relogio_cliente = 0

def limpar_tela():
    print("\n" * 2)

def conectar_e_pedir():
    global relogio_cliente
    
    while True: # Loop Infinito de Tolerância a Falhas (Sprint 4)
        try:
            # Tenta criar o socket e conectar
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(5) # Se o servidor não responder em 5s, dá erro
            cliente.connect((HOST, PORT))
            
            print(f"✅ Conectado ao UniDriver! (Clock: {relogio_cliente})")
            
            while True:
                input("\nPressione ENTER para pedir uma corrida (ou Ctrl+C para sair)...")
                
                # Incrementa relógio antes do evento
                relogio_cliente += 1
                
                # Monta o pacote (Marshalling)
                pedido = {
                    "acao": "SOLICITAR_CORRIDA",
                    "passageiro": "Aluno_UNISAL",
                    "origem": "Laboratório",
                    "relogio": relogio_cliente
                }
                
                print("Enviando pedido...")
                cliente.sendall(json.dumps(pedido).encode('utf-8'))
                
                # Espera resposta
                dados = cliente.recv(1024)
                if not dados: break
                
                resposta = json.loads(dados.decode('utf-8'))
                
                # Atualiza relógio lógico (Sincronização)
                relogio_servidor = resposta.get('relogio', 0)
                relogio_cliente = max(relogio_cliente, relogio_servidor) + 1
                
                print(f"📩 Resposta da Central [Clock {relogio_cliente}]:")
                print(f"   Status: {resposta['status']}")
                print(f"   Mensagem: {resposta['msg']}")

        except (socket.error, socket.timeout) as e:
            # --- TOLERÂNCIA A FALHAS ---
            print(f"⚠️  ERRO: Servidor indisponível ou caiu ({e}).")
            print("⏳ Tentando reconectar em 3 segundos...")
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        finally:
            try:
                cliente.close()
            except:
                pass

if __name__ == "__main__":
    conectar_e_pedir()
