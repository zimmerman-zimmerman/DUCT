import ujson
from geodata.importer.common import get_json_data
from django.contrib.gis.geos import fromstr

from geodata.models import Country, CountryAltName
from geodata.models import Region


class CountryImport():
    """
    Wrapper class for all import methods used on the Country model
    """
    def __init__(self):
        self.get_json_data = get_json_data

    #make sure update_polygon done first
    def update_alt_name(self):
        admin_countries = self.get_json_data("/../data_backup/alternative_names.json")
        for k in admin_countries:#.get('features'):
            country_iso2 = k.get('iso2')#k.get('properties').get('alpha-2')
            name = k.get('name')#k.get('properties').get('name')
            c = Country(code=country_iso2)
            CountryAltName(name=name, country=c).save()

    def update_polygon(self):
        admin_countries = self.get_json_data("/../data_backup/allcountrycodes.json")
        #admin_countries = self.get_json_data("/../data_backup/country_data.json")

        for k in admin_countries:#.get('features'):
            country_iso2 = k.get('alpha-2')#k.get('properties').get('alpha-2')
            name = k.get('name')#k.get('properties').get('name')
            country_iso3 = k.get('alpha-3')#k.get('alpha-3')
            #country_iso2 = k.get('properties').get('iso2')
            #name = k.get('properties').get('name')
            #country_iso3 = k.get('id')
            if not country_iso2:
                continue
            Country(code=country_iso2, iso3=country_iso3, name=name).save()
            #the_country = Country.objects.get(code=country_iso2)
            #the_country.polygon = ujson.dumps(k.get('geometry'))

    def update_country_center(self):
        country_centers = self.get_json_data("/../data_backup/country_center.json")

        for c in country_centers:
            if Country.objects.filter(code=c).exists():
                current_country = Country.objects.get(code=c)

                point_loc_str = ''.join([
                    'POINT(',
                    str(country_centers[c]["longitude"]),
                    ' ',
                    str(country_centers[c]["latitude"]),
                    ')'])
                longlat = fromstr(point_loc_str, srid=4326)
                current_country.center_longlat = longlat
                current_country.save()

    def update_regions(self):
        country_regions = self.get_json_data("/../data_backup/country_regions.json")

        for cr in country_regions:
            country_iso2 = cr['iso2']
            region_dac_code = cr['dac_region_code']

            if Country.objects.filter(code=country_iso2).exists():
                the_country = Country.objects.get(code=country_iso2)

            if Region.objects.filter(code=region_dac_code).exists():
                the_region = Region.objects.get(code=region_dac_code)

            if the_country.region is None and the_country is not None and the_region is not None:
                the_country.region = the_region
                the_country.save()

