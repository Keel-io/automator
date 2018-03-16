import setuptools
from automator.version import Version


setuptools.setup(name='automator',
                 version=Version('0.2.0').number,
                 description='Data cleaning made easy',
                 long_description=open('README.md').read().strip(),
                 author='Keel',
                 author_email='support@keel.io',
                 url='url='https://github.com/keel-io/automator',
                 py_modules=['automator'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='sql, data science, data cleaning',
                 classifiers=['Data cleaning', 'Sql'])
