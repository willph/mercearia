import cx_Freeze
import sys


base = None

if sys.platform == 'win32':
    base = "Win32GUI"

#executables = [cx_Freeze.Executable("controle-de-estoque.py", base=base, icon="loja.ico")]
executables = [cx_Freeze.Executable("listadecompra.py", base=base, icon="loja.icon")]

cx_Freeze.setup(
    name = "MERCEARIA DO WILL",
    #name = "CONTROLE DE ESTOQUE MERCEARIA DO WILL",
    options = {"build_exe": {"packages":["tkinter"], "include_files":["loja.ico"]}},
    version = "2.0.0",
    description = "SISTEMA DE CAIXA",
    #description = "SISTEMA DE CAIXA CONTROLE DE ESTOQUE",
    executables = executables
    )
