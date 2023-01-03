import streamlit as st

from create import create

from delete import delete
from read import read
from update import update
from application import application

from database import show_tables,ExecuteManualQuery

def main():
    col1,col2=st.columns([2,3])
    with col1:
        st.title("Charter-Ghar")
    with col2:
        st.header("House Rental Management System")
    st.subheader("VRUSHANK G -- PES1UG20CS516")
    menu = ["ADD", "VIEW", "EDIT/UPDATE", "DELETE","GET CONTRACT","SQL Window"]
    choice = st.sidebar.selectbox("Menu", menu)
    showtables = [i[0].capitalize() for i in show_tables()]
    forread= [i[0].capitalize() for i in show_tables()]
    forupdate= [i[0].capitalize() for i in show_tables()]
    # st.info(showtables)
    del showtables[0]
    del showtables[0]
    del showtables[3]
    del showtables[3]
    del showtables[4]
    
    del forupdate[0]
    del forupdate[0]
    del forupdate[1]
    del forupdate[2]
    del forupdate[4]

    
    

    if choice == "ADD":
        table=st.selectbox("Select Table", showtables)
        st.subheader("Add Details:")
        create(table)

    elif choice == "VIEW":
        table=st.selectbox("Select Table", forread)
        st.subheader("View details")
        read(table)

    elif choice == "EDIT/UPDATE":
        del forupdate[2]
        table=st.selectbox("Select Table", forupdate)
        st.subheader("Update the details here")
        update(table)

    elif choice == "DELETE":
        table=st.selectbox("Select Table", showtables)
        st.subheader("Delete entries")
        delete(table)
    
    elif choice=="GET CONTRACT":
        application()
    elif choice=="SQL Window":
        query=st.text_area("Enter the SQL query in right MariaDB format!")
        ExecuteManualQuery(query)
    
    

if __name__ == '__main__':
    main()
