from django.contrib.gis.db import models as gis_models

class Geolocation(gis_models.Model):
    name = gis_models.CharField(primary_key=True, max_length=200)

class Region(gis_models.Model):
    region_id = gis_models.AutoField(primary_key=True, editable=False)
    name = gis_models.CharField(unique=True, max_length=200)
    code = gis_models.CharField(max_length=100)

    center_longlat = gis_models.PointField(null=True, blank=True)
    polygons = gis_models.MultiPolygonField(null=True, blank=True)

    wikipedia = gis_models.CharField(null=True, blank=True, max_length=150)
    language = gis_models.CharField(max_length=2, null=True)
    data_source = gis_models.CharField(max_length=100, null=True, blank=True)
    objects = gis_models.Manager()

    def __unicode__(self):
        return self.name


class Country(gis_models.Model):
    country_id = gis_models.AutoField(primary_key=True, editable=False)
    name = gis_models.CharField(unique= True, max_length=100, db_index=True)
    iso2 = gis_models.CharField(max_length=2) #iso2
    iso3 = gis_models.CharField(max_length=3, null=True, blank=True)
    numerical_code_un = gis_models.IntegerField(null=True, blank=True)
    dac_country_code = gis_models.IntegerField(null=True, blank=True)

    capital_city = gis_models.OneToOneField("City", related_name='capital_of',  null=True, blank=True, on_delete=gis_models.SET_NULL)
    region = gis_models.ForeignKey(Region, null=True, blank=True, on_delete=gis_models.SET_NULL)
    un_region = gis_models.ForeignKey('Region', null=True, blank=True, related_name='un_countries', on_delete=gis_models.SET_NULL)
    unesco_region = gis_models.ForeignKey('Region', null=True, blank=True, related_name='unesco_countries', on_delete=gis_models.SET_NULL)

    center_longlat = gis_models.PointField(null=True, blank=True)
    polygons = gis_models.MultiPolygonField(null=True, blank=True)

    wikipedia = gis_models.CharField(null=True, blank=True, max_length=150)
    language = gis_models.CharField(max_length=2, null=True)
    data_source = gis_models.CharField(max_length=100, null=True, blank=True)
    objects = gis_models.Manager()

    class Meta:
        verbose_name_plural = "countries"

    def __unicode__(self):
        return self.name


class City(gis_models.Model):
    city_id = gis_models.AutoField(primary_key=True, editable=False)
    name = gis_models.CharField(unique= True, max_length=200)
    ascii_name = gis_models.CharField(max_length=200, null=True, blank=True)
    country = gis_models.ForeignKey(Country, null=True, blank=True, on_delete=gis_models.SET_NULL)

    center_longlat = gis_models.PointField(null=True, blank=True)

    wikipedia = gis_models.CharField(null=True, blank=True, max_length=150)
    language = gis_models.CharField(max_length=2, null=True)
    data_source = gis_models.CharField(max_length=100, null=True, blank=True)
    objects = gis_models.Manager()

    @property
    def is_capital(self):
        return hasattr(self, 'capital_of')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class SubNational(gis_models.Model):
    subnational_id = gis_models.AutoField(primary_key=True, editable=False)
    name = gis_models.CharField(unique=True, max_length=100)
    iso_3166_2 = gis_models.CharField(null=True, blank=True, max_length=2)
    code_local = gis_models.CharField(null=True, blank=True, max_length=100)
    postcode = gis_models.CharField(null=True, blank=True, max_length=100)
    country = gis_models.ForeignKey(Country, null=True, blank=True, on_delete=gis_models.SET_NULL)

    center_longlat = gis_models.PointField(null=True, blank=True)
    polygons = gis_models.MultiPolygonField(null=True, blank=True)

    #area_sqkm = gis_models.CharField(null=True, blank=True, max_length=100)
    wikipedia = gis_models.CharField(null=True, blank=True, max_length=150)
    language = gis_models.CharField(max_length=2, null=True)
    data_source = gis_models.CharField(max_length=100, null=True, blank=True)
    objects = gis_models.Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "admin1 regions"

class PointBased(gis_models.Model):
    pointbased_id = gis_models.AutoField(primary_key=True, editable=False)
    name = gis_models.CharField(max_length=200)
    type = gis_models.CharField(max_length=200, null=True, blank=True) #choices=['hospital', 'encounter', 'general_marker'])

    country = gis_models.ForeignKey(Country, null=True, blank=True, on_delete=gis_models.SET_NULL)
    center_longlat = gis_models.PointField(null=True, blank=True)

    comment = gis_models.TextField()
    data_source = gis_models.CharField(max_length=100, null=True, blank=True)
    objects = gis_models.Manager()

    @property
    def is_capital(self):
        return hasattr(self, 'capital_of')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


