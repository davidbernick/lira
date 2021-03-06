from setuptools import setup


setup(
    name='green-box-tools',
    version='1.0.0.dev1',
    description='Utility for listener components of Green-Box of HCA-DCP',
    url='https://github.com/HumanCellAtlas/secondary-analysis',
    author='Rex Wang',
    author_email='chengche@broadinstitute.org',
    license='BSD 3-clause "New" or "Revised" License',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['green_box_utils', 'tests'],

    # Required packages
    install_requires=['Flask>=0.12.2',
                      'connexion>=1.1.15',
                      'requests>=2.18.4',
                      'google-auth',
                      'google-cloud-storage',
                      'requests-mock',
                      'mock'],
)
