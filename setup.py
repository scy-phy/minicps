try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': """MiniCPS is a lightweight simulator for accurate network
    traffic in an industrial control system, with basic support for physical
    layer interaction.""",

    'author': 'Daniele Antonioli',

    'url': 'https://github.com/scy-phy/minicps',

    'download_url': 'https://github.com/scy-phy/minicps',

    'author email': 'daniele_antonioli@sutd.edu.sg',

    'version': '1.1.0',

    'install_requires': [
        'cryptography',
        'pyasn1',
        'pymodbus',
        'cpppo',
    ],

    'package': ['minicps'],
    'scripts': [],
    'name': 'minicps'
}


setup(**config)
