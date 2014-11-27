# coding: utf-8
import json
import locale
import datetime
import os
from utils.robots.locale_manager import convert_orig_month_name_to_lib


def get_valid_date_for_str(date_str):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    res_date = None
    res_date_text = ''
    dates_parts = date_str.split(' ')
    if len(dates_parts) == 3:
        year = dates_parts[2]
    else:
        year = u'2014'
    if len(dates_parts) == 1:
        if date_str == u'Сегодня':
            day = datetime.datetime.now().day
        elif date_str == u'Вчера':
            day = datetime.date.fromordinal(datetime.date.today().toordinal()-1).day
        res_date_text = str(day) + ' ' + str(datetime.datetime.now().month) + ' ' + year
        res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %m %Y").date()
    else:
        try:
            res_date_text = dates_parts[0] + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
        except ValueError, e:
            res_date_text = u'1' + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
            print "Datetime converting error: ", dates_parts[0], convert_orig_month_name_to_lib(dates_parts[1]), year
        except Exception, e:
            print e.message
    return res_date


def save_loaded_data_to_file(loaded_json_data, file_name, sub_dir_name):
    saved_pages_directory = 'saved_pages'
    saved_file_name = file_name + '.json'
    try:
        if not os.path.exists(saved_pages_directory):
            os.makedirs(saved_pages_directory)
        site_dir = saved_pages_directory + '/' + sub_dir_name
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)
        with open(site_dir + '/' + saved_file_name, 'w') as f:
            json.dump(loaded_json_data, f)

    except Exception, e:
        import traceback
        print "Saving failed with error:", traceback.print_exc()
        return None
    return site_dir + '/' + saved_file_name