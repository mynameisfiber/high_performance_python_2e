from distutils.core import setup
import numpy as np

from Cython.Build import cythonize
setup(ext_modules=cythonize("cythonfn.pyx", compiler_directives={"language_level": "3"}),
        include_dirs=[np.get_include()])

