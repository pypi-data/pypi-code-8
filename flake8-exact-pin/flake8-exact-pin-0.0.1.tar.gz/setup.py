from setuptools import setup


def get_version(fname='flake8_exact_pin.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='flake8-exact-pin',
    description='A flake8 extension that checks for '
                'exact pins (e.q.: `foo==1.5.6`) in setup.py',
    long_description=get_long_description(),
    keywords='flake8 setup.py pin dependencies',
    version=get_version(),
    author='Marc Abramowitz',
    author_email='msabramo@gmail.com',
    install_requires=['setuptools'],
    entry_points={
        'flake8.extension': [
            'flake8_exact_pin = flake8_exact_pin:ExactPinChecker'
        ],
    },
    url='https://github.com/msabramo/flake8-exact-pin',
    license='MIT',
    py_modules=['flake8_exact_pin'],
    zip_safe=False,
)
