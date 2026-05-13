import streamlit as st # sirve para el select box d abajo 
import requests  
from snowflake.snowpark.functions import col    

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


#https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


#https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

if ingredients_list: # si no es nulo hace lo d adentro 
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    # todavia no lo corre, solo lo guarda en variable y lo escribe en streamlit 
    my_insert_stmt = """ insert into smoothies.public.orders (ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #############
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        # ahora si lo corre 
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+name_on_order, icon="✅")
