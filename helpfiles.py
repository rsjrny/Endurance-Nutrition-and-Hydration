import PySimpleGUI as sg


mainhelp = ''

def get_mainhelp():
    text = ('The Running Nutrition app will assist you in the selection of hydration and nutrition. '
            'Going for a long run, big race coming up? Let the app help you decide what to bring.\n\n'
            'The first step is to enter your:\n'
            '   Run Distance in miles\n'
            '   Run Pace in mm:ss\n'
            'Then your hourly requirements for:\n'
            '   Water (ml),\n'
            '   Calories (g),\n'
            '   Sodium (mg).\n'
            'The app will calculate your required amounts based on distance and pace\n'
            'Now select from the Product Selection list a product and enter a quantity. Press the "Update"'
            'button.\n'
            'Your selected product and quantity will display in the "Selected Products" area and the'
            '"Total selected" fields will be updated. Keep selecting products until your get close to your'
            'required amounts.\n'
            'Whenever you select a product from the list it will also be displayed and highlighted in the'
            'Nutrition table area and the values will populate in the "Add or Update Product" area.\n'
            'To add a new product to the application database you will\n'
            '  1.  Select the blank product in the "Production Selection" List\n'
            '  2.  Fill in the fields from the values on the nutrition label\n'
            '  3.  Press the "Add or Update Product" button'
            )
    return text

