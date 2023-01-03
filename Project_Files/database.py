import mysql.connector
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="house_rental"
)
c = mydb.cursor(buffered=True)


def show_tables():
    c.execute("show tables")
    data = c.fetchall()
    return data

def add_data_owner(F_Name,L_Name, Username, Password, Owner_Addr,DOB):
    c.execute('INSERT INTO Owner(F_Name,L_Name, Username, Password, Owner_Addr,DOB) VALUES (%s,%s,%s,%s,%s,%s)',
              (F_Name,L_Name, Username, Password, Owner_Addr,DOB))
    mydb.commit()
def add_data_oph(Username,Ph_No):
    c.execute('Select Owner_ID from Owner where Username="{}"'.format(Username))
    ids=c.fetchone()
    c.execute('INSERT into Owner_ph VALUES (%s,%s)',( int(ids[0]) , Ph_No))
    mydb.commit()

def add_data_tenant(F_Name,L_Name, Username, Password, Tenant_Addr,DOB):
    c.execute('INSERT INTO Tenant(F_Name,L_Name, Username, Password, Tenant_Addr,DOB) VALUES (%s,%s,%s,%s,%s,%s)',
              (F_Name,L_Name, Username, Password, Tenant_Addr,DOB))
    mydb.commit()
def add_data_tph(Username,Ph_No):
    c.execute('Select Tenant_ID from Tenant where Username="{}"'.format(Username))
    ids=c.fetchone() 
    c.execute('INSERT into Tenant_Ph VALUES (%s,%s)',(int(ids[0]) , Ph_No))
    mydb.commit()

def add_data_house(House_Addr,Rent,Htype,Owner_Id):
    c.execute('INSERT INTO House(House_Addr,Htype,Rent_Cost,Owner_ID) VALUES (%s,%s,%s,%s)',
              (House_Addr,Htype,Rent,Owner_Id))
    mydb.commit()
def add_data_house_type(type,bhk):
    c.execute('INSERT INTO House_type(Type_No,BHK) VALUES (%s,%s)',
              (type,bhk))
    mydb.commit()

def getcolumns(table):
    c.execute('desc {}'.format(table))
    data = c.fetchall()
    return data

def view_all_data(table):
    c.execute('SELECT * FROM {}'.format(table))
    data = c.fetchall()
    return data

def delete_data_owner(id):
    c.execute("DELETE from Owner where Owner_ID={}".format(id[0]))
    mydb.commit()

def delete_data_tenant(id):
    c.execute("DELETE from Tenant where Tenant_ID={}".format(id[0]))
    mydb.commit()

def delete_data_htype(id):
    c.execute("DELETE from House_type where Type_No={}".format(id[0]))
    mydb.commit()

def delete_data_house(id):
    c.execute("DELETE from House where House_ID={}".format(id[0]))
    mydb.commit()

def ExecuteManualQuery(query):
    str(query).replace(";", '')
    if "select" in str(query).lower():
        c.execute(query)
        res = c.fetchall()
        # st.write(c.description)
        st.table(pd.DataFrame(res, columns=[col[0] for col in c.description]))

    elif "insert" in str(query).lower():
        c.execute(query)
        res = c.fetchall()
        st.success(f'inserted successfully with id {c.lastrowid}', icon="✅")
        mydb.commit()
        # st.table(pd.DataFrame(res, columns=[col[0] for col in c.description]))

    elif "update" in str(query).lower():
        c.execute(query)
        res = c.fetchall()
        st.success(f'updated successfully', icon="✅")
        mydb.commit()
        # st.table(pd.DataFrame(res, columns=[col[0] for col in c.description]))

    elif "delete" in str(query).lower():
        c.execute(query)
        res = c.fetchall()
        st.success(f'deleted successfully', icon="✅")
        mydb.commit()
        # st.table(pd.DataFrame(res, columns=[col[0] for col in c.description]))



def payment():
    c.execute('SELECT * FROM Payment')
    data = c.fetchall()
    return data
def contract():
    c.execute('SELECT * FROM Contract')
    data = c.fetchall()
    return data
def con_pay():
    c.execute('SELECT * from Contract inner join Payment on Contract.contract_id=Payment.contract_id')
    data=c.fetchall()
    return data




