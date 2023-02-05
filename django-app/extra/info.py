__author__         =      "Rocuant Roberto"
__created__        =      "02/03/2022"          # MM/DD/YYYY
__credits__        =      ""
__copyright__      =      "Copyright 2023"
__email__          =      "roberto.rocuantv@gmail.com"
__maintainer__     =      "Rocuant Roberto"
__license__        =      "GPL v3.0"
__prod__           =      ""
__disclaimer__     =      ""
__version__        =      "0.1.0"
__logs__           =      {
    'date':         "02/04/2023",
    'info':         ["Connection with API Riot ready.", "Get info from Riot."],
    'problems':     [""],
    'fixed':        None,
    'commit':       "",
}

info = {
    '__author__': __author__,
    '__created__': __created__,
    '__credits__': __credits__,
    '__copyright__': __copyright__,
    '__email__': __email__,
    '__license__': __license__,
    '__logs__': __logs__,
    '__maintainer__': __maintainer__,
    '__prod__': __prod__,
    '__version__': __version__, 
}

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

info = dotdict(dict=info)['dict']