# coding: utf-8

from setuptools import setup
import os

README = os.path.join(os.path.dirname(__file__), 'README.rst')


setup(name='mqtt-sentinel',
      version='0.1',
      description='Integration between MQTT and custom notification services.',
      url='https://github.com/caiovictormc/mqtt-sentinel',
      author='caiovictormc',
      author_email='caiovictormc@gmail.com',
      license='MIT',
      packages=['sentinel'],
      install_requires=[],
      long_description=open(README).read(),
      include_package_data=True,
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: MIT License',
        'Programming Language :: Python :: 3.7',
        'MQTT :: Notification :: Homie',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points={
        'console_scripts': ['msentinel=sentinel.command_line:main']
      },
      zip_safe=False)
