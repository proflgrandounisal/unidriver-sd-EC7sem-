# Laboratório Prático: Fundamentos do UniDriver

Bem-vindos ao repositório base do projeto UniDriver. Este código representa a implementação completa do nosso sistema de transporte distribuído, cobrindo os conceitos de Arquitetura Cliente-Servidor, Transparência, Concorrência e Tolerância a Falhas.

O objetivo do laboratório de hoje é executar a infraestrutura base e validar tecnicamente os desafios que terão de resolver nas Sprints do projeto.

## Estrutura do Repositório
- `servidor.py`: O nó central (Central UniDriver) que gerencia os recursos compartilhados (motoristas) e utiliza Threads para atender múltiplos clientes em simultâneo.
- `cliente.py`: O nó cliente (Passageiro) que faz pedidos e implementa tolerância a falhas.
- `ataque.py`: O nosso script de testes de estresse para validar o controle de concorrência.



---

## Laboratório 1: Arquitetura e Transparência de Acesso

Vamos observar a separação rigorosa de papéis na rede e como os dados são serializados (Marshalling) para trafegar.

### Como testar:
1. Abra um terminal e inicie a Central UniDriver:
   ```bash
   python servidor.py

```

2. Abra um segundo terminal e inicie o Passageiro:
```bash
python cliente.py

```


3. Pressione ENTER no cliente para solicitar uma corrida.

**Desafio para a equipe:** Reparem que o dicionário de dados em Python no cliente foi transformado num formato universal (JSON) antes de ser enviado para o servidor. Que tipo de Transparência de Coulouris é garantida por esta conversão (Marshalling e Unmarshalling)?

---

## Laboratório 2: Tolerância a Falhas e Resiliência

Um sistema distribuído tem de ocultar as falhas da rede ao usuário final (Transparência de Falhas). Vamos testar como o nosso cliente lida com a queda do servidor.

### Como testar:

1. Com o `cliente.py` em execução e conectado ao servidor, volte ao terminal do servidor e pare o processo (pressione `Ctrl+C`).
2. Tente pedir uma corrida no cliente.
3. Observe que o cliente não "crasha". Ele entra num laço infinito de tentativas de reconexão.
4. Reinicie o `servidor.py` e veja o cliente restabelecer a conexão automaticamente.

**Desafio para a equipe:** Analisem o bloco `try/except` no arquivo `cliente.py`. Como esta abordagem protege o sistema e qual é o limite de tempo estipulado (`timeout`)?

---

## Laboratório 3: Threads e o Controle de Concorrência

Como o servidor utiliza Threads para aceitar conexões simultâneas, temos o problema do compartilhamento de memória (Recurso Crítico). Sem controle, dois passageiros poderiam reservar o mesmo motorista ao mesmo tempo.

### Como testar:

1. Garanta que o `servidor.py` está rodando num terminal.
2. Em outro terminal, execute o nosso script de estresse:
```bash
python ataque.py

```


3. Este script lança 5 clientes (Threads) em simultâneo contra o servidor num ataque de concorrência.

**Desafio para a equipe:** Na tela, verão que apenas um pedido é "ACEITO" e os outros quatro recebem a mensagem "NEGADO". Analisem a linha com `lock_motorista` (o Mutex) na Zona Crítica do `servidor.py`. Se comentarem essa linha e rodarem o ataque novamente, o que acontece com a integridade do sistema?

---

## Exemplos de Testes (Evidências para a Sprint)

Para a entrega do Relatório Técnico, vocês deverão rodar os testes abaixo e capturar as telas (prints) comprovando o funcionamento da arquitetura distribuída.

### Teste 1: Bloqueio de Recurso Crítico (Mutex)

* **Objetivo:** Provar que o sistema impede reservas duplicadas.
* **Execução:** Com o servidor ligado, rode o comando `python ataque.py`.
* **Evidência Esperada:** Tire um print do terminal de ataque mostrando exatamente a saída onde um Passageiro recebe o Status "ACEITO" e os demais recebem "NEGADO".

### Teste 2: Sincronização de Relógios (Lamport)

* **Objetivo:** Provar que os eventos no sistema distribuído estão ordenados no tempo de forma lógica, mesmo em máquinas diferentes.
* **Execução:** Ligue o servidor e conecte um cliente. Faça três pedidos de corrida espaçados por alguns segundos.
* **Evidência Esperada:** Tire um print do terminal do servidor (`Log de Auditoria`) mostrando a tag `[CLOCK: X]` incrementando sequencialmente a cada ação.

### Teste 3: Recuperação de Desastres

* **Objetivo:** Provar que o cliente sobrevive à falha do nó central.
* **Execução:** Com o cliente conectado, derrube o servidor (`Ctrl+C`). Tire um print do cliente mostrando a mensagem de falha e tentativa de reconexão ("Tentando reconectar..."). Em seguida, suba o servidor novamente e tire outro print do cliente informando que a conexão foi restabelecida com sucesso.

```

```
