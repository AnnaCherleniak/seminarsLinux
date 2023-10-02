import pytest

PATH_IN = '/home/anna/homework/test'
PATH_OUT = '/home/anna/homework/out'
PATH_EXIT = '/home/anna/homework/folder1'
PATH_EXIT2 = '/home/anna/homework/folder2'


def checkout(command: str, text: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if not result.returncode:
        my_list = out.split('\n')
        if text in my_list:
            return True
    return False


def getout(command: str):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


def test_step1():
    assert checkout(f'cd {PATH_IN}; 7z a {PATH_OUT}/arh1', 'Everything is Ok'), 'test_step1 Fail'


def test_tep2():
    assert checkout(f'cd {PATH_EXIT}; 7z u {PATH_OUT}/arh1', 'Everything is Ok'), 'test_step3 Fail'


def test_tep3():
    res1 = checkout(f'7z l {PATH_OUT}/arh1.7z', 'file1')
    res2 = checkout(f'7z l {PATH_OUT}/arh1.7z', 'file2')
    res3 = checkout(f'7z l {PATH_OUT}/arh1.7z', 'file3')
    assert res1 and res2 and res3, 'test_step4 Fail'


def test_step4():
    res1 = checkout(f'cd {PATH_OUT}; 7z x arh1.7z -o{PATH_EXIT2} -y', 'Everything is Ok')
    res2 = checkout(f'ls {PATH_EXIT2}', 'file1')
    res3 = checkout(f'ls {PATH_EXIT2}', 'file2')
    res4 = checkout(f'ls {PATH_EXIT2}', 'file3')
    assert res1 and res2 and res3 and res4, 'test_step5 FAIL'


def test_step5():
    res1 = checkout(f'cd {PATH_IN}; 7z h file1', 'Everything is Ok')
    hash = getout(f'cd {PATH_IN}; crc32 file1').upper()
    res2 = checkout(f'cd {PATH_IN}; 7z h file1', hash)
    assert res1 and res2, 'test_step8 FAIL'


if __name__ == '__main__':
    pytest.main(['-v'])
