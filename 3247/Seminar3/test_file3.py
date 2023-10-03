import yaml
from checks import checkout, getout
import pytest

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        res1 = checkout(f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1',
                        'Everything is Ok')
        res2 = checkout(f'ls {data["PATH_OUT"]}', 'arh1.7z')
        assert res1 and res2, 'test_step1 Fail'

    def test_step2(self, clear_folders, make_files):

        res = []
        res.append(checkout(f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1',
                            'Everything is Ok'))
        res.append(checkout(f'cd {data["PATH_OUT"]}; 7z e arh1.7z -o{data["PATH_EXIT"]}',
                            'Everything is Ok'))
        for item in make_files:
            res.append(checkout(f'ls {data["PATH_EXIT"]}', item))
        assert all(res), 'test_step2 FAIL'

    def test_step3(self):
        assert checkout(f'cd {data["PATH_OUT"]}; 7z t arh1.7z',
                        'Everything is Ok'), 'test_step3 FAIL'

    def test_step4(self):
        assert checkout(f'cd {data["PATH_IN"]}; 7z u {data["PATH_OUT"]}/arh1',
                        'Everything is Ok'), 'test_step3 Fail'

    def test_step5(self, clear_folders, make_folders, make_files):
        res = []
        res.append(checkout(f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1',
                        'Everything is Ok'))
        for item in make_files:
            res.append(checkout(f"cd {data['PATH_OUT']}; 7z l arh1.7z", item))
        assert all(res), 'test_step5 Fail'

    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(checkout(f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1',
                            'Everything is Ok'))
        res.append(checkout(f'cd {data["PATH_OUT"]}; 7z x arh1.7z -o{data["PATH_EXIT2"]} -y',
                            'Everything is Ok'))
        for item in make_files:
            res.append(checkout(f'ls {data["PATH_EXIT2"]}', item))
        res.append(checkout(f'ls {data["PATH_EXIT2"]}', make_subfolder[0]))
        res.append(checkout(f'ls {data["PATH_EXIT2"]}/{make_subfolder[0]}',
                            make_subfolder[1]))
        assert all(res), 'test_step6 FAIL'

    def test_step7(self):
        assert checkout(f'cd {data["PATH_OUT"]}; 7z d arh1.7z',
                        'Everything is Ok'), 'test_step2 Fail'

    def test_step8(self, clear_folders, make_files):
        res = []
        for item in make_files:
            res.append(checkout(f'cd {data["PATH_IN"]}; 7z h {item}',
                                'Everything is Ok'))
            hash = getout(f'cd {data["PATH_IN"]}; crc32 {item}').upper()
            res.append(checkout(f'cd {data["PATH_IN"]}; 7z h {item}', hash))
        assert all(res), 'test_step8 FAIL'


if __name__ == '__main__':
    pytest.main(['-v'])
