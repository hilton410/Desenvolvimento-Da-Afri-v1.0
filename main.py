# ==================================================
# MAIN.PY - Interface CLI para a Linguagem afri
# ==================================================
import sys

def main(argv: list[str]):
    try:
        from afri.management import command_line, execute_file

        if len(argv) > 1:
            execute_file(argv[1])
        else:
            command_line()
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar Afri. Verifique "
            "se está tudo instalado corretamente."
        ) from exc

if __name__ == "__main__":
    main(sys.argv)