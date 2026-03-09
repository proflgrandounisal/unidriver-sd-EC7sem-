import xmlrpc.client

# 1. Criação do "Client Stub" (Proxy)
# Ele finge ser o servidor localmente
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print("[*] Conectado ao Middleware RPC.")

# 2. Chamada transparente (A mágica do RPC)
# Parece uma função local, mas os parâmetros trafegam pela rede em formato XML
imposto = proxy.calcular_imposto(250.0)
status = proxy.verificar_status_servidor()

print(f"[*] Status da Rede: {status}")
print(f"[*] O imposto calculado remotamente é: R$ {imposto}")
