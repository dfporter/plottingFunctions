import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='plottingFunctions',
    version='0.0.1',
    author='Douglas F Porter',
    author_email='dfporter@gmail.com',
    description='Various plotting functions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dfporter/plottingFunctions',
    project_urls = {
        "Bug Tracker": "https://github.com/dfporter/plottingFunctions/issues"
    },
    license='MIT',
    packages=['toolbox'],
    install_requires=['numpy', 'sklearn', 'scipy', 'pandas'],
)