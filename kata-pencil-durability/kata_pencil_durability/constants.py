__author__ = 'Dhanu'

import logging

log = logging.getLogger(__name__)


class _constants:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError(f'Can\'t rebind const(%s)' % name)
        self.__dict__[name] = value


import sys

sys.modules[__name__] = _constants()

from . import constants

constants.space_char = ' '
constants.collision_char = '@'
constants.two = 2
constants.one = 1
constants.zero = 0
constants.last_erased = -1


