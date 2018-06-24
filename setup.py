from setuptools import setup

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(name='apispec-decorated-crawler',
        version='1.0.0',
        license='MIT',
        description='Plugin for apispec which helps reusing the documentation by using a decorated function stack.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Brunoais',
        author_email='brunoaiss@gmail.com',
        url='https://github.com/brunoais/apispec-decorated-crawler',
        install_requires=['apispec'],
        py_modules=['brunoais.apispec.ext.decorated_crawler'],
        classifiers=(
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
      )
