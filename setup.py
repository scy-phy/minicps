try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': """MiniCPS is a lightweight simulator for accurate network
    traffic in an industrial control system, with basic support for physical
    layer interaction.""",

    'author': 'scy-phy',

    'url': 'https://github.com/scy-phy/minicps',

    'download_url': 'https://github.com/scy-phy/minicps',

    'author email': 'abc@gmail.com',

    'version': '0.1.0',

    'install_requires': [
        'cpppo',
        'networkx',
        'matplotlib',
        'nose',
        'nose-cover3',
    ],

    'package': ['minicps'],
    'scripts': [],
    'name': 'minicps'
}


setup(**config)
