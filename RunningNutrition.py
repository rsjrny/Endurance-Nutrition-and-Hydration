import PySimpleGUI as sg
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
    # print(values)

    if ':' not in values['-INPACE-']:
        sg.popup_error('Pace must contain a :, as in 7:55')
        values.update({'-INPACE-': '00:00'})
    if values['-INDISTANCE-'] == '':
        values.update({'-INDISTANCE-': '0'})
    if values['-INCALORIES-'] == '':
        values.update({'-INCALORIES-': '0'})
    if values['-INSODIUM-'] == '':
        values.update({'-INSODIUM-': '0'})
    if values['-INWATER-'] == '':
        values.update({'-INWATER-': '0'})

    return values


FRAME_BORDER_WIDTH = 10

# print(sg.__version__)
# print(sg.sys.version)
# print(sg.tclversion_detailed)

# get the ini file values for the window
inifile, configs = utils.get_ini()
milesV = utils.get_config(configs, 'DEFAULT', 'milesV')
paceV = utils.get_config(configs, 'DEFAULT', 'paceV')
caloriesV = utils.get_config(configs, 'DEFAULT', 'caloriesV')
sodiumV = utils.get_config(configs, 'DEFAULT', 'sodiumV')
waterV = utils.get_config(configs, 'DEFAULT', 'waterV')
# mytheme = utils.get_config(configs, 'WINDOW', 'theme')

s_pace = utils.pace_to_seconds(paceV)
compTime, dectime = utils.calc_time(float(milesV), s_pace)
compmsg = 'Time to complete is: ' + str(compTime) + '   (' + str(dectime) + ') hours'

# set up the GUI
theme_list = sg.theme_list()
sg.theme('BlueMono')

# ------ Menu Definition ------ #
menu_def = [['&File', ['E&xit']],
            ['&Settings',
             ['Display Theme Choices', 'Select Theme', 'Nutritionix (not available yet)', ['AppId', 'AppKey']], ],
            ['&Help', ['&Using Running Nutrition', '&About...']], ]

# ------- Build the input fields -------- #
column1 = [[sg.Text('Run Distance', expand_y=True, expand_x=True), ],
           [sg.InputText(size=5, key='-INDISTANCE-', default_text=milesV, tooltip='Enter the run distance',
                         enable_events=True)],
           [sg.Text('')],
           [sg.Text('   ', size=5)],
           [sg.Text('')],
           # [sg.Text('   ', size=15)]
           [sg.Button('Refresh'), sg.Button('Exit')]
           ]

column2 = [[sg.Text('Run Pace')],
           [sg.InputText(size=6, key='-INPACE-', default_text=paceV, tooltip='Enter your desired run pace',
                         enable_events=False)],
           [sg.Text('')],
           [sg.Text('   ', size=5)],
           [sg.Text('')],
           [sg.Text('   ', size=5)]
           ]

column3 = [[sg.Text('Water/hr. (ml)')],
           [sg.InputText(size=5, key='-INWATER-', default_text=waterV, enable_events=True,
                         tooltip='Enter your water requirements per hour in ml')],
           [sg.Text('Water Required (Liters)')],
           [sg.Text('ReqWat', key='-REQWAT-', size=7, background_color='White')],
           [sg.Text('Water Selected')],
           [sg.Text('selwater here', key='-SELWAT-', size=7, background_color='White')]
           ]

column4 = [[sg.Text('Calories/hr.')],
           [sg.InputText(size=5, key='-INCALORIES-', default_text=caloriesV, enable_events=True,
                         tooltip='Enter your calorie requirement per hour')],
           [sg.Text('Calories Required (g)')],
           [sg.Text('ReqCal', key='-REQCAL-', size=7, background_color='White')],
           [sg.Text('Calories Selected')],
           [sg.Text('selcal here', key='-SELCAL-', size=7, background_color='White')]
           ]

column5 = [[sg.Text('Sodium/hr. (mg)')],
           [sg.InputText(size=5, key='-INSODIUM-', default_text=sodiumV, enable_events=True,
                         tooltip='Enter your sodium requirement per hour')],
           [sg.Text('Sodium Required (mg)')],
           [sg.Text('ReqSod', key='-REQSOD-', size=7, background_color='White')],
           [sg.Text('Sodium Selected')],
           [sg.Text('sel sod here', key='-SELSOD-', size=7, background_color='White')]
           ]

input_columns = [
    [sg.Column(column1),
     sg.Column(column2),
     sg.Column(column3),
     sg.Column(column4),
     sg.Column(column5)],
]

df, tabdata, headings, mlist = build_product_lists()
sdf, sdata, shead = utils.build_selected_list(df)

select_columns = [[sg.Listbox(mlist, select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(30, 15),
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
              justification='l', selected_row_colors=('white', 'blue'),
              alternating_row_color='lightyellow', display_row_numbers=False,
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

width, lines = size = (40, 32)
wrapper = textwrap.TextWrapper(width=40, max_lines=32, placeholder=' ...')
new_text = '\n'.join(wrapper.wrap(helptext))

ninstruct_columns = [[sg.Column([[sg.Text(helptext, size=(40,32), font=('Helvetica', 12) )]], scrollable=True, key='-MAINHELP-')]]

time_calc = [
    sg.Text(compmsg, key='-COMPMSG-', font=('Helvetica', 24))
]

selected_table = [
    [sg.Table(values=sdata, headings=['Qty', 'Prod', 'Srv'], enable_click_events=False,
              col_widths=[5, 10, 5],
              # auto_size_columns=True,
              # size=(45, 17),
              alternating_row_color='lightyellow',
              justification='l', selected_row_colors=('white', 'blue'),
              key='-STABLE-') ]
]
input_frame = [
    [sg.Frame('Input Area', input_columns, expand_y=False, expand_x=True),
     sg.Frame('Selected Products', selected_table, expand_y=False, expand_x=True)]
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

# Create the Window

sortO = True  # flag to track the table sort order

window = sg.Window('Running Nutrition and Hydration', layout, resizable=True, grab_anywhere=True,
                   auto_size_buttons=True, finalize=True, element_justification='l')
# window['-MAINHELP-'].TKOut.output.config(wrap='word')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # print(event, values)
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

    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break

    # if event in ('-INDISTANCE-', '-INPACE-', '-INWATER-', '-INCALORIES-', '-INSODIUM-'):
    #     pass

    if event == 'Using Running Nutrition':
        sg.PopupOK('Help', helpfiles.get_mainhelp())

    # If a product is selected set the NNPROD variable used by others
    # and highlight and show the entry in the -PTABLE-
    if event == '-NUTRITIONPROD-' and len(values['-NUTRITIONPROD-']):
        if len(values['-NUTRITIONPROD-'][0]) > 0:
            populate_update_fields(window)
        else:
            clear_update_fields(window)
            pass

        itnum = 0
        for item in tabdata:
            if item[1] == str(values['-NUTRITIONPROD-'][0]):
                window['-PTABLE-'].update(select_rows=[itnum])
                # print('len tabdata = ', len(tabdata))
                if itnum < 5:
                    itnum = 0
                elif itnum > len(tabdata) - 4:
                    itnum = len(tabdata) - 1
                else:
                    # itnum = itnum + 4
                    pass
                # print('itnum = ', itnum)
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[itnum])

                break
            itnum += 1
        pass

    if event == 'Edit Nutrition Data':  # perform quantity Update
        # print('in Edit Nutrition Data')
        if values['-NUTRITIONPROD-'] is None:
            sg.PopupError('Present the new product panel')
            pass

    if event == 'Add or Update Product':
        # print('in Add or Update Product')
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
        #

        pass

    if event == 'Update Quantity':  # perform quantity Update
        # print('in Update Quantity')
        if not len(values['-NUTRITIONPROD-']) or not len(values['-NEWQUANT-']):
            sg.popup_error('No product selected or quantity entered')
            pass
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
            pass

    if event == 'Delete Entry':  # perform quantity Update
        if (values['-NUTRITIONPROD-'][0]) == '':
            sg.popup_error('No product selected')
            pass
        else:
            if sg.popup_ok_cancel('are you sure you want to delete ' + values['-NUTRITIONPROD-'][0]) != 'OK':
                pass
            else:
                qprod = values['-NUTRITIONPROD-'][0]
                sql.delete_row(qprod)
                df, tabdata, headings, mlist = build_product_lists()
                window['-NUTRITIONPROD-'].update(mlist)
                window['-PTABLE-'].update(tabdata)
            pass

    if event == 'Refresh':  # if user taps Refresh
        pass

    if isinstance(event, tuple) and event[0] == '-PTABLE-':
        # print('in isinstance tuple: ', event)
        if event[0] == '-PTABLE-':
            # print('in event: ', event[0])
            if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                # print('event[2][0] is -1', event)
                col_num_clicked = event[2][1]
                sortO = not sortO  # sort the table by the column. each click reverses the sort
                sorted_table_values, sortO = utils.sort_table(tabdata, col_num_clicked, sortO)
                window['-PTABLE-'].update(sorted_table_values)
                # set the table display to the top row after a sort
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[0])

            if event[2][0] >= 0:
                window['-PTABLE-'].update(row_colors=((event[2][0], 'white', 'red'), (event[2][0], 'white', 'red')))
                # set the table display to the top
                iix = int(event[2][0])
                # print(iix, type(iix))
                window['-PTABLE-'].Widget.see(window['-PTABLE-'].tree_ids[iix])
            pass
        pass

# closing the app, rewrite the config values
utils.rewrite_config_file(inifile, configs, values)

window.close()
