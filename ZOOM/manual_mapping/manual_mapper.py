from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.db import connection,transaction
from django.conf import settings
from django.http import Http404
import numpy as np
import pandas as pd
import pickle 
import json
import datetime
import time
import os

from dateutil.parser import parse
from indicator.models import *
from geodata.models import Country
from lib.converters import convert_to_JSON
from lib.tools import check_column_data_type, correct_data, convert_df
from lib.common import get_data, get_dtype_data
from file_upload.models import File
from error_correction.error_correction import *


def manual_mapper(data):
    """Perfoms manual mapping process."""
    if 'dict' in data:
        order = {}
        index_order = {}
        bulk_list = []
        file_id = data['file_id']
        mappings = data['dict']
        unit_of_measure_value = mappings.pop("empty_unit_of_measure", None)
        empty_values_array = [mappings.pop("empty_indicator", None), mappings.pop("empty_country", None), mappings.pop("empty_indicator_cat", None),
                                unit_of_measure_value, mappings.pop("empty_date", None)]
        relationship_dict = mappings.pop("relationship", None)
        left_over_dict = mappings.pop("left_over", None)
        df_data = get_data(file_id)
        error_data, dtypes_dict = get_dtype_data(file_id)

        print("Begining Mapping")
        ###If column mapped to multiple sections in data model
        if relationship_dict:
            relationship_dict = clean_data(relationship_dict, "~", " ")
            left_over_dict = clean_data(left_over_dict, "~", " ")
            
        ###Start checking the keys 
        for key in mappings:
            if mappings[key]:#this is included incase no mapping is given
                if len(mappings[key]) > 1:#greated than one for subgroups change for indicator scenario
                    if key == "indicator_category":
                       df_data, mappings, dtypes_dict, tmp_mapping = group_indicator_categories(df_data, mappings, dtypes_dict, relationship_dict,key)
                else:
                    mappings[key][0] = mappings[key][0].replace("~", " ")

        df_data, mappings, dtypes_dict = apply_missing_values(df_data, mappings, dtypes_dict, empty_values_array)

        ###Comvert csv
        if relationship_dict:
            #check if unit of measure exists
            df_data = convert_df(mappings, relationship_dict, left_over_dict, df_data, dtypes_dict, unit_of_measure_value)

        print("Validating data")
        for key in mappings:
            if mappings[key]:
                if key in mappings[key]:
                    mappings[key] = [key]
                if not mappings[key][0] in df_data.columns:
                    mappings[key][0] = mappings[key][0].replace("~", " ")

        
        result, correction_mappings, context = check_mapping_dtypes(mappings, dtypes_dict)
        
        ###Checking if mapping is bad or not
        if not result:
            return context

        error_lines, zip_list, summary_results, summary_indexes, new_dtypes_dict = generate_error_data(df_data)
        save_validation_data(error_lines, file_id, new_dtypes_dict)
        ###Combine dictionaries
        for key in new_dtypes_dict:
            dtypes_dict[key] = new_dtypes_dict[key] 

        df_data = correct_data(df_data, correction_mappings, error_lines)
        null_values = df_data[mappings['indicator_category'][0]].isnull()
        df_data[mappings['indicator_category'][0]][null_values] = "Default"

        #cycle through dataset and save each line
        order['file'] = file 
        order["date_created"] = datetime.datetime.now()
        instance = Time(date_type = "YYYY")
        instance.save()
        order['date_format'] = instance  

        datapoint_headings = []
        for key in mappings:
            if mappings[key]:
                index_order[key] = mappings[key][0]
                datapoint_headings.append(mappings[key][0])
                
        print("Save indicators, sources, categories, countries")
        get_save_unique_datapoints()

                count = 0

        #print("Date Value column")#
        #f= (lambda x: True if len(x) >= 4 else False)
        #print(df_data['Date'][df_data['Date'].apply(f)])

        print("Begining mapping process")
        for count in range(len(df_data)):
            #statement += " ("
            for key in mappings:
                if mappings[key]:
                    if mappings[key][0] in df_data.columns:
                       #print(df_data[mappings[key][0]][count])
                       order[key] = df_data[mappings[key][0]][count]
                    else:
                       #print(df_data[mappings[key][0].replace("~", " ")][count])
                       order[key] = df_data[mappings[key][0].replace("~", " ")][count] # kind of a stupid way to handle this 
                    
            #instance = MeasureValue(value = order['measure_value'], value_type =order['unit_measure'], name="")
            #bulk_measure_value.append(instance)
            #del order['unit_measure'] # temporary fix  
            #add measure unit
            #order['measure_value'] = instance
            #add foreign keys to indicator datapoint model

            if 'indicator_category' in order:
                order['indicator_category'] = ind_cat_dict[order['indicator'] + order['indicator_category']] # why +??
            if 'source' in order:
                order['source'] = ind_source_dict[order['indicator'] + order['source']]
            if 'indicator' in order:
                order['indicator'] = ind_dict[order['indicator']]
            if 'country' in order:
                order['country'] = ind_country_dict[order['country']]
                #bf.d.
            
            #for key in order:
            #   statement += "'%s'," % str((order[key])).decode('utf-8')
            #statement = statement[:-1] + ") " """
            instance = IndicatorDatapoint(**order)
            bulk_list.append(instance)

        IndicatorDatapoint.objects.bulk_create(bulk_list)
        #print("Save successful")
        #os.remove(dict_name)#remove tmp file with datatypes
        #Transgender people: HIV prevalence, 
         #convert_to_JSON("Transgender people: HIV prevalence", "Transgender people: Population size estimate")#allow user to choose these

        #return HttpResponseRedirect('tags/%d'%file_id)
        #return nothing
        context = {"success" : 1}
        #return render(request, 'manual_mapping/manual_mapping.html', context)
        #return HttpResponse(error_message)
        return context
    else :
        context = {"error_messages" : "No data in dictionary sent", "success" : 0}
        return context


def clean_data(data, unwanted_str, replace_str):
    """Begins process for grouping indicator categories together.
    
    Args:
        data ([],{}): data to be cleaned.
        unwanted_str (str): string value to be replaced.
        replace_str (str): string value to be inserted.

    Returns: 
        data ([],{}): returns a cleaned version of the data.
    """
    for i in data:
        value = data.pop(i)
        key = i.replace(unwanted_str, replace_str)
        data[key] = value
    return data

def group_indicator_categories(df_data, mappings, dtypes_dict, relationship_dict, key):
    """Begins process for grouping indicator categories together.
    
    Args:
        df_data (Dataframe): dataframe of CSV file.
        mappings ({str:[str]}): the users chosen mappings for a file column.
        dtypes_dict ({str:str}): stores the data-types found for each heading.
        relationship_dict ({str: [str]}): section of the data model mapped to a file heading.
        key (str): file heading.

    Returns: 
        df_data (Dataframe): dataframe of CSV file.
        mappings ({str:[str]}): the users chosen mappings for a file column.
        dtypes_dict ({str:str}): stores the data-types found for each heading.
        tmp_mappings ([str]): if a file heading is mapped to multiple parts of
                              the data model, create an array of headings for 
                              the relationship creation method.
    """

    #ignore relationship

    df_data["indicator_category"] = ""
    tmp_mappings = ['indicator_category']
    count = 0
    for value in mappings[key]:
        mappings[key][count] = mappings[key][count].replace("~", " ")
        value = value.replace("~", " ")

        #loop through data combine with heading name and itself   
        if not value == 'indicator_category':
            if not relationship_dict:#no relationshup defined
                    df_data["indicator_category"] = df_data["indicator_category"] + "|" + value + ":" + df_data[value].map(str)
            else:
                if not (value in relationship_dict):
                    df_data["indicator_category"] = df_data["indicator_category"] + "|" + value + ":" + df_data[value].map(str)
                else:
                    tmp_mappings.append(value)     
        count += 1
    mappings[key] = tmp_mappings#IF RELATIONSHOip add here????
    dtypes_dict[mappings['indicator_category'][0]] = [('str','str')]

    return df_data, mappings, dtypes_dict, tmp_mappings


def apply_missing_values(df_data, mappings, dtypes_dict, empty_values_array):
    """Appliess missing values to dataframe.
    
    Args:
        df_data (Dataframe): dataframe of CSV file.
        mappings ({str:[str]}): the users chosen mappings for a file column.
        dtypes_dict ({str:str}): stores the data-types found for each heading.
        empty_values_array ([str]): values related to missing values in manual mapping process

    Returns: 
        df_data (Dataframe): dataframe of CSV file.
        mappings ({str:[str]}): the users chosen mappings for a file column.
        dtypes_dict ({str:str}): stores the data-types found for each heading.
    """
    indicator_value, country_value, indicator_category_value, unit_of_measure_value, value_of_date = empty_values_array

    if indicator_value:
        mappings['indicator'] = ['indicator']
        df_data['indicator'] = indicator_value
        dtypes_dict[mappings['indicator'][0]] = [('str', 'str')]
        #add indicator value as column 

    if country_value:
        mappings['country'] = ['country']
        df_data['country'] = country_value
        dtypes_dict[mappings['country'][0]] = [('iso2', 'iso2')]

    if indicator_category_value:
        mappings['indicator_category'] = ['indicator_category']
        df_data['indicator_category'] = indicator_category_value
        dtypes_dict[mappings['indicator_category'][0]] = [('str', 'str')]

    if value_of_date:
        mappings['date_value'] = ['date_value']
        df_data['date_value'] = value_of_date
        dtypes_dict[mappings['date_value'][0]] = [('date', 'date')]

    if unit_of_measure_value:
        if len(unit_of_measure_value.keys()) < 2 :#chect each entry emoty unit_of measure a dict
            mappings['unit_of_measure'] = ['unit_of_measure']
            df_data['unit_of_measure'] = unit_of_measure_value[unit_of_measure_value.keys()[0]]
            dtypes_dict[mappings['unit_of_measure'][0]] = [('str', 'str')]
        else:
            mappings['unit_of_measure'] = ['unit_of_measure']
            dtypes_dict[mappings['unit_of_measure'][0]] = [('str', 'str')]

    return df_data, mappings, dtypes_dict

def check_mapping_dtypes(mappings, dtypes_dict):
    """Begins process of checking if mapped columns are suitable.
    
    Args:
        mappings ({str:[str]}): the users chosen mappings for a file column.
        dtypes_dict ({str:str}): stores the data-types found for each heading.

    Returns: 
        result: indicates whether there is a bad mapping or not.
        correction_mappings ({str:(str,str)}): the conversion needed for each file heading.
        context ({str:data}): the information displayed to the user if mapping is bad.
    """

    correction_mappings = {}
    error_message = []

    for key in mappings:
            if mappings[key]:#this is included incase no mapping is given
                correction_mappings[mappings[key][0]] = []
                temp_results_check_dtype, temp_found_dtype, temp_convert_dtype = check_column_data_type(key, dtypes_dict[mappings[key][0]])

                if temp_results_check_dtype != False:
                    correction_mappings[mappings[key][0]] = (temp_found_dtype, temp_convert_dtype) 
                else:
                    error_message.append(mappings[key][0] + " to " + key + ", found " + temp_found_dtype + ", needed " + temp_convert_dtype + ". ")#datatype blah blah 

    context = {"error_messages" : error_message, "success" : 0}
    return (not len(error_message) > 0), correction_mappings, context 


def get_save_unique_datapoints():
    count  = 0
    ind_dict = {}
    ind_cat_dict = {}
    ind_source_dict = {}
    ind_country_dict = {}
    unique_indicator = [] 
    unique_indicator_cat = [] 
    unique_indicator_source = [] 
    unique_country = []

    if "indicator" in index_order:
        unique_indicator = df_data[index_order["indicator"]].unique()
    if "indicator_category" in index_order:
        unique_indicator_cat = df_data.groupby([index_order["indicator"],index_order["indicator_category"]]).size().reset_index()
    if "source" in index_order:
        unique_indicator_source = df_data.groupby([index_order["indicator"],index_order["source"]]).size().reset_index()
    if "country" in index_order:
        unique_country = df_data[index_order['country']].unique()
    unique_lists = [unique_indicator, unique_indicator_cat, unique_indicator_source, unique_country]
    count = 0

    #change this to use bulk saves
    for unique_list in unique_lists:
        for i in range(len(unique_list)):
            if(count == 0):#indicator
                instance = Indicator.objects.filter(id=unique_list[i]).first()
                #print(unique_list[i])
                if not instance:
                    instance = Indicator(id = unique_list[i])
                    instance.save()
                ind_dict[unique_list[i]] = instance
            elif(count == 1):#indicator_cat
                if "|" in unique_list[index_order['indicator_category']][i]:
                    cats = sorted(list(filter(None, np.unique(np.array(unique_list[index_order['indicator_category']][i].split("|"))))))
                    temp_id = ind_dict[unique_list[index_order['indicator']][i]].id + ("".join(cats[0]))
                    parent, created = IndicatorCategory.objects.get_or_create(unique_identifier= temp_id,
                                                                            name=cats[0], 
                                                                            indicator = ind_dict[unique_list[index_order['indicator']][i]],
                                                                            level=0)
                    
                    if not parent:
                        parent = created  

                 
                    for j in range(1 , len(cats)):                    
                        temp_id = ind_dict[unique_list[index_order['indicator']][i]].id + ("".join(cats[0:j+1]))
                        parent, created = IndicatorCategory.objects.get_or_create(unique_identifier=temp_id,
                                                                                name=cats[j], 
                                                                                indicator = ind_dict[unique_list[index_order['indicator']][i]],
                                                                                parent = parent,
                                                                                level=j)#first()
                        if not parent:
                            parent = created

                    finstance = parent
                else:
                    temp_id = ind_dict[unique_list[index_order['indicator']][i]].id + (unique_list[index_order['indicator_category']][i])
                    finstance, created = IndicatorCategory.objects.get_or_create(unique_identifier=temp_id,
                                                                                name = unique_list[index_order['indicator_category']][i], 
                                                                                indicator = ind_dict[unique_list[index_order['indicator']][i]], 
                                                                                level=0)
                    if not finstance:
                        finstance = created
                    
                ind_cat_dict[unique_list[index_order['indicator']][i] + unique_list[index_order['indicator_category']][i]] = finstance####wrong here
            elif(count == 2):#ind_source
                #print(index_order['source'][i])
                instance = IndicatorSource.objects.filter(id = unique_list[index_order['source']][i].decode(errors='ignore'), indicator = ind_dict[unique_list[index_order['indicator']][i]]).first() 
                if not instance:
                    instance = IndicatorSource(id = unique_list[index_order['source']][i].decode(errors='ignore'), indicator = ind_dict[unique_list[index_order['indicator']][i]])
                    instance.save()
                ind_source_dict[unique_list[index_order['indicator']][i] + unique_list[index_order['source']][i]] = instance
                
            else:#indicator_sub
                #print(unique_list[i])
                instance = Country.objects.filter(code = unique_list[i])
                if instance.count() > 0:
                    #instance.save()
                    ind_country_dict[unique_list[i]] = instance[0]
                else:#not in data base
                    instance = None#Country(code = unique_list[i])
                    #check = unique_list[i]
                    #try:
                    #    instance.save()
                    #    ind_country_dict[unique_list[i]] = instance
                    #except Exception as e:
                        #instance = None
                    ind_country_dict[unique_list[i]] = instance
        count += 1   
