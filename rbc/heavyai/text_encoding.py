'''HeavyDB Bytes type that corresponds to HeavyDB type TEXT ENCODED NONE.
'''

__all__ = ['HeavyDBTextEncodingDictType', 'TextEncodingDict']

from .metatype import HeavyDBMetaType
from rbc import typesystem


class HeavyDBTextEncodingDictType(typesystem.Type):
    """HeavyDB Text Encoding Dict type for RBC typesystem.
    """

    @property
    def __typesystem_type__(self):
        return typesystem.Type('int32')


class TextEncodingDict(object, metaclass=HeavyDBMetaType):
    pass
