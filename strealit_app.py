# created the main python file
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('Snowflake Streamlit Application')
streamlit.header(' 🥣Breakfast Menu')
streamlit.text('  🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('  🥑Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# streamlit.dataframe(my_fruit_list)
my_fruit_list= my_fruit_list.set_index('Fruit')
# streamlit.multiselect("Pick some fruits :", list(my_fruit_list.index))
# streamlit.dataframe(my_fruit_list)
fruits_selected = streamlit.multiselect('Pick some fruits :', list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
# import requests
# streamlit.header("Fruityvice Fruit Advice!")

# try:
#   fruit_choice = streamlit.text_input('What fruit would you like information about?')
#   if not fruit_choice:
#     streamlit.error("Please select a frruit to get information.")
#   else:
def get_fruityvice_data(this_fruit_choice):    
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a frruit to get information.")
  else:
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) 
    # fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # streamlit.dataframe(fruityvice_normalized)
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.stop()  
  
 
    
    
# streamlit.write('The user entered ', fruit_choice)

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # streamlit.text(fruityvice_response)
# # streamlit.text(fruityvice_response.json())
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# # tablular form
# streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
#         my_cur.execute("insert into fruit_load_list values('jackfruit','papaya', 'guava', 'kiwi') ")
        my_cur.execute("insert into fruit_load_list values( '"+ new_fruit +"') ")
        return "Thanks for adding" + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function=insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)



