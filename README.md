# Desenvolvimento-Da-Afri-v1.0

Desenvolvimento da versão 1.0 da Afri linguagem de progracão

O **Afri** é uma linguagem de programação interpretada, de código aberto, idealizada,
fundada e desenvolvida por **José Carlos Pipa**.

Construída sobre o ecossistema Python, o seu principal propósito é ser uma ferramenta
educacional e conceitual, trazendo uma sintaxe totalmente baseada na língua portuguesa para
facilitar o aprendizado de lógica de programação e a estrutura de compiladores para a comunidade
tecnológica de Angola e do mundo.

O motor do **Afri** possui um **pipeline clássico** composto:
- **Lexer** (Analisador Léxico)
- **Parser** (Analisador Sintático que gera uma AST)
- e **Interpretador** dinâmico com gestão de memória.

# 1. Como funciona a Afri Language

O arquivo `main.py` é a **CLI (Command Line Interface)** da linguagem responsável pela execução
do programa. Para habilitar o **Modo Iterativo** da linguagem digite:
```shell
python main.py
```
```terminaloutput
==================================================
     Afri 1.0 Interpretador - Modo Interativo
    Digita o teu código ou '.sair' para fechar.
      Digite '.ajudar' para mais informações
==================================================
afri >
```

A linguagem possuí comandos simples em português português para quebrar a barreira do
aprendizado da **lógica de programação**. Por exemplo para imprimir um conteúdo na tela
basta digitar o `ver [argumento]`:

```terminaloutput
==================================================
     Afri 1.0 Interpretador - Modo Interativo
    Digita o teu código ou '.sair' para fechar.
      Digite '.ajudar' para mais informações
==================================================
afri > ver "Olá, Mundo!"
Olá, Mundo!
afri >
```

Caso temos um `arquivo.af` podes executar o comando:
- teste00.af
```textmate
ver "Olá, Mundo!"
ver "Bem-Vindo ao afri v1.0!"
```
```shell
python main.py testes/teste00.af
```
```terminaloutput
Olá, Mundo!
Bem-Vindo ao afri v1.0!
```