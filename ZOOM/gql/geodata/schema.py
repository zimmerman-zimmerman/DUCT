import graphene
from django_filters import CharFilter, FilterSet, NumberFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from geodata.models import (City, Country, Geolocation, PointBased, Province,
                            Region, SubNational)


class CountryNode(DjangoObjectType):
    entry_id = graphene.String()
    polygons = graphene.JSONString()
    center_longlat = graphene.JSONString()

    class Meta:
        model = Country
        only_fields = (
            'iso2', 'iso3', 'name'
        )
        interfaces = (relay.Node, )

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_polygons(self, context, **kwargs):
        return self.polygons.json if self.polygons else None

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None


class CountryFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = Country
        fields = {
            'iso2': ['exact', 'icontains', 'istartswith', 'in'],
            'iso3': ['exact', 'icontains', 'istartswith', 'in'],
            'name': ['exact', 'icontains', 'istartswith', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class RegionNode(DjangoObjectType):
    entry_id = graphene.String()
    polygons = graphene.JSONString()
    center_longlat = graphene.JSONString()
    country = graphene.List(CountryNode)

    class Meta:
        model = Region
        only_fields = (
            'name', 'code'
        )
        interfaces = (relay.Node, )

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_polygons(self, context, **kwargs):
        return self.polygons.json if self.polygons else None

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None

    def resolve_country(self, context, **kwargs):
        return Country.objects.filter(region__pk=self.id)


class RegionFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = Region
        fields = {
            'name': ['exact', 'icontains', 'istartswith', 'in'],
            'code': ['exact', 'icontains', 'istartswith', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class SubNationalNode(DjangoObjectType):
    entry_id = graphene.String()
    polygons = graphene.JSONString()
    center_longlat = graphene.JSONString()

    class Meta:
        model = SubNational
        exclude_fields = ('polygons', 'center_longlat')
        interfaces = (relay.Node, )

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_polygons(self, context, **kwargs):
        return self.polygons.json if self.polygons else None

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None


class SubNationalFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = SubNational
        fields = {
            'name': ['exact', 'icontains', 'istartswith', 'in'],
            'iso_3166_2': ['exact', 'icontains', 'istartswith', 'in'],
            'code_local': ['exact', 'icontains', 'istartswith', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class CityNode(DjangoObjectType):
    entry_id = graphene.String()
    center_longlat = graphene.JSONString()

    class Meta:
        model = City
        exclude_fields = ('center_longlat', 'polygons', )
        interfaces = (relay.Node, )

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None


class CityFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = City
        fields = {
            'name': ['exact', 'icontains', 'istartswith', 'in'],
            'language': ['exact', 'icontains', 'istartswith', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class PointBasedNode(DjangoObjectType):
    center_longlat = graphene.JSONString()

    class Meta:
        model = PointBased
        only_fields = (
            'id', 'name', 'type', 'subnational', 'comment', 'data_source'
        )
        interfaces = (relay.Node, )

    def resolve_geolocation(self, context, **kwargs):
        return self.geolocation.all()

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None


class PointBasedFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = PointBased
        fields = {
            'type': ['exact', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class GeolocationNode(DjangoObjectType):
    entry_id = graphene.String()
    country = graphene.Field(CountryNode)
    region = graphene.Field(RegionNode)
    sub_national = graphene.Field(SubNationalNode)
    city = graphene.Field(CityNode)
    point_based = graphene.Field(PointBasedNode)
    center_longlat = graphene.JSONString()
    polygons = graphene.JSONString()

    class Meta:
        model = Geolocation
        exclude_fields = (
            'center_longlat', 'polygons'
        )
        interfaces = (relay.Node,)

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_country(self, context, **kwargs):
        return Country.objects.get(id=self.object_id) \
            if self.type == 'country' else None

    def resolve_region(self, context, **kwargs):
        return Region.objects.get(id=self.object_id) \
            if self.type == 'region' else None

    def resolve_sub_national(self, context, **kwargs):
        return SubNational.objects.get(id=self.object_id) \
            if self.type == 'subnational' else None

    def resolve_city(self, context, **kwargs):
        return City.objects.get(id=self.object_id) \
            if self.type == 'city' else None

    def resolve_point_based(self, context, **kwargs):
        return PointBased.objects.get(id=self.object_id) \
            if self.type == 'pointbased' else None

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json \
            if self.center_longlat else None

    def resolve_polygons(self, context, **kwargs):
        return self.polygons.json \
            if self.polygons else None


class GeolocatioFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')
    object_id__in = CharFilter(method='filter_object_id__in')

    class Meta:
        model = Geolocation
        fields = {
            'tag': ['exact', 'icontains', 'istartswith','in'],
            'object_id': ['exact'],
            'type': ['exact', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})

    def filter_object_id__in(self,queryset,name,value):
        name = 'object_id__in'
        return queryset.filter(**{name:eval(value)})


class ProvinceNode(DjangoObjectType):
    entry_id = graphene.String()
    polygons = graphene.JSONString()
    center_longlat = graphene.JSONString()

    class Meta:
        model = Province
        only_fields = (
            'name'
        )
        interfaces = (relay.Node, )

    def resolve_entry_id(self, context, **kwargs):
        return self.id

    def resolve_polygons(self, context, **kwargs):
        return self.polygons.json if self.polygons else None

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json if self.center_longlat else None


class ProvinceFilter(FilterSet):
    entry_id = NumberFilter(method='filter_entry_id')
    entry_id__in = CharFilter(method='filter_entry_id__in')

    class Meta:
        model = Province
        fields = {
            'name': ['exact', 'icontains', 'istartswith', 'in'],
        }

    def filter_entry_id(self, queryset, name, value):
        name = 'id'
        return queryset.filter(**{name: value})

    def filter_entry_id__in(self, queryset, name, value):
        name = 'id__in'
        return queryset.filter(**{name: eval(value)})


class Query(object):
    country = relay.Node.Field(CountryNode)
    all_countries = DjangoFilterConnectionField(
        CountryNode, filterset_class=CountryFilter
    )

    geolocation = relay.Node.Field(GeolocationNode)
    all_geolocations = DjangoFilterConnectionField(
        GeolocationNode, filterset_class=GeolocatioFilter
    )

    point_based = relay.Node.Field(PointBasedNode)
    all_point_based = DjangoFilterConnectionField(
        PointBasedNode, filterset_class=PointBasedFilter
    )

    region = relay.Node.Field(RegionNode)
    all_regions = DjangoFilterConnectionField(
         RegionNode, filterset_class=RegionFilter)

    province = relay.Node.Field(ProvinceNode)
    all_provinces = DjangoFilterConnectionField(
        ProvinceNode, filterset_class=ProvinceFilter)
