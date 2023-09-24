import os
import streamlit as st
from streamlit_option_menu import option_menu
import sql
import utils

# set default values for 1st time run. These values are updated by the user later on and the vars will be updated
if os.getenv('paceV') is None:
    os.environ['paceV'] = '10:30'
if os.getenv('milesV') is None:
    os.environ['milesV'] = '26.2'
if os.getenv('waterV') is None:
    os.environ['waterV'] = '500'
if os.getenv('sodiumV') is None:
    os.environ['sodiumV'] = '500'
if os.getenv('calorieV') is None:
    os.environ['calorieV'] = '240'

df_colNames = ['Quantity', 'Product', 'Sodium (mg)', 'Water', 'Carbs', 'Calories', 'Serving', 'Serving Size',
               'Caffeine', 'Total Carbs', 'Total Sodium', 'Total Calories', 'Comment']


# @st.cache


def get_nutrition_data():
    """
    Read the database containing food information into df

    """
    df = sql.tableToDF("""SELECT * FROM Product""")

    return df


def put_nutrition_data(df):
    """
    Read the database containing food information into df

    """
    sql.dftoSQL(df, 'Product')


def sidebar(df):
    """
    build the application sidebar and return the calculated fields
    :return:
        pace: your pace
        miles: run length in miles
        waterV: water consumption per hour
        sodiumV: sodium consumption per hour
        calorieV: calories needed per hour
        compTime: time to complete the run
        dectime: time to complete run in decimal

    """

    pace = st.sidebar.text_input("Run Pace", placeholder="mm:ss", value=os.getenv('paceV'))
    if pace == '' or pace is None:
        pace = "10:30"
    os.environ['paceV'] = pace
    s_pace = utils.pace_to_seconds(pace)
    miles = st.sidebar.number_input("Run Length (miles)", min_value=0.0, max_value=500.0, step=0.10,
                                    value=float(os.getenv('milesV')), format="%.2f")
    os.environ['milesV'] = str(miles)
    compTime, dectime = utils.calc_time(miles, s_pace)
    waterV = st.sidebar.number_input("My Water Requirements- ml per hour", min_value=0, max_value=2000, step=10,
                                     value=int(os.getenv('waterV')))
    os.environ['waterV'] = str(waterV)
    sodiumV = st.sidebar.number_input("My sodium Requirements - mg per hour", min_value=0, max_value=2000, step=10,
                                      value=int(os.getenv('sodiumV')))
    os.environ['sodiumV'] = str(sodiumV)
    calorieV = st.sidebar.number_input("My calories Requirements - per hour", min_value=0, max_value=2000, step=10,
                                       value=int(os.getenv('calorieV')))
    os.environ['calorieV'] = str(calorieV)

    return df, pace, miles, waterV, sodiumV, calorieV, compTime, dectime


def extra():
    """
    build the application sidebar and return the calculated fields
    :return:
        pace: your pace
        miles: run length in miles
        waterV: water consumption per hour
        sodiumV: sodium consumption per hour
        calorieV: calories needed per hour
        compTime: time to complete the run
        dectime: time to complete run in decimal

    """
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        with col1:
            pace = st.text_input("Run Pace ", placeholder="mm:ss", value=os.getenv('paceV'))
            if pace == '' or pace is None:
                pace = "10:30"
            os.environ['paceV'] = pace
            s_pace = utils.pace_to_seconds(pace)
        with col2:
            miles = st.number_input("Run Length (miles) ", min_value=0.0, max_value=500.0, step=0.10,
                                            value=float(os.getenv('milesV')), format="%.2f")
            os.environ['milesV'] = str(miles)
            compTime, dectime = utils.calc_time(miles, s_pace)
        with col3:
            waterV = st.number_input("Water Requirements- ml per hour", min_value=0, max_value=2000, step=10,
                                             value=int(os.getenv('waterV')))
            os.environ['waterV'] = str(waterV)

        with col4:
            sodiumV = st.number_input("Sodium Requirements - mg per hour", min_value=0, max_value=2000,
                                              step=10,
                                              value=int(os.getenv('sodiumV')))
            os.environ['sodiumV'] = str(sodiumV)
        with col5:
            calorieV = st.number_input("Calories Requirements - per hour", min_value=0, max_value=2000, step=10,
                                       value=int(os.getenv('calorieV')))
            os.environ['calorieV'] = str(calorieV)

    return pace, miles, waterV, sodiumV, calorieV, compTime, dectime


def page_setup():

    st.set_page_config(page_title='Running Nutrition Dashboard', layout='wide')
    st.markdown('<style>body{background-color: lightgreen;}</style>', unsafe_allow_html=True)
    styles = 'text-align: center; color: blue; font-size:300%; border-style: solid; background-color: powderblue;'
    # # 2. horizontal menu
    # selected2 = option_menu(None, ['Settings'],
    #                         icons=['gear'],
    #                         menu_icon="cast", default_index=0, orientation="horizontal")
    # st.text_input("Database Location")
    st.markdown("<h1 style='" + styles + "'>Running Nutrition Dashboard</h1>", unsafe_allow_html=True)
    # https://discuss.streamlit.io/t/colored-boxes-around-sections-of-a-sentence/3201/2
    # local_css("mycss.css")


    return st.container()


def clear_quantities():
    sql.reset_quantity()
    return


def refresh_page():

    return


def build_buttons():
    '''
    build the row of buttons.
    we set up 3 columns and are only using the first column so the buttons will be close together
    :return:
        edit value based on button click
    '''
    with st.container():
        pl = build_prod_list()
        col1, col2, col3, col4 = st.columns(4, gap='small')
        with col1:
            tprod = st.selectbox('Product:', pl)
            refresh = st.button('Refresh', on_click=refresh_page)
        with col2:
            if not tprod:
                tquan = 0
            tquan = st.number_input('Selected Quantity', value=0)
            if st.button('Clear All Quantities'):
                clear_quantities()
        with col3:
            st.text("Click to update the Quantity")
            if st.button('Update Quantity'):
                update_quantity(tprod, tquan)
        with col4:
            st.text("select a product and press to delete from the database")
            if st.button('Delete Product'):
                sql.delete_row(tprod)
        tquan = 0

    return


def update_products(inquant=0, inprod='', insod=0, incarb=0, incal=0, inwat=0, inserv=0, insrvt=' ', incaf=0, incom=''):
    """
    add or update products in the database
    if the product exists then update
    else add

    :return:
    """
    if not inprod:
        st.text('product field cannot be empty')
    else:
        sql.ins_rep(inquant=inquant, inprod=inprod, insod=insod, incarb=incarb, incal=incal, inwat=inwat, inserv=inserv,
                insrvt=insrvt, incaf=incaf, incom=incom)

    refresh_page()
    return


def build_prod_list():
    """
    build a list of product names. Also insert a blank product for clearing the fields
    :return:
    """
    ndf = df.loc[:, ['Product']]
    ndf.loc[-1] = ['']  # adding a row
    ndf = ndf.sort_values(by=['Product'])
    mlist = ndf['Product'].tolist()
    return mlist


def update_quantity(prod, quant):
    sql.update_quantity(prod, quant)
    get_nutrition_data()
    return


def populate_form(val):

    dbout = sql.searchdb("SELECT * FROM Product WHERE Product = '" + val + "'")

    build_form(inquant=dbout[0][0], inprod=dbout[0][1], incarb=dbout[0][2], insod=dbout[0][3], incal=dbout[0][4],
               incaf=dbout[0][5], inwat=dbout[0][6], inserv=dbout[0][7], insrvt=dbout[0][8], incom=dbout[0][12])

    return


def build_form(inquant=0, inprod='', insod=0, incarb=0, incal=0, inwat=0, inserv=0, insrvt=' ', incaf=0, incom=''):
    with st.form('Update',clear_on_submit=True):
        cont1 = st.container()
        with cont1:
            wstr = 'Enter or modify products here:'
            st.text(wstr)
            prod = st.text_input('product', value=inprod)
            c1, c2, c3, = st.columns(3)
            with c1:
                car = st.number_input('Carbs', value=incarb)
                ser = st.number_input('Servings', value=inserv)
                caf = st.number_input('Caffeine (mg)', value=incaf)
                com = st.text_input('Comment', value=incom)
            with c2:
                cals = st.number_input('calories', value=incal)
                srt = st.text_input('Serving Size', value=insrvt)
                wat = st.number_input('Water (ml)', value=inwat)
                quan = st.number_input('Quantity', value=inquant)
            with c3:
                sod = st.number_input('Sodium (mg)', value=insod)

            submit = st.form_submit_button('update', on_click=update_products(inquant=quan, inprod=prod, insod=sod,
                                                                              incarb=car, incal=cals, inwat=wat,
                                                                              inserv=ser, insrvt=srt,
                                                                              incaf=caf, incom=com))


if __name__ == '__main__':
    # TODO: add parse args to supply startup default calories, sodium, water / hour values
    conta = page_setup()
    df = get_nutrition_data()
    # df, pace, miles, waterV, sodiumV, calorieV, compTime, dectime = sidebar(df)

    with conta:
        pace, miles, waterV, sodiumV, calorieV, compTime, dectime = extra()
        st.subheader("Time to Complete " + str(round(miles, 2)) + " miles: " + str(compTime) + " (" + str(
            round(dectime, 2)) + " hrs.)")
        wstr = "Total Calories Required: " + str(round(calorieV * dectime, 2)) + ', ' + \
                "Total Sodium Required: " + str(round(sodiumV * dectime, 2)) + ' mg, ' + \
                 "Total Water Required: " +  str(round((waterV * dectime) / 1000, 2)) + ' Litres'
        st.text(wstr)

        totCal = df['Total Calories'].sum()
        totSod = df['Total Sodium'].sum()
        totCarb = df['Total Carbs'].sum()
        wstr = "Total Calories Selected: " + str(totCal) + " Total Sodium Selected: " + str(totSod) + \
               " Total Carbs Selected: " + str(totCarb)

        st.text(wstr)
        wstr = "Total Per Hour Calories: " + str(round(float(totCal) / float(dectime), 2)) + \
                 " Total Per Hour Sodium: " + str(round(float(totSod) / float(dectime), 2)) + \
                 " Total Per Hour Carbs: " + str(round(float(totCarb) / float(dectime), 2))
        st.text(wstr)
        build_buttons()
        with st.expander('Collapse to hide full data table', expanded=True):
            st.dataframe(df, hide_index=True)
        mlist = build_prod_list()
        srchfor = st.selectbox('Populate_Form with:', mlist)

        if srchfor:
            populate_form(srchfor)
        else:
            build_form()
