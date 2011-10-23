from setuptools import find_packages, setup

setup(
    name = 'CookieRevocation',
    version = '0.1',
    author = 'Jon Cave',
    description = "Trac plugin to enable revocation of a user's trac_auth cookie",
    license = 'BSD',

    packages = find_packages(exclude=['*.tests*']),
    package_data = { 'cookierevocation': ['templates/*.html'] },
    entry_points = {
        'trac.plugins': [
            'cookierevocation = cookierevocation.revoke',
        ],
    },
)
