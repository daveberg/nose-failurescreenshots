from setuptools import setup

requires = [
    'nose',
    'selenium'
]


setup(
    name='nose_webdriverfailuress',
    version='0.14',
    author='Dave',
    author_email='david.bisset@fanduel.com',
    description='capture screenshot on test failure or error',
    py_modules=['nose_webdriverfailuress'],
    include_package_data=True,
    entry_points={
        'nose.plugins.0.10': [
            'nose_webdriverfailuress = nose_webdriverfailuress:FailureScreenshots'
        ]
    },
    install_requires=requires
)
