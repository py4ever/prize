import os
from distutils.core import setup
from setuptools import find_packages

from prize.setting import VERSION

README_RST = os.path.join(os.getcwd(), "README.rst")
with open(README_RST, 'r') as rfile:
    LONG_DESCRIPTION = rfile.read()

setup(name='prize',  ## 包名
      version=VERSION,  ## 版本号
      keywords=("prize", "choujiang",  "levin", "leixuewei"),
      description='A tool to pickup winner randomly from inputs', ##项目描述信息
      long_description=LONG_DESCRIPTION,
      author='levin', ##作者
      author_email='levinmhliu@gmail.com',
      url='https://blog.csdn.net/geeklevin', ##这个库的介绍链接，也可以库的开发者网站
      install_requires=["renxianqi","ttkbootstrap"],
      license='Apache License 2.0', ##许可证类型
      packages=find_packages(),
      platforms=["all"],
      entry_points={
          'console_scripts': [
              'prize = prize.main:main',
              'choujiang = prize.main:main',
          ]
      },
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )