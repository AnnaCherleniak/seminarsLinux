import subprocess


def command_find(command: str, text: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if not result.returncode:
        my_list = out.split('\n')
        if text in my_list:
            return True
        else:
            return False


if __name__ == '__main__':
    print(command_find('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))
