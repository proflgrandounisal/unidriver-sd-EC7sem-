import Pyro5.api

# 1. O Cliente precisa do URI (Uniform Resource Identifier) que aponta para o Objeto
uri = "PYRO:calculadora.objeto@localhost:9090"

# 2. Criação do Proxy (O "Skeleton" no jargão RMI)
calculadora_remota = Pyro5.api.Proxy(uri)

print("[*] Invocando método remoto para calcular juros...")
# Acessamos o método do objeto como se ele existisse na nossa memória RAM local
resultado = calculadora_remota.calcular_juros_compostos(1000, 12)
print(f"[*] Resultado do cálculo: R$ {resultado}")

print("[*] Alterando o estado do objeto remoto...")
calculadora_remota.alterar_taxa(0.10)

resultado_novo = calculadora_remota.calcular_juros_compostos(1000, 12)
print(f"[*] Resultado com nova taxa: R$ {resultado_novo}")
