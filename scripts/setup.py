import os
import subprocess
import sys
import platform

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {command}\nErro: {e}")
        sys.exit(1)

def setup_env():
    project = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv = os.path.join(project, ".venv")
    requirements = os.path.join(project, "requirements.txt")

    os.chdir(project)

    if not os.path.exists(venv):
        print(f"Criando ambiente virtual: {venv}")
        run_command(f'"{sys.executable}" -m venv .venv')

    if platform.system() == "Windows":
        pip_executable = os.path.join(venv, "Scripts", "pip.exe")
    else:
        pip_executable = os.path.join(venv, "bin", "pip")

    if os.path.exists(requirements):
        print("Atualizando dependências...")
        run_command(f'"{pip_executable}" install -r "{requirements}"')
        print("\nSetup concluído com sucesso!")

if __name__ == "__main__":
    setup_env()