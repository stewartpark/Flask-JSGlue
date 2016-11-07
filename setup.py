"""
Flask-JSGlue
------------

Flask-JSGlue helps hook up your Flask application nicely with the front end.

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Flask-JSGlue',
    version='0.3.1',
    url='http://stewartpark.github.com/Flask-JSGlue',
    license='BSD',
    author='Stewart Park',
    author_email='stewartpark92@gmail.com',
    description='Flask-JSGlue helps hook up your Flask application nicely with the front end.',
    long_description=__doc__,
    py_modules=['flask_jsglue'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
