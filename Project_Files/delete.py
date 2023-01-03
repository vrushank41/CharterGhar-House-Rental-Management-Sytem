import pandas as pd
import streamlit as st
from database import view_all_data,getcolumns,delete_data_owner,delete_data_tenant,delete_data_htype,delete_data_house,c


def delete(table):
    result = view_all_data(table)
    cols = [i[0] for i in getcolumns(table)]
    df = pd.DataFrame(result,columns=cols)
    if st.button("Current data"):
        st.table(df)


    def delete_owner():
        c.execute("Select Owner_ID,Username from Owner")
        data=c.fetchall()
        ownerid=[int(i[0]) for i in data]
        user=[str(i[1]) for i in data]
        selected_user=st.multiselect("Select Owners to be deleted",zip(ownerid,user))
        if len(selected_user)!=0:
            st.warning("Do you want to delete the selected owners?")
        if st.button("Submit"):
            for id in selected_user:
                delete_data_owner(id)
            st.success("Successfully deleted",icon="✅")
    def delete_tenant():
        c.execute("Select Tenant_ID,Username from Tenant")
        data=c.fetchall()
        tenantid=[int(i[0]) for i in data]
        user=[str(i[1]) for i in data]
        selected_user=st.multiselect("Select the tenants to be deleted",zip(tenantid,user))
        if len(selected_user)!=0:
            st.warning("Do you want to delete the selected tenants?")
        if st.button("Submit"):
            for id in selected_user:
                delete_data_tenant(id)
            st.success("Successfully deleted",icon="✅")
    def delete_house():
        c.execute("Select House_ID,Owner_ID from House")
        data=c.fetchall()
        houseid=[int(i[0]) for i in data]
        ownerid=[int(i[1]) for i in data]
        selected_house=st.multiselect("Select the House_ID belonging to Owner_ID that you want to delete",zip(houseid,ownerid))
        if len(selected_house)!=0:
            st.warning("Do you want to delete the selected Houses?")
        if st.button("Submit"):
            for id in selected_house:
                delete_data_house(id)
            st.success("Successfully deleted",icon="✅")         
    def delete_house_type():
        c.execute("Select Type_No,BHK from House_type")
        data=c.fetchall()
        types=[int(i[0]) for i in data]
        bhk=[str(i[1]) for i in data]
        selected_house=st.multiselect("Select the Types to be deleted",zip(types,bhk))
        if len(selected_house)!=0:
            st.warning("Do you want to delete the selected types?")
        if st.button("Submit"):
            for id in selected_house:
                delete_data_htype(id)
            st.success("Successfully deleted",icon="✅")
    

    if table=="Owner":
        delete_owner()
    elif table=="Tenant":
        delete_tenant()
    elif table=="House":
        delete_house()
    elif table=="House_type":
        delete_house_type()

                
    new_result = view_all_data(table)
    df = pd.DataFrame(new_result,columns=cols)
    if st.button("New data"):
        st.table(df) 