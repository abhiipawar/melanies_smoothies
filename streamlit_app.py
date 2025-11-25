# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothie Orders :cup_with_straw: {st.__version__}")
st.write(
  """Orders that need to be filled!
  """
)

session = get_active_session()

my_dataframe = session.table("smoothies.public.orders").select(col('ORDER_UID'),col('INGREDIENTS'),col('NAME_ON_ORDER'),col('ORDER_FILLED'))
editable_df = st.data_editor(my_dataframe)

if my_dataframe:
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success('Order(s) Updated!',icon="👍")
        except:
            st.write('Something went wrong')
else:
    st.write('There are no more pending Orders right now',icon="👍")
