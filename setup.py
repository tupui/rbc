import os
import sys
import builtins

if sys.version_info[:2] < (3, 4):
    raise RuntimeError("Python version >= 3.4 required.")

builtins.__RBC_SETUP__ = True

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

DESCRIPTION = "RBC - Remote Backend Compiler"
LONG_DESCRIPTION = """
The aim of the Remote Backend Compiler project is to distribute the
tasks of a program JIT compilation process to separate computer
systems using the client-server model. The frontend of the compiler
runs on the client computer and the backend runs on the server
computer. The compiler frontend will send the program code to compiler
backend in IR form where it will be compiled to machine code.
"""

def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    metadata = dict(
        name='rbc',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='BSD',
        version='0.1.0.dev1',
        author='Pearu Peterson',
        maintainer='Pearu Peterson',
        author_email='pearu.peterson@quansight.com',
        url='https://github.com/plures/rbc',
        platforms='Cross Platform',
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            "Operating System :: OS Independent",
            "Topic :: Software Development",
        ],
        install_requires=[
            "numba",
            "llvmlite",
        ],
        packages=['rbc'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
    )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return


if __name__ == '__main__':
    setup_package()
    del builtins.__RBC_SETUP__