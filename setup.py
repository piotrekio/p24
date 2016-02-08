from distutils.core import setup


setup(
    name = 'p24',
    version = '0.1',
    description = 'Set of tools for utilizing Przelewy24 API',
    author = 'Piotr Wasilewski',
    author_email = 'piotrek@piotrek.io',
    url = 'https://github.com/piotrekio/p24',
    py_modules = ['p24'],
    install_requires = ['requests==2.9.1']
)
