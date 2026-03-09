from xmlrpc.server import SimpleXMLRPCServer

# 1. Definimos os procedimentos (funções) isolados
def calcular_imposto(valor):
    print(f"[*] Processando cálculo remoto para o valor: {valor}")
    return valor * 0.15

def verificar_status_servidor():
    return "Servidor RPC Operacional"

# 2. Iniciamos o Middleware (Server Stub)
servidor = SimpleXMLRPCServer(("localhost", 8000))
print("[*] Servidor RPC aguardando chamadas na porta 8000...")

# 3. Registramos as funções para que a rede possa enxergá-las
servidor.register_function(calcular_imposto, "calcular_imposto")
servidor.register_function(verificar_status_servidor, "verificar_status_servidor")

servidor.serve_forever()
