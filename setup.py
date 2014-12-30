from setuptools import setup, find_packages


setup(
    name='django_toolchest',
    version='0.1',
    desription='Tools to aid in django app development.',
    author='Jacob Burbach',
    author_email='jmburbach@gmail.com',
    license='BSD',
    packages=find_packages(exclude=('tests.*', 'tests')),
)
