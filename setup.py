from setuptools import setup, find_packages
import os

version = '1.2dev'

setup(name='osha.dynamicpressroom',
      version=version,
      description="Turns PressRoom objects into Dynamic Pressrooms!",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        ],
      keywords='pressroom plone syslab',
      author='Syslab.com, GmbH',
      author_email='info@syslab.com',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL + EUPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'mock',
          ],
      },
      paster_plugins=["ZopeSkel"],
      )
