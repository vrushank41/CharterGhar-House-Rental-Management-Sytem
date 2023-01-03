import pandas as pd
import streamlit as st
from database import view_all_data,getcolumns


def read(table):
    result = view_all_data(table)
    cols = [i[0] for i in getcolumns(table)]
    df = pd.DataFrame(result,columns=cols)
    if st.button("View"):
        st.table(df)
    