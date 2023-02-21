# Inventory Management App

## About
This web application is a remake of a data entry application I built in my previous role with some tweaks and variations. For example, the program I built was for a loan tracker. This application is an inventory management system for a mock clothing store.

## Tools & Libraries used:
  1. Python
  2. Flask
  3. HTML
  4. CSS
  5. gspread
  6. os
  7. dotenv

## App Functions

![homepage](https://user-images.githubusercontent.com/75923327/220240671-eca7c206-8e62-4176-a514-f3a00835e27c.png)


The web application will bring you to a page that asks if you would like to:
  1. add a new product or 
  2. update an exisiting product. 
  
 ## Function 1: Add New Product

![image](https://user-images.githubusercontent.com/75923327/220240908-3b408823-3441-4da1-a30b-94494911b9ba.png)

Clicking on "Add New Product" will take you to a page to enter the information of the new product you would like to add (please note: all fields in the form must be filled out before submitting). Once you have filled out the product information, click "submit". 

Clicking submit will do some things on the backend in python:
  1. The program will get all the data that was entered on the form and store it in a dictionary. 
  2. A unique Product ID number and a unique SKU number will be created for the new product. 
  3. This data including the Product ID and SKU number will be appended to a new row in the "Clothing Store Inventory" sheet [found here](https://docs.google.com/spreadsheets/d/13P_XzQkFN_z51AtpwR5r03YZMrWf4BF7JjBdMmDhFBk/edit?usp=sharing). 

 ## Function 2: Update Existing Product
 
![image](https://user-images.githubusercontent.com/75923327/220243698-7c3a3f44-e739-4157-a5c4-9a2ca77b6422.png)

Clicking on "Update Exisitng Product" will take you to a page to enter the information you would like to update for an existing product (please note: you must select a current ID from the dropdown menu before submitting). Once you have fillde out the information you would like to update, click "update". 

Clicking submit will do some things on the backend in python:
  1. Locate the selected Product ID on the "Clothing Store Inventory" sheet and find the row. 
  2. The program will get all the data that was entered on the form and store it in a dictionary. 
  3. This data will be used to update the data for each cell for the given Product ID on the "Clothing Store Inventory" sheet [found here](https://docs.google.com/spreadsheets/d/13P_XzQkFN_z51AtpwR5r03YZMrWf4BF7JjBdMmDhFBk/edit?usp=sharing). 
