from rest_framework import mixins, viewsets


class ListRetrieveMixin(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass
