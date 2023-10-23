import PySimpleGUI as sg
from ctypes import windll
import ast
from nutritionix_api import NutritionixAPI, NutrientCalculator
windll.shcore.SetProcessDpiAwareness(1)
import helpfiles
import sql
import textwrap
import utils


def build_product_lists():
    tdf, ttabdata, theadings = utils.populate_table()
    tmlist = utils.build_prod_list(tdf)
    return tdf, ttabdata, theadings, tmlist


def populate_update_fields(window):
    details = sql.searchdb("SELECT *  FROM Product WHERE Product = '" + str(values['-NUTRITIONPROD-'][0]) + "'")
    fields = details[0]  # get tuple from list
    window['-NNPROD-'].update(values['-NUTRITIONPROD-'][0])
    window['-PRODQUNT-'].update(fields[0])
    window['-PRODCARBS-'].update(fields[2])
    window['-PRODSOD-'].update(fields[3])
    window['-PRODCALS-'].update(fields[4])
    window['-PRODCAFF-'].update(fields[5])
    window['-PRODWATR-'].update(fields[6])
    window['-PRODSRV-'].update(fields[7])
    window['-PRODSRVS-'].update(fields[8])
    window['-PRODCOMM-'].update(fields[12])


def clear_update_fields(window):
    window['-NNPROD-'].update(values['-NUTRITIONPROD-'][0])
    window['-PRODQUNT-'].update('0')
    window['-PRODCARBS-'].update('0')
    window['-PRODSOD-'].update('0')
    window['-PRODCALS-'].update('0')
    window['-PRODCAFF-'].update('0')
    window['-PRODWATR-'].update('0')
    window['-PRODSRV-'].update('0')
    window['-PRODSRVS-'].update(' ')
    window['-PRODCOMM-'].update(' ')


def check_input_values(values):
    '''

    Verify that the input fields contain the correct data. If not, populate with defaults
    :param values:
    :return: values
    '''
    # check pace for : and numerics
    if ':' not in values['-INPACE-']:
        sg.popup_error('The entered pace is not in the format of nn:nn', keep_on_top=True, location=poploc)
        window['-INPACE-'].update('00:00')
    else:
        split_pace = values['-INPACE-'].split(':')
        if not split_pace[0].isnumeric() or not split_pace[1].isnumeric():
            sg.popup_error('The entered pace is not in the format of nn:nn', keep_on_top=True, location=poploc)
            window['-INPACE-'].update('00:00')
            values.update({'-INPACE-': '00:00'})
    # set any blank values to their default
    if values['-INDISTANCE-'] == '':
        values.update({'-INDISTANCE-': '0'})
    if values['-INCALORIES-'] == '':
        values.update({'-INCALORIES-': '0'})
    if values['-INSODIUM-'] == '':
        values.update({'-INSODIUM-': '0'})
    if values['-INWATER-'] == '':
        values.update({'-INWATER-': '0'})

    return values


def set_vvalues():
    # print('in set vvalues: ', vvalues)
    vvalues['milesv'] = values['-INDISTANCE-']
    vvalues['pacev'] = values['-INPACE-']
    vvalues['caloriesv'] = values['-INCALORIES-']
    vvalues['sodiumv'] = values['-INSODIUM-']
    vvalues['waterv'] = values['-INWATER-']
    vvalues['location'] = winloc


def load_selection_list(self):
    df, tdata, headings, mlist = build_product_lists()
    # list_product_selection.clear()
    for vals in mlist:
        self.ui.list_product_selection.addItem(vals)


def reload_all_tables(self):
    df, tabdata, headings, mlist = build_product_lists()
    sdf, sdata, shead = utils.build_selected_list(df)


def get_pop_location(window):
    winloc = window.current_location()
    winsize = window.get_screen_size()
    poploc0 = winloc[0] + 1000
    poploc1 = winloc[1] + 200
    poploc = (poploc0, poploc1)
    errloc = (poploc0+350, poploc1+350)

    return winloc, poploc, errloc, winsize


def get_get_desired_theme():
    """
    Text enter fields for login Id and Key
    Verify the login when ok is pressed
    Stored the Id and Key in the ini file
    :return:
    """
    layout = [
        [sg.Text('Select the theme from the list ')],
        [sg.Listbox(sg.theme_list(), key='themelist', size=(20, 15))],
        [sg.Button('OK'), sg.Button('Cancel')],
    ]

    window = sg.Window('Select the theme', layout, location=poploc).Finalize()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return ''
        else:
            window.close()
            return values['themelist'][0]


def get_nutritionix_login(config):
    """
    Text enter fields for login Id and Key
    Verify the login when ok is pressed
    Stored the Id and Key in the ini file
    :return:
    """
    layout = [
        [sg.Text('Enter NutritionIX Id '), sg.InputText('', key='appid')],
        [sg.Text('Enter NutritionIX Key'), sg.InputText('', key='appkey')],
        [sg.Button('OK'), sg.Button('Cancel')],
    ]

    window = sg.Window('NutritionIX Login Values', layout, location=poploc).Finalize()
    # todo: retrieve login info if it aleady exists
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        else:
            # add login to ini and verify
            utils.set_config(config, 'NUTRITIONIX', 'app_id', values['appid'])
            utils.set_config(config, 'NUTRITIONIX', 'app_key', values['appkey'])
            break

    window.close()

    return


def list_nutritionix_items():
    """
    Text enter fields for login Id and Key
    Verify the login when ok is pressed
    Stored the Id and Key in the ini file
    :return:
    """
    items = ['']
    fd_dict = {}
    layout = [
        [sg.Text('Enter Product to Search: '), sg.InputText('', key='-SEARCHFOR-'), sg.Button('Search')],
        [sg.Radio('Branded', "RADIO1", default=True, key='-brand-'), sg.Radio('Common', "RADIO1", default=False, key='-comm-')],
        [sg.Text('Select your product'), sg.Listbox(items, key='-itemlist-', select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True, size=(45,10))],
        [sg.Button('OK'), sg.Button('Cancel')],
    ]

    window = sg.Window('Online Product Search (NutritionIX)', layout, location=poploc, keep_on_top=True).Finalize()
    thisitem = ''
    while True:

        items = ['']
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        elif event == '-itemlist-':
            thisitem = values['-itemlist-'][0]

        elif event == 'OK':
            if thisitem == '':
                sg.popup_error('You did not select a product from the list, either select an item or press cancel to quit', location=errloc, keep_on_top=True)
                continue
            # let's see if this is already in the database, if so no need to waste a call
            dbsrch = sql.searchdb("SELECT Product FROM Product WHERE Product like '%" + thisitem + "'")
            if dbsrch:
                # the item is already in the db, do not waste a lookup
                continue
            response = nutritionix_api.get_item(fd_dict[thisitem])
            #print(response)
            #response = {'foods': [{'food_name': 'Electrolyte, Fruit Punch', 'brand_name': 'Nuun', 'serving_qty': 1, 'serving_unit': 'tablet', 'serving_weight_grams': 5.5, 'nf_metric_qty': 5.5, 'nf_metric_uom': 'g', 'nf_calories': 10, 'nf_total_fat': None, 'nf_saturated_fat': None, 'nf_cholesterol': None, 'nf_sodium': 360, 'nf_total_carbohydrate': 4, 'nf_dietary_fiber': None, 'nf_sugars': 1, 'nf_protein': None, 'nf_potassium': 100, 'nf_p': None, 'full_nutrients': [{'attr_id': 205, 'value': 4}, {'attr_id': 208, 'value': 10}, {'attr_id': 269, 'value': 1}, {'attr_id': 306, 'value': 100}, {'attr_id': 307, 'value': 360}], 'nix_brand_name': 'Nuun', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'nix_item_name': 'Electrolyte, Fruit Punch', 'nix_item_id': '58411d408e527e7352740f89', 'metadata': {}, 'source': 8, 'ndb_no': None, 'tags': None, 'alt_measures': None, 'lat': None, 'lng': None, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/58411d458e527e7352740f8b.jpeg', 'highres': None, 'is_user_uploaded': False}, 'note': None, 'class_code': None, 'brick_code': None, 'tag_id': None, 'updated_at': '2022-08-02T21:02:15+00:00', 'nf_ingredient_statement': 'WATER, SUGAR, GRAPEFRUIT JUICE CONCENTRATE, CARBON DIOXIDE, GRAPEFRUIT EXTRACT, CITRIC ACID, NATURAL FLAVORS.'}]}
            # print(nutrient_calculator.calculate_calorie_content_me(nutrient_calculator.aggregate_nutrients(response)))
            response = response.get('foods')[0]
            brand = str(response.get('brand_name'))
            my_item = brand + " " + thisitem
            srv_unit = response.get('serving_unit', 0)
            srv_qty = response.get('serving_qty', 0)
            cals = response.get('nf_calories', 0)
            fat = response.get('nf_total_fat', 0)
            prot = response.get('nf_protein', 0)
            carbs = response.get('nf_carbs', 0)
            sodium = response.get('nf_sodium', 0)
            fiber = response.get('nf_dietary_fiber', 0)
            sugars = response.get('nf_sugars', 0)
            potassium = response.get('nf_potassium', 0)
            # pic = response.get('photo')
            # print(pic)
            sql.ins_rep(inquant=0, inprod=my_item, insod=sodium, incarb=carbs, incal=cals, inwat=0,
                        inserv=srv_qty, insrvt=srv_unit, incaf=0, incom='')

            continue

        elif event == 'Search':
            # if searchfor is empty tell user
            if values['-SEARCHFOR-'] == '':
                sg.popup_error("Enter a search term", location=errloc)
                continue

            # nutritionix_api = NutritionixAPI(app_id=vvalues['app_id'], app_key=vvalues['app_key'])
            response = nutritionix_api.search_instant(query=values['-SEARCHFOR-'])
            # response = {'common': [], 'branded': [{'food_name': 'Hydration Endurance Drink Mix, Blueberry Strawberry', 'serving_unit': 'scoop', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Hydration Endurance Drink Mix, Blueberry Strawberry', 'serving_qty': 0.5, 'nf_calories': 30, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/5c91e949c1178fb72996270a.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '5c91e943c1178fb729962709', 'locale': 'en_US'}, {'food_name': 'Endurance Drink Mix, Orange Mango', 'serving_unit': 'pack', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Endurance Drink Mix, Orange Mango', 'serving_qty': 1, 'nf_calories': 60, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/5cd675292e8774f258cb5b95.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '5cd67526fd8f8bc366ebe20d', 'locale': 'en_US'}, {'food_name': 'Nacho Flavored Plant Based Protein Chips', 'serving_unit': 'oz', 'nix_brand_id': '5e32828558cf634277155db7', 'brand_name_item_name': 'Endurance Nacho Flavored Plant Based Protein Chips', 'serving_qty': 1, 'nf_calories': 110, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/64fef62c598200000a895caa.jpeg'}, 'brand_name': 'Endurance', 'region': 1, 'brand_type': 2, 'nix_item_id': '64fef62c598200000a895ca9', 'locale': 'en_US'}, {'food_name': 'Sport, Lemon Lime', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Sport, Lemon Lime', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/608c022b540b5212d7691e91.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '55e5f48c73b5cdfc437292e6', 'locale': 'en_US'}, {'food_name': 'Electrolyte Supplement, Citrus Fruit', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Electrolyte Supplement, Citrus Fruit', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/62adce39af1b1900061480c1.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '586c9f28fec639615cafeac6', 'locale': 'en_US'}, {'food_name': 'Electrolyte, Fruit Punch', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Electrolyte, Fruit Punch', 'serving_qty': 1, 'nf_calories': 10, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/58411d458e527e7352740f8b.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '58411d408e527e7352740f89', 'locale': 'en_US'}, {'food_name': 'Electrolyte Tab, Strawberry Lemonade', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Electrolyte Tab, Strawberry Lemonade', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/56e290f42d25f2e24244d2a0.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '56e290e34ba8078112de99d2', 'locale': 'en_US'}, {'food_name': 'Strawberry Lemonade Flavored Instant Electrolyte Drink Mix', 'serving_unit': 'stick', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Strawberry Lemonade Flavored Instant Electrolyte Drink Mix', 'serving_qty': 1, 'nf_calories': 25, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/652fbde7b5eb9800090a6280.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '652fbde7b5eb9800090a627f', 'locale': 'en_US'}, {'food_name': 'Wild Strawberry Effervescent Tablets', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Wild Strawberry Effervescent Tablets', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/6389dc5437f9e200066f693c.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '6389dc5337f9e200066f693b', 'locale': 'en_US'}, {'food_name': 'Tropical Blast Endurance Blend', 'serving_unit': 'scoop', 'nix_brand_id': '55784572ddfe47543a147ccd', 'brand_name_item_name': 'E-Fuel Tropical Blast Endurance Blend', 'serving_qty': 1, 'nf_calories': 70, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/6510191cb8dd7600083feea9.jpeg'}, 'brand_name': 'E-Fuel', 'region': 1, 'brand_type': 2, 'nix_item_id': '650047a4948e160008478b4a', 'locale': 'en_US'}, {'food_name': 'Active, Tri-Berry', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Active, Tri-Berry', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/615b37f26ba4f4525f8e4062.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '55df5ba34da00e9525173ef5', 'locale': 'en_US'}, {'food_name': 'Energy Supplement, Mixed Berry', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Energy Supplement, Mixed Berry', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/651feba65de4ac000814da37.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '5860c1738e84494e3fd29f92', 'locale': 'en_US'}, {'food_name': 'Energy Tablet, Cherry Limeade', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Energy Tablet, Cherry Limeade', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/6247051dd4078c0009be4d36.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '58256daee2e184b12f05edbb', 'locale': 'en_US'}, {'food_name': 'Active Electrolyte Supplement, Watermelon', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Active Electrolyte Supplement, Watermelon', 'serving_qty': 1, 'nf_calories': 10, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/5854e3ad3761fb8a451634fa.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '585392465e3d356b0667dae7', 'locale': 'en_US'}, {'food_name': 'Immunity, Blueberry Tangerine', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Immunity, Blueberry Tangerine', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/6092dfb78e85e93ea114be40.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '5b98bed24605ec9240feeea2', 'locale': 'en_US'}, {'food_name': 'Electrolyte Supplement', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Electrolyte Supplement', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/64a54fd5384e800008708e8a.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '59a26e9a52cf65760b93a454', 'locale': 'en_US'}, {'food_name': 'Energy Supplement, Mango Orange', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Energy Supplement, Mango Orange', 'serving_qty': 1, 'nf_calories': 10, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/583d280e69147544449db81c.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '583d28336abddf40540e4bd0', 'locale': 'en_US'}, {'food_name': 'Blueberry Pomegranate Hydration Vitamins', 'serving_unit': 'tablet', 'nix_brand_id': '51db37cd176fe9790a899b2e', 'brand_name_item_name': 'Nuun Blueberry Pomegranate Hydration Vitamins', 'serving_qty': 1, 'nf_calories': 10, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/64942b0ea2478900082743b5.jpeg'}, 'brand_name': 'Nuun', 'region': 1, 'brand_type': 2, 'nix_item_id': '64942b0da2478900082743b4', 'locale': 'en_US'}, {'food_name': 'Raspberry lemonade dietary supplement', 'serving_unit': 'tablet', 'nix_brand_id': '5d774d5d46bed3f11d446ea7', 'brand_name_item_name': 'Nuun Hydration Raspberry lemonade dietary supplement', 'serving_qty': 1, 'nf_calories': 15, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/643bd6ed13d3d2000897fde8.jpeg'}, 'brand_name': 'Nuun Hydration', 'region': 1, 'brand_type': 2, 'nix_item_id': '643bd6ec13d3d2000897fde7', 'locale': 'en_US'}, {'food_name': 'Original Plant Based Protein Chips', 'serving_unit': 'bag', 'nix_brand_id': '651febf75de4ac000814db2c', 'brand_name_item_name': 'Natural Endurance Original Plant Based Protein Chips', 'serving_qty': 1, 'nf_calories': 150, 'photo': {'thumb': 'https://nutritionix-api.s3.amazonaws.com/651febf75de4ac000814db2e.jpeg'}, 'brand_name': 'Natural Endurance', 'region': 1, 'brand_type': 2, 'nix_item_id': '651febf75de4ac000814db2d', 'locale': 'en_US'}]}
            if values['-brand-']:
                fdtype = 'branded'
            else:
                fdtype = 'common'

            fd_list = response.get(fdtype)
            fd_dict = {}
            for food in fd_list:
                if fdtype == 'branded':
                    fname = food.get("brand_name_item_name", "Unknown")
                else:
                    fname = food.get("food_name", "Unknown")

                fnix = food.get("nix_item_id", "Unknown")
                fd_dict[fname] = fnix
                items.append(fname)

            window['-itemlist-'].update(items)
            # print(items)
            # print(fd_dict)

            continue

        else:
            pass

    window.close()

    return


def make_window(theme=None):
    # set up the GUI
    if theme:
        sg.theme(theme)
        vvalues['theme'] = theme
    else:
        sg.theme('BlueMono')

    if vvalues['theme'] == 'BlueMono':
        altrowcol = 'lightyellow'
    else:
        altrowcol = None

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['E&xit']],
                ['&Settings',
                 ['Display Theme Choices', 'Select Theme', 'Nutritionix Login']],
                ['&Help', ['&Using Running Nutrition', '&About...']], ]

    # ------- Build the input fields -------- #
    column1 = [[sg.Text('Run Distance', expand_y=True, expand_x=True), ],
               [sg.InputText(size=5, key='-INDISTANCE-', default_text=milesV, tooltip='Enter the run distance',
                             enable_events=True)],
               [sg.Text('')],
               # [sg.Text('')],
               [sg.Button('Refresh'), sg.Button('Exit')]
               ]

    column2 = [[sg.Text('Run Pace')],
               [sg.InputText(size=6, key='-INPACE-', default_text=paceV, tooltip='Enter your desired run pace',
                             enable_events=False)],
               [sg.Text('Run Requirements')],
               [sg.Text('Selected Totals')],
               # [sg.Text('   ', size=5)]
               ]

    column3 = [[sg.Text('Water/hr. (ml)')],
               [sg.InputText(size=5, key='-INWATER-', default_text=waterV, enable_events=True,
                             tooltip='Enter your water requirements per hour in ml')],
               [sg.Text('ReqWat', key='-REQWAT-', size=7, background_color='White')],
               [sg.Text('selwater here', key='-SELWAT-', size=7, background_color='White')],
               # [sg.Text('   ', size=5)]
               ]

    column4 = [[sg.Text('Calories/hr.')],
               [sg.InputText(size=5, key='-INCALORIES-', default_text=caloriesV, enable_events=True,
                             tooltip='Enter your calorie requirement per hour')],
               [sg.Text('ReqCal', key='-REQCAL-', size=7, background_color='White')],
               [sg.Text('selcal here', key='-SELCAL-', size=7, background_color='White')],
               # [sg.Text('   ', size=5)]
               ]

    column5 = [[sg.Text('Sodium/hr. (mg)')],
               [sg.InputText(size=5, key='-INSODIUM-', default_text=sodiumV, enable_events=True,
                             tooltip='Enter your sodium requirement per hour')],
               [sg.Text('ReqSod', key='-REQSOD-', size=7, background_color='White')],
               [sg.Text('sel sod here', key='-SELSOD-', size=7, background_color='White')],
               # [sg.Text('   ', size=5)]
               ]

    selected_table = [
        [sg.Table(values=sdata, headings=['Qty', 'Prod', 'Srv'], enable_click_events=False,
                  col_widths=[5, 10, 5],
                  # auto_size_columns=True,
                  num_rows=8,
                  alternating_row_color=altrowcol,
                  justification='l',
                  key='-STABLE-')]
    ]
    column6 = [[]]
    input_columns = [
        [sg.Column(column1),
         sg.Column(column2),
         sg.Column(column3),
         sg.Column(column4),
         sg.Column(column5),
         sg.Column(selected_table), sg.Button('Copy Table', key='-COPYTABLE-'),
         sg.Button('Search Products', key='-SRCHBTN-')],
    ]

    select_columns = [[sg.Listbox(mlist, select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(30, 10),
                                  enable_events=True, key='-NUTRITIONPROD-',
                                  tooltip='This is a list of all the available products. If you choose one it '
                                          'will populate the Update Product box and highlight '
                                          'the entry in the details table')],
                      [sg.Button('Update Quantity'),
                       sg.InputText(size=5, key='-NEWQUANT-'),
                       sg.Push(),
                       sg.Button('Delete Entry')
                       ]]

    input_table = [
        [sg.Table(values=tabdata, headings=headings, enable_click_events=True,
                  justification='l',
                  # selected_row_colors=('white', 'blue'),
                  alternating_row_color=altrowcol,
                  display_row_numbers=False,
                  key='-PTABLE-', expand_x=True, expand_y=True), ]
    ]

    table_frame = [[sg.Frame('Nutrition Table', input_table)]]

    # build the new product fields
    ncolumnA = [
        [sg.Text('Product Name')],
        [sg.InputText(size=30, key='-NNPROD-', enable_events=True)]
    ]

    ncolumn1 = [
        [sg.Text('Calories')],
        [sg.InputText(size=5, key='-PRODCALS-', default_text='0')],
        [sg.Text('Caffeine')],
        [sg.InputText(size=5, key='-PRODCAFF-', default_text='0')],
        [sg.Text('Servings')],
        [sg.InputText(size=5, key='-PRODSRV-', default_text='0')],

    ]

    ncolumn2 = [
        [sg.Text('Carbs')],
        [sg.InputText(size=5, key='-PRODCARBS-', default_text='0')],
        [sg.Text('Water (ml)')],
        [sg.InputText(size=5, key='-PRODWATR-', default_text='0')],
        [sg.Text('Serving Size')],
        [sg.InputText(size=10, key='-PRODSRVS-', default_text='0')],

    ]

    ncolumn3 = [
        [sg.Text('Sodium (mg)')],
        [sg.InputText(size=5, key='-PRODSOD-', default_text='0')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('Quantity')],
        [sg.InputText(size=5, key='-PRODQUNT-', default_text='0')],
    ]

    ncolumnt = [
        [sg.Text('Comment')],
        [sg.InputText(size=30, key='-PRODCOMM-', default_text=' ')],
        [sg.Button('Add or Update Product')]
    ]

    ninput_columns = [
        [sg.Column(ncolumnA)],
        [sg.Column(ncolumn1),
         sg.Column(ncolumn2),
         sg.Column(ncolumn3)],
        [sg.Column(ncolumnt)],
    ]

    helptext = helpfiles.get_mainhelp()

    # width, lines = size = (40, 32)
    wrapper = textwrap.TextWrapper(width=40, max_lines=32, placeholder=' ...')
    new_text = '\n'.join(wrapper.wrap(helptext))

    ninstruct_columns = [
        [sg.Column([[sg.Text(helptext, size=(40, 25), font=('Helvetica', 12))]],
                   scrollable=True, key='-MAINHELP-')]]

    time_calc = [
        sg.Text(compmsg, key='-COMPMSG-', font=('Helvetica', 24))
    ]

    input_frame = [
        [sg.Frame('Input Area', input_columns, expand_y=False, expand_x=True), ]
    ]

    update_columns = [[sg.Frame('Product Selection', select_columns),
                       sg.Frame('Add or Update Products', ninput_columns),
                       sg.Frame('Instructions', ninstruct_columns)]]

    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [input_frame],
        [sg.HorizontalSeparator()],
        [time_calc],
        [sg.HorizontalSeparator()],
        [update_columns],
        [table_frame],
    ]

    window = sg.Window('Running Nutrition and Hydration', layout, resizable=True, grab_anywhere=True,
                       finalize=True, auto_size_buttons=True, element_justification='l')
    if vvalues['location'] != 'None':
        winloc = vvalues['location']
        if isinstance(winloc, str):
            winloc = ast.literal_eval(winloc)
        window.move(winloc[0], winloc[1])
        # TODO: implement window size remember (winsize var)

    return window


# get the ini file values for the window
inifile, configs = utils.get_ini()
vvalues = utils.read_ini(configs, 'RNHDEFS')
vvalues.update(utils.read_ini(configs,'NUTRITIONIX'))
milesV = vvalues['milesv']
paceV = vvalues['pacev']
caloriesV = vvalues['caloriesv']
sodiumV = vvalues['sodiumv']
waterV = vvalues['waterv']
compTime = vvalues['comptime']
compmsg = vvalues['compmsg']

# app_id = 'e6541bf3'
# app_key = '2848dfdacf3be363a7835fffd9aaf72a'

app_id = vvalues['app_id']
app_key = vvalues['app_key']
nutritionix_api = NutritionixAPI(app_id=app_id, app_key=app_key)
nutrient_calculator = NutrientCalculator()
# works, move it to where it belongs
# response = nutritionix_api.get_nutrients(query='Nuun Endurance Strawberry Lemonade')
# # response = nutritionix_api.search_instant(query='Nuun Endurance Strawberry Lemonade')
# print(response)

df, tabdata, headings, mlist = build_product_lists()
sdf, sdata, shead = utils.build_selected_list(df)

# Create the Window

sortO = True  # flag to track the table sort order

window = make_window(vvalues['theme'])

while True:
    event, values = window.read()
    # print(event, values)
    winloc, poploc, errloc, winsize = get_pop_location(window)
    vvalues['location'] = str(winloc)
    vvalues['winsize'] = str(winsize)
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break
    set_vvalues()
    df, tabdata, headings, mlist = build_product_lists()
    sdf, sdata, shead = utils.build_selected_list(df)
    window['-PTABLE-'].update(tabdata)
    window['-STABLE-'].update(sdata)
    check_input_values(values)
    s_pace = utils.pace_to_seconds(values['-INPACE-'])
    compTime, dectime = utils.calc_time(float(values['-INDISTANCE-']), s_pace)
    compmsg = 'Time to complete is: ' + str(compTime) + '   (' + str(dectime) + ') hours'
    window['-COMPMSG-'].update(compmsg)
    window['-REQCAL-'].update(round(int(values['-INCALORIES-']) * dectime, 2))
    window['-REQSOD-'].update(round(int(values['-INSODIUM-']) * dectime, 2))
    window['-REQWAT-'].update(round(int(values['-INWATER-']) * dectime / 1000, 2))
    window['-SELCAL-'].update(sql.sum_calories())
    window['-SELSOD-'].update(sql.sum_sodium())
    window['-SELWAT-'].update(sql.sum_water() / 1000)

    # if event in ('-INDISTANCE-', '-INPACE-', '-INWATER-', '-INCALORIES-', '-INSODIUM-'):
    #     pass

    if event == '-COPYTABLE-':
        sg.Print(sdf.to_string(index=False), no_titlebar=True, location=poploc)

    if event == 'Using Running Nutrition':
        sg.PopupOK('Help', helpfiles.get_mainhelp(), keep_on_top=True, location=poploc)

    if event == 'Display Theme Choices':
        sg.theme_previewer(columns=5, scrollable=True, scroll_area_size=(1200, 400))

    if event == 'Nutritionix Login':
        get_nutritionix_login(configs)

    if event == '-SRCHBTN-':
        list_nutritionix_items()
        continue

    if event == 'Select Theme':
        # TODO: get theme chooser working
        my_theme = get_get_desired_theme()
        if my_theme:
            window.close()
            window = make_window(theme=my_theme)

    # If a product is selected set the NNPROD variable used by others
    # and highlight and show the entry in the -PTABLE-
    if event == '-NUTRITIONPROD-' and len(values['-NUTRITIONPROD-']):
        if len(values['-NUTRITIONPROD-'][0]) > 0:
            populate_update_fields(window)
        else:
            clear_update_fields(window)
            continue

        itnum = 0
        for item in tabdata:
            if item[1] == str(values['-NUTRITIONPROD-'][0]):
                window['-PTABLE-'].update(select_rows=[itnum])
                if itnum < 5:
                    itnum = 0
                elif itnum > len(tabdata) - 4:
                    itnum = len(tabdata) - 1
                else:
                    # itnum = itnum + 4
                    pass
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[itnum])

                break
            itnum += 1
        continue

    if event == 'Edit Nutrition Data':  # perform quantity Update
        # print('in Edit Nutrition Data')
        if values['-NUTRITIONPROD-'] is None:
            sg.PopupError('Present the new product panel', keep_on_top=True, location=poploc)
            continue

    if event == 'Add or Update Product':
        # print('in Add or Update Product')
        if values['-NNPROD-'] == '':
            sg.popup_error('Enter the product information before clicking the Add button', keep_on_top=True,
                           location=poploc)
            continue
        sql.ins_rep(inquant=values['-PRODQUNT-'], inprod=values['-NNPROD-'], insod=values['-PRODSOD-'],
                    incarb=values['-PRODCARBS-'], incal=values['-PRODCALS-'], inwat=values['-PRODWATR-'],
                    inserv=values['-PRODSRV-'], insrvt=values['-PRODSRVS-'], incaf=values['-PRODCAFF-'],
                    incom=values['-PRODCOMM-'])
        df, tabdata, headings, mlist = build_product_lists()
        window['-NUTRITIONPROD-'].update(mlist)
        # sort the table and update the product lists for display
        sorted_table_values, sortO = utils.sort_table(tabdata, 0, True)
        window['-PTABLE-'].update(sorted_table_values)
        sdf, sdata, shead = utils.build_selected_list(df)
        window['-STABLE-'].update(sdata)

        continue

    if event == 'Update Quantity':  # perform quantity Update
        # print('in Update Quantity')
        if not len(values['-NUTRITIONPROD-']) or not len(values['-NEWQUANT-']):
            sg.popup_error('No product selected or quantity entered', keep_on_top=True, location=poploc)
            continue
        else:
            qprod = values['-NUTRITIONPROD-'][0]
            quant = values['-NEWQUANT-'][0]
            sql.update_quantity(qprod, quant)
            df, tabdata, headings, mlist = build_product_lists()
            # now resort table by quant and redisplay
            sorted_table_values, sortO = utils.sort_table(tabdata, 0, True)
            window['-PTABLE-'].update(sorted_table_values)
            sdf, sdata, shead = utils.build_selected_list(df)
            window['-STABLE-'].update(sdata)

            continue

    if event == 'Delete Entry':  # perform quantity Update
        if (values['-NUTRITIONPROD-'][0]) == '':
            sg.popup_error('No product selected', keep_on_top=True, location=poploc)
            continue
        else:
            if sg.popup_ok_cancel('are you sure you want to delete ' + values['-NUTRITIONPROD-'][0], keep_on_top=True,
                                  location=poploc) != 'OK':
                continue
            else:
                qprod = values['-NUTRITIONPROD-'][0]
                sql.delete_row(qprod)
                df, tabdata, headings, mlist = build_product_lists()
                window['-NUTRITIONPROD-'].update(mlist)
                window['-PTABLE-'].update(tabdata)
                clear_update_fields(window)
                window['-NNPROD-'].update('')
            continue

    if event == 'Refresh':  # if user taps Refresh
        continue

    if isinstance(event, tuple) and event[0] == '-PTABLE-':
        # print('in isinstance tuple: ', event)

        if event[0] == '-PTABLE-':
            # print('in event: ', event)
            if event[2][0] is None:
                continue
            if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                # print('event[2][0] is -1', event)
                col_num_clicked = event[2][1]
                sortO = not sortO  # sort the table by the column. each click reverses the sort
                sorted_table_values, sortO = utils.sort_table(tabdata, col_num_clicked, sortO)
                window['-PTABLE-'].update(sorted_table_values)
                # set the table display to the top row after a sort
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[0])

            if event[2][0] >= 0:
                window['-PTABLE-'].update(row_colors=((event[2][0], 'white', 'red'), (event[2][0], 'white', 'darkblue')))
                # set the table display to the top
                iix = int(event[2][0])
                # print(iix, type(iix))
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[iix])
            continue
        continue

# closing the app, rewrite the config values
utils.rewrite_config_file(inifile, configs, vvalues)

window.close()
