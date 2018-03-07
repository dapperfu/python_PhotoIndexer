from setuptools import setup
import versioneer

setup(name="ffinfo",
      version=__VERSION__,
      description="View technical information and metadata of video files",
      url='https://github.com/jed-frey/ffinfo',
      author='Jed Frey',
      author_email='jed-frey@users.noreply.github.com',
      license='GPLv3',
      packages=['ffinfo'],
      zip_safe=False,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
)
