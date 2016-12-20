import hashlib


def safe_string_hash(string):
    return hashlib.sha256(string).hexdigest()


class metaobject(object):
    '''drop-in baseclass replacement for :py:class:`object` used in every MetaMeta component available in the :ref:`Public API`.

    All instances and whose type is a metaobject subclass carry a ``__meta__`` read-only property with all collected metadata + original module location, etc
    '''
    # TODO: consider `meta` as opposed to `__meta__`


class Singleton(metaobject):
    """base class for self-transmogrifying singletons with support for
    further subclassing. (its metaclass steals the original "Type" from its module and replaces it with an instance)

    Example:

    ::

      class matching(Singleton):
          def strings(obj):
              return isinstance(obj, basestring)

          def containers(obj):
              return isinstance(obj, (dict, list, tuple))

      items = [
          'foo',
          {"non": "string"},
          ['nonstring'],
          'bar'
      ]

      assert filter(matching.strings, items) == [
          'foo',
          'bar',
      ]

      assert filter(matching.containers, items) == [
          {"non": "string"},
          ['nonstring'],
      ]

    """

    def __hash__(self):
        location = self.__meta__.__type__
        # TODO: __meta__.__parent__ is another __meta__ :)

        return safe_string_hash(location)
