# Running Nutrition and Hydration

# far from complete

## Description

This app is designed to help you choose the correct nutrition for your run based on your hourly hydration and Nutrition requirements.
You can manually enter the product and nutritional information or signup for a free Id and Key from NutritionIX and download
the nutritional values from their database.

## Features

- Enter you run length, run pace, hourly requirements for Calories, Sodium and Water.
- Select products from the product list.
- See the values for Calories, Sodium, and Water summed from your selected products.
- Add new products to your nutrition database.

## Instructions

1. Create folder on your PC
2. copy the /DataFiles/ folder to the new folder in step 1
3. Copy the /dist/RunningNutrition.exe to your PC into the new folder.
4. execute RunningNutrition.exe
5. Update your Run input parameters.
6. Enter the quantity for each item you will bring.

## NutritionIX Information

https://developer.nutritionix.com/

Signup for a free account (limited to 25 searches per day)  
Choose View API Keys  
Select 'Create new key'  
Enter your Id and Key under the settings menu   


## Installation Notes

Build the exe was performed using 
pyinstaller --onefile --windowed RunningNutrition.py  

### Execution

copy /dist/RunningNutrition.exe and 
/DataFiles/*.*  to a new folder   
cd to the folder then execute RunningNutrition.exe

## packages used

NutritionIX  
PySimpleGiu  
Pandas


## Author

Russ Lilley
RussLilley@yahoo.com
rsjrny software

