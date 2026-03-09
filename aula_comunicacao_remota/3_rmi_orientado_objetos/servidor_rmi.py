import Pyro5.api

# 1. Definimos uma Classe inteira, com estado e métodos.
# A tag @Pyro5.api.expose avisa o Middleware que esta classe pode ser acessada remotamente.
@Pyro5.api.expose
class CalculadoraFinanceira(object):
    def __init__(self):
        self.taxa_juros_padrao = 0.05
        print("[*] Objeto CalculadoraFinanceira instanciado na memória do Servidor.")

    def calcular_juros_compostos(self, capital, tempo):
        print(f"[*] Recebida invocação remota para capital {capital} no tempo {tempo}")
        montante = capital * (1 + self.taxa_juros_padrao) ** tempo
        return round(montante, 2)

    def alterar_taxa(self, nova_taxa):
        self.taxa_juros_padrao = nova_taxa
        print(f"[*] Taxa alterada remotamente para {nova_taxa}")
        return True

# 2. Iniciamos o Daemon do Pyro5 (O Middleware RMI)
daemon = Pyro5.api.Daemon(host="localhost", port=9090)
uri = daemon.register(CalculadoraFinanceira, "calculadora.objeto")

print("[*] Servidor RMI Operacional.")
print(f"[*] URI de acesso do objeto: {uri}")
print("[*] Aguardando invocações de métodos...")

daemon.requestLoop()
