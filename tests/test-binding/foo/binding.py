import collections.abc
import json
import typing


from azure.functions_worker.bindings import meta


class Binding(meta.InConverter, meta.OutConverter,
              binding='foo'):
    pass
