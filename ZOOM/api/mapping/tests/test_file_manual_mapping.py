from django.test import TestCase
from unittest import skip
import json
from django.test import RequestFactory, Client
from rest_framework.test import APIClient
from geodata.importer.country import CountryImport
from indicator.models import MAPPING_DICT

class FileManualMappingTestCase(TestCase):
    request_dummy = RequestFactory().get('/')
    c = APIClient()

    def test_file_manual_mapping(self):

        #Intialise countries
        ci = CountryImport()
        ci.update_polygon()
        ci.update_alt_name()

        '''
        Test 0: Upload file
        '''

        res = self.c.post(
            '/api/metadata/sources/?format=json',
            {
                'name': 'The one',
            })

        self.assertEquals(res.status_code, 201, res.json())
        self.assertIsNotNone(res.json()['id'])
        id = res.json()['id']

        '''
        Test 1: Upload file
        '''

        with open('samples/AIDSinfotest.csv') as fp:
                res = self.c.post(
                        '/api/metadata/?format=json',
                        {
                        'file': fp,
                        'description': 'temp description',
                        'title': 'AIDSinfotest.csv',
                        'contains_subnational_data': True,
                        'organisation': 'ZZ',
                        'maintainer': 'kieran',
                        'date_of_dataset': '2009-08-06',
                        'methodology': 'Testing',
                        'define_methodology': 'Really tesring',
                        'update_frequency': 'All the time',
                        'comments': 'Good stuff',
                        'accessibility': 'p',
                        'data_quality': 'good',
                        'number_of_rows': 200,
                        'file_types': 'csv',
                        'location': 1,
                        'source': id,
                        })

        self.assertEquals(res.status_code, 201, res.json())
        self.assertIsNotNone(res.json()['id'])


        '''
        Test 2: Validate
        '''
        res_file_validate = self.c.post(
            '/api/validate/?format=json',
            {
            'id': res.json()['id'],
            }, format='json'
            )
        
        # print res_file_validate.json()['found_list']

        self.assertEquals(res_file_validate.status_code, 200, res_file_validate.json())
        self.assertIsNotNone(res_file_validate.json()['found_list'])
        self.assertIsNotNone(res_file_validate.json()['missing_list'])
        self.assertIsNotNone(res_file_validate.json()['summary'])

        '''
        Test 3: File Manual Mapping
        '''
        MAPPING_DICT['metadata_id'] = res.json()['id']
        MAPPING_DICT['mapping_dict']['geolocation'] = ['Area']
        MAPPING_DICT['mapping_dict']['value'] = ['Data Value']
        MAPPING_DICT['mapping_dict']['value_format'] = ['Unit']
        MAPPING_DICT['mapping_dict']['indicator'] = ['Indicator']
        MAPPING_DICT['mapping_dict']['date'] = ['Time Period']
        MAPPING_DICT['mapping_dict']['comment'] = ['Source']
        MAPPING_DICT['mapping_dict']['filters'] = ['Subgroup']
        MAPPING_DICT.pop('extra_information', None)

        MAPPING_DICT['filter_headings'] = {'Subgroup': 'Subgroup'}
        print(MAPPING_DICT)

        # **manual_mapping_data,
        res_file_manual_mapping = self.c.post(
            '/api/mapping/?format=json',
            MAPPING_DICT,
            format='json'
            )
        
        self.assertEquals(res_file_manual_mapping.status_code, 200, res_file_manual_mapping.json())
        self.assertEquals(res_file_manual_mapping.json()['success'], 1)
