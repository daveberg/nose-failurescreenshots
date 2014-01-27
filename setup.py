from setuptools import setup

requires = [
    'nose',
    'selenium'
]


setup(
    name='nosetest webdriver failure screen shots',
    version='0.13',
    author='Dave',
    author_email='david.bisset@fanduel.com',
    description='capture screenshot on test failure or error',
    py_modules=['failurescreenshots'],
    include_package_data=True,
    entry_points={
        'nose.plugins.0.10': [
            'failurescreenshots = failurescreenshots:FailureScreenshots'
        ]
    },
    install_requires=requires
)
