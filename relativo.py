import os
import sys

#CAMINHO BASE DO SCRIPT OU DO EXECUTÁVEL
def caminho_relativo(caminho):
    try:
        #QUANDO EMPACOTADO COM PYINSTALLER
        base= sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")

    return os.path.join(base, caminho)

