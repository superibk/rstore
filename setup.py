from setuptools import setup

setup(
    name='rstore',
    version='0.1.0',
    packages=['rstore'],
    install_requires=[
        'prettytable~=2.0.0',
        'requests~=2.24.0',
    ],
    description="tool that communicates with the public Reddit API, can tell which posts are new, which posts have dropped off, and which had vote changes.",
    entry_points={
        'console_scripts': [
            'rstore = rstore.__main__:main'
        ]
    })
