from py2puml.py2puml import py2puml


def test_puml_creation():
    with open('custom_tests.puml', 'w') as puml_file:
        puml_file.writelines(py2puml('test_domain', 'test_domain'))
