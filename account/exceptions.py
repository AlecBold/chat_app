from django.core.serializers.python import Serializer
from django.utils.encoding import smart_text


class LazyUserEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'username': smart_text(obj.username, strings_only=True)})
        dump_object.update({'email': smart_text(obj.email, strings_only=True)})
        return dump_object
