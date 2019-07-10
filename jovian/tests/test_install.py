import unittest
# import yaml
from jovian.utils.envfile import (check_error, extract_env_name,
                                  extract_pkg, get_environment_dict, identify_env_file)

FILES_PREFIX = 'jovian/tests/resources/'     # change based on which dir you're running the tests in
# eg: for running only this file, change FILES_PREFIX = 'resources/'


class InstallUtilsTest(unittest.TestCase):

    def test_identify_env_file(self):
        env_fname = identify_env_file(env_fname=None)
        self.assertEqual(env_fname, 'environment.yml')

    def test_get_environment_dict(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        expected = {'prefix': '/home/admin/anaconda3/envs/test-env', 'dependencies':
            ['six=1.11.0', 'sqlite'], 'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname=env_filename)

        self.assertDictEqual(environment, expected)

        with self.assertRaises(FileNotFoundError):
            get_environment_dict(env_fname='non-existent-file.yml')

        # with self.assertRaises(yaml.YAMLError):    # we're printing the exception, not raising it.
        #     get_environment_dict(env_fname=FILES_PREFIX + 'invalid-yaml-file.yml')

    def test_extract_env_name(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        name = extract_env_name(env_fname=env_filename)
        name2 = extract_env_name(env_fname=FILES_PREFIX+'empty-yaml-file.yml')

        self.assertEqual(name, 'test-env')
        self.assertIsNone(name2)
        with self.assertRaises(FileNotFoundError):    # we're printing error, not raising it.
            extract_env_name(env_fname='non-existent-file.yml')

    def test_check_notfound(self):
        error_str = '''ResolvePackageNotFound: 
                        - sixx=1.11.0'''
        error_str2 = '''UnsatisfiableError: 
                                - six=1.91.0'''
        error_str3 = '''AnyOtherException: 
                                - six=1.91.0'''
        error, pkgs = check_error(error_str)
        error2, pkgs2 = check_error(error_str2)
        error3, pkgs3 = check_error(error_str3)

        self.assertEqual(error, 'unresolved')
        self.assertListEqual(pkgs, ['sixx=1.11.0'])
        self.assertEqual(error2, 'unsatisfiable')
        self.assertListEqual(pkgs2, ['six=1.91.0'])
        self.assertIsNone(error3)
        self.assertListEqual(pkgs3, [])

    def test_extract_pkg(self):
        lines = [['- six=1.11.0', 'six=1.11.0'], ['sqlite', None], ['', None], ['- six=1.11.0',
                                                                                'six=1.11.0']]
        for line in lines:
            self.assertEqual(extract_pkg(line=line[0]), line[1])


if __name__ == '__main__':
    unittest.main()
