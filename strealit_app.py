# created the main python file
import streamlit
import pandas as pd
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
import requests
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
# streamlit.text(fruityvice_response)
# streamlit.text(fruityvice_response.json())
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# tablular form
streamlit.dataframe(fruityvice_normalized)



