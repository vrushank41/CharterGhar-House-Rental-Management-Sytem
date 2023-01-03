import pandas as pd
import streamlit as st
from database import view_all_data,getcolumns,c,mydb
import datetime as dt


def update(table):
    result = view_all_data(table)
    cols = [i[0] for i in getcolumns(table)]
    df = pd.DataFrame(result,columns=cols)
    if st.button("Current data"):
        st.table(df)


    def update_owner():
        c.execute("Select Owner_ID,Username from Owner")
        data=c.fetchall()
        ownerid=[int(i[0]) for i in data]
        user=[str(i[1]) for i in data]
        selected_user=st.selectbox("Select Owner to be Updated",zip(ownerid,user))
        c.execute("SELECT * from Owner where Owner_ID={}".format(selected_user[0]))
        update_user=c.fetchone()
        st.write(update_user)
        Owner_ID = int(update_user[0])
        F_Name = update_user[1]
        L_Name = update_user[2]
        Username = update_user[3]
        Password = update_user[4]
        Owner_Addr = update_user[5]
        DOB = update_user[6]

        c.execute("SELECT Ph_No from Owner_ph where Owner_ID={}".format(Owner_ID))
        ph=c.fetchall()
        use=ph
        # st.write(len(use))
        if len(ph)==1 :
            ph=ph[0][0]
        else:
            ph=""
        # st.write(ph)

        st.subheader("Showing for OwnerID: {}".format(Owner_ID))
        col1,col2=st.columns(2)
        with col1:
            new_F_Name = st.text_input("Firstname",value=F_Name)
            new_Username = st.text_input("Username",value=Username)
            new_DOB = st.date_input("DOB",value=DOB,
                min_value=dt.datetime.today() - dt.timedelta(days=10000),
                max_value=dt.datetime.today())
            new_ph=st.text_input("Ph.No",value=ph)
        with col2:
            new_L_Name = st.text_input("Lastname",value=L_Name)
            new_Password = st.text_input("Password",type="password",value=Password)
            new_Owner_Addr = st.text_area("Address",value=Owner_Addr)
        if st.button("Submit"):
            c.execute("UPDATE Owner SET F_Name=%s, L_Name=%s, Username=%s, Password=%s, DOB=%s, Owner_Addr=%s WHERE "
              "F_Name=%s and L_Name=%s and Username=%s and Password=%s and DOB=%s and Owner_Addr=%s", (new_F_Name, new_L_Name, new_Username, new_Password, new_DOB,new_Owner_Addr,F_Name,L_Name,Username,Password,DOB,Owner_Addr))
            if len(use)==1:
                c.execute("UPDATE Owner_ph SET Ph_No=%s WHERE "
                "Owner_ID=%s", (new_ph,Owner_ID))
                mydb.commit()
            else:
                c.execute("Insert into Owner_Ph values(%s,%s)",(Owner_ID,new_ph))
                mydb.commit()
            
            st.success("Successfully Updated details of {}".format(Owner_ID),icon="✅")

    def update_tenant():
        c.execute("Select Tenant_ID,Username from Tenant")
        data=c.fetchall()
        tenantid=[int(i[0]) for i in data]
        user=[str(i[1]) for i in data]
        selected_user=st.selectbox("Select Owner to be Updated",zip(tenantid,user))
        c.execute("SELECT * from Tenant where Tenant_ID={}".format(selected_user[0]))
        update_user=c.fetchone()
        st.write(update_user)
        Tenant_ID = int(update_user[0])
        F_Name = update_user[1]
        L_Name = update_user[2]
        Username = update_user[3]
        Password = update_user[4]
        Tenant_Addr = update_user[5]
        DOB = update_user[6]

        c.execute("SELECT Ph_No from Tenant_Ph where Tenant_ID={}".format(Tenant_ID))
        ph=c.fetchall()
        use=ph
        # st.write(len(use))
        if len(ph)==1 :
            ph=ph[0][0]
        else:
            ph=""
        # st.write(ph)

        st.subheader("Showing for Tenant_ID: {}".format(Tenant_ID))
        col1,col2=st.columns(2)
        with col1:
            new_F_Name = st.text_input("Firstname",value=F_Name)
            new_Username = st.text_input("Username",value=Username)
            new_DOB = st.date_input("DOB",value=DOB,
                min_value=dt.datetime.today() - dt.timedelta(days=10000),
                max_value=dt.datetime.today())
            new_ph=st.text_input("Ph.No",value=ph)
        with col2:
            new_L_Name = st.text_input("Lastname",value=L_Name)
            new_Password = st.text_input("Password",type="password",value=Password)
            new_Tenant_Addr = st.text_area("Address",value=Tenant_Addr)
        if st.button("Submit"):
            c.execute("UPDATE Tenant SET F_Name=%s, L_Name=%s, Username=%s, Password=%s, DOB=%s, Tenant_Addr=%s WHERE "
              "F_Name=%s and L_Name=%s and Username=%s and Password=%s and DOB=%s and Tenant_Addr=%s", (new_F_Name, new_L_Name, new_Username, new_Password, new_DOB,new_Tenant_Addr,F_Name,L_Name,Username,Password,DOB,Tenant_Addr))
            
            if len(use)==1:
                c.execute("UPDATE Tenant_Ph SET Ph_No=%s WHERE "
                "Tenant_ID=%s", (new_ph,Tenant_ID))
                mydb.commit()
            else:
                c.execute("Insert into Tenant_Ph values(%s,%s)",(Tenant_ID,new_ph))
                mydb.commit()
            
            st.success("Successfully Updated details of {}".format(Tenant_ID),icon="✅")
            
    def update_house():
        c.execute("Select House_ID,Owner_ID from House")
        data=c.fetchall()
        houseid=[int(i[0]) for i in data]
        ownerid=[int(i[1]) for i in data]
        selected_user=st.selectbox("Select House belonging to Owner which has to be updated",zip(houseid,ownerid))
        c.execute("SELECT * from House where House_ID={}".format(selected_user[0]))
        update_user=c.fetchone()
        st.write(update_user)
        House_ID = int(update_user[0])
        House_Addr = update_user[1]
        Htype = (update_user[2]) if update_user[2] else None
        Rent_Cost = int(update_user[3])
        Owner_ID = int(update_user[4])
        c.execute("Select Type_No from House_Type")
        types=c.fetchall()
        st.subheader("Showing for House_ID: {}".format(House_ID))
        new_House_Addr=st.text_area("House Address",value=House_Addr)
        new_Rent=st.number_input("Rent Cost Per Month",min_value=1000,value=Rent_Cost)
        new_HType=st.selectbox("Select the Type",types,index=types.index((Htype,)) if Htype else 0)
        new_Owner_ID=st.number_input("OwnerID",Owner_ID,disabled=True)
        if st.button("Submit"):
            c.execute("UPDATE House SET Rent_Cost=%s,House_Addr=%s,Htype=%s WHERE "
              "House_ID=%s", (new_Rent,new_House_Addr,int(new_HType[0]),House_ID))
            mydb.commit()
            st.success("Successfully Updated details of House_ID {}".format(House_ID),icon="✅")



    if table=="Owner":
        update_owner()
    elif table=="Tenant":
        update_tenant()
    elif table=="House":
        update_house()
        

    updated_result = view_all_data(table)
    df = pd.DataFrame(updated_result,columns=cols)
    if st.button("Updated data"):
        st.table(df)
    
