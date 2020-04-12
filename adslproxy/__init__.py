# coding=utf-8

def version():
    """
    get version from version file
    :return:
    """
    from adslproxy import __version__
    return __version__.version()
