# ==================================================
# MANAGEMENT.PY - Gerenciador de interfaces
# ==================================================
from .afri_interpreter import AfriInterpreter, Token
import os, sys

def afri_header():
    print(
        "==================================================\n"
        "     Afri 1.0 Interpretador - Modo Interativo     \n"
        "    Digita o teu código ou '.sair' para fechar.   \n"
        "      Digite '.ajudar' para mais informações      \n"
        "==================================================\n"
        , end="")

def afri_help():
    print(
        "==================================================\n"
        "     Bem-vindo ao Afri 1.0 se é sua primeira      \n"
        "   Vez a usar o afri vai adorar sua simplicidade  \n"
        "      Digite '.ajudar' para mais informações      \n"
        "==================================================\n"
        " \033[33m'.sair'\033[m: para sair do modo iterativo             \n"
        " \033[33m'.ajudar'\033[m: para saber de mais informações        \n"
        " \033[33m'.limpar'\033[m: para limpar o terminal                \n"
        # " \033[33m'.copyright'\033[m: ...                              \n"
        # " \033[33m'.credits'\033[m:   ...                              \n"
        # " \033[33m'.license'\033[m:   ...                              \n"
        "==================================================\n"
    , end="")

def afri_clear():
    command = ''
    if sys.platform.startswith('win'): command = 'cls'
    elif sys.platform.startswith('linux'): command = 'clear'
    elif sys.platform.startswith('darwin'): command = 'clear'
    os.system(command)

def exec_command(command: str, afri_interpreter: AfriInterpreter):
    output = afri_interpreter.run(command)

    if 'parser_errors' in output:
        for parser_error in output['parser_errors']:
            print(f"\033[31m{parser_error}\033[m")

    if Token.ERROR in output:
        print(f"\033[31m{output[Token.ERROR][0]}: {output[Token.ERROR][2]}, linha {output[Token.ERROR][1]}\033[m")

def exec_code(code: str, afri_interpreter: AfriInterpreter):
    output = afri_interpreter.run(code)
    if 'parser_errors' in output:
        for parser_error in output['parser_errors']:
            print(f"\033[31m{parser_error}\033[m")

    if Token.ERROR in output:
        print(f"\033[31m{output[Token.ERROR][0]}: {output[Token.ERROR][2]}, linha {output[Token.ERROR][1]}\033[m")

    return output['result']

def command_line():
    afri_header()
    afri_interpreter = AfriInterpreter()
    while True:
        try:
            command = input("\033[33mafri > \033[m")
            match command.strip().lower():
                case ".sair":
                    break
                case ".ajudar":
                    afri_help()
                case ".limpar":
                    afri_clear()
                    afri_header()
                case _:
                    exec_command(command, afri_interpreter)
        except KeyboardInterrupt:
            break

def execute_file(filepath: str):
    filepath = os.path.realpath(filepath)

    if not os.path.isfile(filepath):
        print(f"\033[31mafri\033[m: o caminho não é um ficheiro: \033[31m'{filepath}'\033[m")
        return

    if not filepath.endswith('.af'):
        print("\033[33maviso\033[m: O afri recomenda ficheiros com a extensão \033[33m'.af'\033[m")

    with (open(filepath, 'r', encoding='utf-8') as f):
        afri_code = f.read()

    exec_code(afri_code, AfriInterpreter())