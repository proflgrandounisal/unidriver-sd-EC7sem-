# Exemplos Práticos: Comunicação Remota e Serialização

Este diretório contém os códigos complementares da aula de Sistemas Distribuídos sobre Marshalling, RPC e RMI. O objetivo é demonstrar na prática como a abstração da comunicação evolui de manipuladores brutos de bytes (Sockets) para chamadas de métodos complexos (RMI).

## Como executar os testes:

Para cada um dos 3 exemplos, a dinâmica é a mesma:
1. Abra um terminal e inicie o arquivo do **Servidor**.
2. Abra um segundo terminal e inicie o arquivo do **Cliente**.

**Importante para o Exemplo 3 (RMI):**
A Invocação de Método Remoto não é nativa da biblioteca padrão do Python. Nós utilizamos o `Pyro5` para atuar como Middleware. Antes de rodar, instale a dependência:
`pip install Pyro5`

**Nota para a Sprint 1 do Projeto (TCC / UniDriver):**
Para fins didáticos e controle exato sobre o tráfego da rede e portas, o projeto prático da disciplina utilizará a abordagem do **Exemplo 1** (Sockets + JSON). O RPC e o RMI são demonstrados aqui para conhecimento arquitetural de mercado e compreensão teórica.
