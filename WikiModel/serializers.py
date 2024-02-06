from rest_framework import serializers
from WikiModel.models import WikiNamespaces, Page, Contributor


class WikiNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikiNamespaces
        fields = ('key',
                  'case',
                  'text')


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id',
                  'title',
                  'ns',
                  'redirect_title')


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id',
                  'user_name',
                  'user_ip')
