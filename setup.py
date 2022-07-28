from setuptools import find_packages, setup

setup(
    name='eth-portfolio',
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    description='eth-portfolio makes it easy to analyze your portfolio.',
    author='BobTheBuidler',
    author_email='bobthebuidlerdefi@gmail.com',
    url='https://github.com/BobTheBuidler/eth-portfolio',
    install_requires=[
        "pandas>=1.4.3,<1.5",
        "ypricemagic>=1.1.1.dev67,<1.1.3",
    ],
    setup_requires=[
        'setuptools_scm',
    ],
)