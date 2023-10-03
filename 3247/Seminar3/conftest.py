import pytest
from checks import checkout, getout
import random
import string
import yaml
from datetime import datetime


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(f'mkdir {data["PATH_IN"]} {data["PATH_OUT"]}'
                    f' {data["PATH_EXIT"]} {data["PATH_EXIT2"]}', '')


@pytest.fixture()
def clear_folders():
    return checkout(f'rm -rf {data["PATH_IN"]}/* {data["PATH_OUT"]}/*'
                    f' {data["PATH_EXIT"]}/* {data["PATH_EXIT2"]}/*', '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["PATH_IN"]}; dd if=/dev/urandom of={filename}'
                    f' bs=1M count=1 iflag=fullblock', ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f'cd {data["PATH_IN"]}; mkdir {subfoldername}', ''):
        return None, None
    if not checkout(f'cd {data["PATH_IN"]}/{subfoldername};'
                    f' dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock', ''):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'Stop: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout('cat /proc/loadavg')
    checkout(f'echo "time: {datetime.now().strftime("%H:%M:%S.%f")} count: {data["count"]} load: {stat}">> stat.txt', '')
