"""
Utilities useful during the build.
"""
# author: Loic Esteve
# license: BSD
import os

from distutils.version import LooseVersion

DEFAULT_ROOT = 'sklearn'
CYTHON_MIN_VERSION = '0.23'

try:
    from sklearn._build_utils import maybe_cythonize_extensions
except ImportError:
    # maybe_cythonize_extensions exists from scikit-learn 0.18.1 onwards
    def build_from_c_and_cpp_files(extensions):
        """Modify the extensions to build from the .c and .cpp files.

        This is useful for releases, this way cython is not required to
        run python setup.py install.
        """
        for extension in extensions:
            sources = []
            for sfile in extension.sources:
                path, ext = os.path.splitext(sfile)
                if ext in ('.pyx', '.py'):
                    if extension.language == 'c++':
                        ext = '.cpp'
                    else:
                        ext = '.c'
                    sfile = path + ext
                sources.append(sfile)
            extension.sources = sources


    def maybe_cythonize_extensions(top_path, config):
        """Tweaks for building extensions between release and development mode."""
        is_release = os.path.exists(os.path.join(top_path, 'PKG-INFO'))

        if is_release:
            build_from_c_and_cpp_files(config.ext_modules)
        else:
            message = ('Please install cython with a version >= {0} in order '
                       'to build a scikit-learn development version.').format(
                           CYTHON_MIN_VERSION)
            try:
                import Cython
                if LooseVersion(Cython.__version__) < CYTHON_MIN_VERSION:
                    message += ' Your version of Cython was {0}.'.format(
                        Cython.__version__)
                    raise ValueError(message)
                from Cython.Build import cythonize
            except ImportError as exc:
                exc.args += (message,)
                raise

            config.ext_modules = cythonize(config.ext_modules)

