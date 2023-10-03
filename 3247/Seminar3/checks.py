import subprocess


def checkout(command: str, text: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    return False


def checkout_negative(command: str, text: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.PIPE)
    if text in result.stdout or text in result.stderr:
        return True
    return False


def getout(command: str):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

