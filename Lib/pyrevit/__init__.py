import os
import os.path as op

# noinspection PyUnresolvedReferences
from System.Diagnostics import Process

# ----------------------------------------------------------------------------------------------------------------------
# testing for availability of __revit__ just in case and collect host information
# ----------------------------------------------------------------------------------------------------------------------

# define HOST_SOFTWARE
try:
    # noinspection PyUnresolvedReferences
    HOST_SOFTWARE = __revit__
except Exception:
    raise Exception('Critical Error. Host software handle is not available (__revit__)')


class _HostVersion:
    """Contains current host version and provides comparison functions."""
    def __init__(self, *args):
        if args:
            self.version = str(args[0])     # type: str
        else:
            self.version = HOST_SOFTWARE.Application.VersionNumber      # type: str

        self.proc_id = Process.GetCurrentProcess().Id

    def is_newer_than(self, version):
        return int(self.version) > int(version)

    def is_older_than(self, version):
        return int(self.version) < int(version)


def _get_username():
    """Return the username from Revit API (Application.Username)"""
    uname = HOST_SOFTWARE.Application.Username
    uname = uname.split('@')[0]  # if username is email
    uname = uname.replace('.', '')  # removing dots since username will be used in file naming
    return uname


HOST_VERSION = _HostVersion()
HOST_USERNAME = _get_username()

HOST_ADSK_PROCESS_NAME = Process.GetCurrentProcess().ProcessName


# ----------------------------------------------------------------------------------------------------------------------
# Testing the value of __forceddebugmode__ (set in builtins scope by C# Script Executor)
# ----------------------------------------------------------------------------------------------------------------------
class _ExecutorParams(object):
    @property   # read-only
    def forced_debug_mode(self):
        # noinspection PyUnresolvedReferences
        return __forceddebugmode__

    @property   # read-only
    def window_handle(self):
        # noinspection PyUnresolvedReferences
        return __window__

    @property   # writeabe
    def command_name(self):
        # noinspection PyUnresolvedReferences
        return __commandname__

    @command_name.setter
    def command_name(self, value):
        # noinspection PyUnusedLocal
        __commandname__ = value


EXEC_PARAMS = _ExecutorParams()


# ----------------------------------------------------------------------------------------------------------------------
# environment info
# ----------------------------------------------------------------------------------------------------------------------
def _find_home_directory():
    """Return the pyRevitLoader.py full directory address"""
    try:
        return op.dirname(op.dirname(op.dirname(op.dirname(__file__))))   # 4 steps back for <home>/Lib/pyrevit/config
    except NameError:
        raise Exception('Critical Error. Can not find home directory.')


# main pyrevit repo folder
HOME_DIR = _find_home_directory()

# main pyrevit lib folder
MAIN_LIB_DIR = op.join(HOME_DIR, 'lib')

# default extension extensions folder
EXTENSIONS_DEFAULT_DIR = op.join(HOME_DIR, 'extensions')


PYREVIT_ADDON_NAME = 'pyrevit'
_VERSION_MAJOR = 4
_VERSION_MINOR = 0


# user env paths
USER_ROAMING_DIR = os.getenv('appdata')
USER_SYS_TEMP = os.getenv('temp')
