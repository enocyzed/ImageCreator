
# When the package is a pip package, this can be removed
import sys
import os
import pathlib
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
sys.path.append(dname)
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
#

from ImageCreator.core.use import create, create_on_press, create_on_modified, create_template


def create_from_params(params_path, save_path=None, save_name=None):
    return create(params_path, save_path, save_name)
