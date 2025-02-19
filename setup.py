from setuptools import setup

setup(
    name='pysyun_etherscan_transactions_source',
    version='1.0',
    author='Illiatea',
    author_email='illiatea2@gmail.com',
    py_modules=['etherscan_transaction'],
    install_requires=['requests', 'eth_abi', 'eth_utils']
)
