import streamlit as st
from database import add_data_owner,add_data_oph,getcolumns,add_data_tenant,add_data_tph,add_data_house,add_data_house_type,c
import datetime as dt

def create(table):
    cols = [i[0] for i in getcolumns(table)]
    type = [i[1] for i in getcolumns(table)]
    # st.write(cols,type)
    
    def create_owner():
        # c.execute("Select Owner_ID from Owner")
        # data=c.fetchall()
        # ownerid=[i for i in data]
        col1,col2=st.columns(2)
        with col1:
            F_Name = st.text_input("Firstname")
            Username = st.text_input("Username")
            DOB = st.date_input("DOB",value=dt.datetime.today(),
                min_value=dt.datetime.today() - dt.timedelta(days=10000),
                max_value=dt.datetime.today())
            ph=st.text_input("Ph.No")
        with col2:
            L_Name = st.text_input("Lastname")
            Password = st.text_input("Password",type="password")
            Owner_Addr = st.text_area("Address")

        if st.button("Submit"):
            add_data_owner(F_Name,L_Name,Username,Password,Owner_Addr,DOB)
            add_data_oph(Username,ph)
            st.success("Added the details of {} in Owner".format(Username))
    
    def create_tenant():
        col1,col2=st.columns(2)
        with col1:
            F_Name = st.text_input("Firstname")
            Username = st.text_input("Username")
            DOB = st.date_input("DOB",value=dt.datetime.today(),
                min_value=dt.datetime.today() - dt.timedelta(days=10000),
                max_value=dt.datetime.today())
            ph=st.text_input("Ph.No")
        with col2:
            L_Name = st.text_input("Lastname")
            Password = st.text_input("Password",type="password")
            Tenant_Addr = st.text_area("Address")

        if st.button("Submit"):
            add_data_tenant(F_Name,L_Name,Username,Password,Tenant_Addr,DOB)
            add_data_tph(Username,ph)
            st.success("Added the details of {} in Tenant".format(Username))

    def create_house():
        c.execute("Select Owner_ID from Owner")
        data=c.fetchall()
        ownerid=[int(i[0]) for i in data]

        c.execute("Select Type_No,BHK from house_type")
        data=c.fetchall()
        type=[int(i[0]) for i in data]
        bhk=[str(i[1]) for i in data]
        House_Addr=st.text_area("House Address")
        Rent=st.number_input("Rent Cost Per Month",min_value=1000)
        HType=st.selectbox("Select the Type",zip(type,bhk))
        Owner_ID=st.selectbox("OwnerID",ownerid)
        if st.button("Submit"):
            add_data_house(House_Addr,Rent,HType[0],Owner_ID)
            st.success("Added the details of house belonging to Owner {}".format((Owner_ID)))

    def create_house_type():
        type=st.number_input("Type.No",min_value=1,step=1)
        bhk=st.text_input("Enter in this format: _ BHK")
        if st.button("Submit"):  
            add_data_house_type(type,bhk)
            st.success("Added House Type {}".format(type))

    if table=="Owner":
        create_owner()
    elif table=="Tenant":
        create_tenant()
    elif table=="House":
        create_house()
    elif table=="House_type":
        create_house_type()