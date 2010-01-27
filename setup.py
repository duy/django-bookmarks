from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-bookmarks',
    version=__import__('bookmarks').__version__,
    description='A reusable Django app for bookmark management.',
    author='James Tauber',
    author_email='jtauber@jtauber.com',
    url='http://code.google.com/p/django-bookmarks/',
    packages=[
        'bookmarks',
    ],
#    package_dir={'bookmarks': 'bookmarks'},
#
#    package_data = {
#        'bookmarks': [
#            'templates/bookmarks/*.html'
#            'templates/feeds/*.html'
#        ],
#    },

#    packages=find_packages(),
#    package_data = {
#        'bookmarks': [
#            'templates/bookmarks/*.html',
#            'templates/feeds/*.html'
#        ],
#    },
#    include_package_data=True,
#    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
