import configparser
import operator
import pandas as pd
import os

import PySimpleGUI as sg

import sql


# https://docs.python.org/3/library/configparser.html


def pace_to_seconds(pace):
    """Converts a running pace in the format mm:ss to seconds."""
    minutes, seconds = map(int, pace.split(':'))
    return minutes * 60 + seconds


# Function to calculate speed
def cal_speed(dist, time):
    return dist / time


# Function to calculate distance travelled
def cal_dis(speed, time):
    return speed * time


# Function to calculate time taken
def cal_time(dist, speed):
    return dist / speed


def calc_time(miles, s_pace):
    seconds = s_pace * miles
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    length = '%d:%02d:%02d' % (hour, min, sec)
    fraction_of_hour = round(hour + (min / 60) + (sec / 3600), 2)
    return length, fraction_of_hour


def calc_requirements(inwater=0, incal=0, insod=0, dectime=0.0):
    reqcal = float(incal) * dectime
    reqsod = float(insod) * dectime
    reqwat = float(inwater) * dectime
    # print('calcout= ',reqcal, reqsod, reqwat)
    return reqcal, reqsod, reqwat


def get_ini(inifile='DataFiles/config.ini'):
    """
    read the ini file and return all values in a dict
    :return:
    """
    # print('in get_ini')
    inifile = os.path.join(os.getcwd(), inifile)

    if not os.path.exists(inifile):
        create_inifile(inifile)
        # print('created new ini')
    config = configparser.RawConfigParser()
    config.read(inifile)
    # nuts = dict(config.items('RNHDEFS') + config.items('NUTRITIONIX'))
    return inifile, config


def read_ini(config, section):
    return dict(config.items(section))


def create_inifile(inifile):
    config = configparser.RawConfigParser()
    if 'RNHDEFS' not in config.sections():
        config.add_section('RNHDEFS')
    config.set('RNHDEFS', 'milesv', '10')
    config.set('RNHDEFS', 'pacev', '7:05')
    config.set('RNHDEFS', 'caloriesv', '240')
    config.set('RNHDEFS', 'sodiumv', '500')
    config.set('RNHDEFS', 'waterv', '500')
    config.set('RNHDEFS', 'dectime', '0.0')
    config.set('RNHDEFS', 'comptime', '4:30:00')
    config.set('RNHDEFS', 'compmsg', 'Time to complete is: 2:05:00 (2.08) hours')
    config.set('RNHDEFS', 'theme', 'BlueMono')
    config.set('RNHDEFS', 'location', 'None')
    config.set('RNHDEFS', 'winsize', 'None')
    if 'NUTRITIONIX' not in config.sections():
        config.add_section('NUTRITIONIX')
    config.set('NUTRITIONIX', 'app_id', 'None')
    config.set('NUTRITIONIX', 'app_key', 'None')

    write_config(inifile, config)
    return


def set_config(config, section, element, value):
    # if section does not exist create it
    if section not in config.sections():
        config.add_section(section)
    # if element does not exist create it
    # set the value
    config.set(section, element, value)


def get_config(config, section, element):
    return config.get(section, element)


def write_config(infile, config):
    with open(infile, 'w') as configfile:
        config.write(configfile)
    configfile.close()


def rewrite_config_file(inifile, configs, values):
    configs['RNHDEFS']['milesv'] = values['milesv']
    configs['RNHDEFS']['pacev'] = values['pacev']
    configs['RNHDEFS']['caloriesv'] = values['caloriesv']
    configs['RNHDEFS']['waterv'] = values['waterv']
    configs['RNHDEFS']['sodiumv'] = values['sodiumv']
    configs['RNHDEFS']['dectime'] = values['dectime']
    configs['RNHDEFS']['comptime'] = values['comptime']
    configs['RNHDEFS']['compmsg'] = values['compmsg']
    configs['RNHDEFS']['theme'] = values['theme']
    configs['RNHDEFS']['location'] = values['location']
    configs['RNHDEFS']['winsize'] = values['winsize']

    write_config(inifile, configs)


def sum_water(df, headers):
    sumwater = pd.DataFrame(headers)
    sumwater['sumwater'] = pd.to_numeric(df['Water'])


def build_prod_list(df):
    """
    build a list of product names. Also insert a blank product for clearing the fields
    :return:
    """
    ndf = df.loc[:, ['Product']]
    ndf.loc[-1] = ['']  # adding a row
    ndf = ndf.sort_values(by=['Product'])
    mlist = ndf['Product'].tolist()
    return mlist


def build_selected_list(df):
    """
    build a list of product names with quanities where Qunatity > 0
    :return: df
    """
    ndf = df.loc[df['Quantity'] > 0].copy()
    ndf = ndf[['Quantity', 'Product', 'Serving Size']]
    values = ndf.values.tolist()
    headings = ndf.columns.tolist()
    # print(ndf)
    return ndf, values, headings


def populate_table():
    """
    read the Product table in the database and build a pandas dataframe. Now take the df
    and extract the headers and the rows.
    :return:
        values = table rows
        headings = column headers
    """
    df = sql.tableToDF("""SELECT * FROM Product ORDER BY Product""")
    values = df.values.tolist()
    headings = df.columns.tolist()

    return df, values, headings


def update_quantity(prod, quant):
    """
    Update the db table with the entered quanity
    :param prod:
    :param quant:
    :return:
        new table, table rows, table column headers
    """
    sql.update_quantity(prod, quant)
    df, values, headings = populate_table()

    return df, values, headings


def get_nutrition_data():
    """
    Read the database containing food information into df

    """
    df = sql.tableToDF("""SELECT * FROM Product""")

    return df


def update_products(inquant=0, inprod='', insod=0, incarb=0, incal=0, inwat=0, inserv=0, insrvt=' ', incaf=0, incom=''):
    """
    add or update products in the database
    if the product exists then update
    else add

    :return:
    """
    if not inprod:
        sg.PopupError('product field cannot be empty')
    else:
        sql.ins_rep(inquant=inquant, inprod=inprod, insod=insod, incarb=incarb, incal=incal, inwat=inwat, inserv=inserv,
                    insrvt=insrvt, incaf=incaf, incom=incom)

    return


def sort_table(table, cols, order):
    """

    :param table:
    :param cols:
    :param order: direction table was last sorted in. Used to order the order
    :return: sorted table, sort direction
    """
    # print('cols=', cols, 'order = ', order)
    # order = not order
    try:
        table = sorted(table, key=operator.itemgetter(cols), reverse=order)
    except Exception as e:
        sg.popup_error('Error in sort_table', 'Exception in sort_table', e)

    return table, order


if __name__ == "__main__":
    # inifile, configs = get_ini('DataFiles/testconfig.ini')
    # set_config(configs, 'TEST', 'elemtest', 'testvalue')
    # write_config(inifile, configs)

    exit()