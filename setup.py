from setuptools import setup, find_packages

setup(
    name='django-widgets',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,

    description='An alternative for templatetags.',
    maintainer='Marcin Nowak',
    maintainer_email='marcin.j.nowak@gmail.com',
    url='https://github.com/marcinn/django-widgets',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
    ],
)
