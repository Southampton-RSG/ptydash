import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='PtyDash',
    version='0.0.1.dev1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Southampton-RSG/ptydash',
    author='James Graham',
    author_email='J.Graham@soton.ac.uk',
    license='GPLv2',
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Monitoring',
        'Development Status :: 2 - Pre-Alpha'
    ),
    packages=setuptools.find_packages(
        exclude=['docs', 'tests', 'env*']
    ),
    package_data={
        'ptydash': [
            'templates/*.html',
            'templates/modules/*.html',
            'static/img/logo_100px.png'
        ]
    },
    install_requires=[
        'matplotlib',
        'numpy',
        'six',
        'tornado'
    ],
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'ptydash = ptydash.server:main',
        ]
    }
)
