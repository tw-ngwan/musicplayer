from setuptools import setup

setup(
    name='musicplayer',
    version='1.1',
    packages=['pip', 'certifi', 'setuptools', 'attrs', 'pytube',
              'Pillow', 'tqdm', 'decorator', 'idna', 'requests',
              'imageio', 'pycparser', 'sortedcontainers', 'pygame',
              'charset-normalizer', 'numpy', 'cffi', 'async-generator',
              'PySocks', 'sniffio', 'outcome', 'wsproto', 'et-xmlfile',
              'moviepy', 'exceptiongroup', 'wheel', 'trio', 'h11',
              'trio-websocket', 'mttkinter', 'imageio-ffmpeg', 'colorama',
              'PyInputPlus', 'PySimpleValidate', 'proglog', 'stdiomask'],
    install_requires=[
        'pytube>=12.1.0',
        'Pillow>=9.2.0',
        'pygame>=2.1.2',
        'moviepy>=1.0.3',
        'mttkinter>=0.6.1',
        'imageio-ffmpeg>=0.4.7'
        'PyInputPlus>=0.2.12'
    ],
    url='https://github.com/tw-ngwan/musicplayer',
    license='',
    author='tw-ngwan',
    author_email='tengwei.ngwan@gmail.com',
    description='Desktop music player that implements multithreading'
)
