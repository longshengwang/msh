from setuptools import setup, find_packages

# files = ["src/*"]


setup(
      name="msh",
      version="1.2",
      keywords='mac ssh',
      description="mac ssh client(linux can also use)",
      author="wls",
      author_email="wanglongshengdf@gmail.com",
      url="https://github.com/mswang66/msh",
      license="GNU",
      python_requires='==2.7.*',
      install_requires=['pexpect','ipaddress'],
      packages=find_packages(),
      scripts=["scripts/msh"],
      )
