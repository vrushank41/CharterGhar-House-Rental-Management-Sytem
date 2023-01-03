import streamlit as st
import extra_streamlit_components as stx
import pandas as pd
from database import payment,con_pay,c,mydb
from database import contract,getcolumns,view_all_data
import datetime as dt


def newcontract(ten_id):
    result = view_all_data('Contract')
    cols = [i[0] for i in getcolumns('Contract')]
    df = pd.DataFrame(result,columns=cols)
    if st.button("Current data"):
        st.table(df)
    if "Tenant_ID" in st.session_state:
        c.execute("SELECT House_ID,House_Addr,Rent_Cost,Owner_ID from House")
        data=c.fetchall()
        houseid=[int(i[0]) for i in data]
        houseaddr=[i[1] for i in data]
        rentcost=[int(i[2]) for i in data]
        ownerid=[int(i[3]) for i in data]
        
        Tenant_ID = st.text_input("Tenant_ID",value=ten_id,disabled=True)
        House_ID = st.selectbox("Select Houses belonging to respective owners",zip(houseid,houseaddr,ownerid,rentcost))
        Start_date=st.date_input("Start Date(max 2 weeks)",value=dt.datetime.today(),min_value=dt.datetime.today(),
                max_value=dt.datetime.today() + dt.timedelta(days=14))
        Duration = st.number_input("Enter the months",min_value=1)

        Rent_Cost_Duration=Duration*House_ID[3] 
        Rent_Cost_Duration=st.number_input("Total Rent",value=Rent_Cost_Duration,disabled=True)   

        if st.button("Submit"):
            c.execute("INSERT into contract(Start_Date,Duration,Rent_Cost_Duration,Owner_Id,Tenant_Id,House_Id) values(%s,%s,totalrent({},{}),%s,%s,%s)".format(Duration,House_ID[3]),(Start_date,Duration,int(House_ID[2]),Tenant_ID,int(House_ID[0]) ))
            c.execute('Update Tenant set Status={},Tenant_Addr="{}" where Tenant_ID={}'.format(1,House_ID[1],Tenant_ID))
            mydb.commit()
            st.success("Tenant_Id {} gets into the contract✅".format(Tenant_ID))
            c.execute("Select * from Contract_save")
            res=c.fetchall()
            st.table(pd.DataFrame(res, columns=[col[0] for col in c.description]))
    new_result = view_all_data('Contract')
    df = pd.DataFrame(new_result,columns=cols)
    if st.button("New data"):
        st.table(df)
    
    


    



def showconpay(ten_id):
    if "Tenant_ID" in st.session_state:
        result1 = view_all_data('Contract')
        cols1 = [i[0] for i in getcolumns("Contract")]
        df = pd.DataFrame(result1,columns=cols1)
        if st.button("Show all contracts"):
            st.table(df)
        c.execute("SELECT Contract_ID from Contract")
        data=c.fetchall()
        contractid=[int(i[0]) for i in data]
        
        selected_con=st.multiselect("Select Contract_Id to get the complete details",contractid)
        result2 = view_all_data('Payment')
        cols2 = [i[0] for i in getcolumns("Payment")]
        use=cols1+cols2
        del use[11]
        del use[11]
        # st.write(use)

        for con in selected_con:
            c.execute("Select Contract.Contract_ID,Contract.Start_Date,Contract.Duration,Contract.Rent_Cost_Duration,Contract.Owner_ID,Contract.Tenant_ID,Contract.House_ID,Payment.Payment_ID,Payment.Pay_From,Payment.Payment_Date,Payment.Amount from Contract inner join Payment on Contract.Contract_ID=Payment.Contract_ID where Contract.Contract_ID={}".format(con))
            data=c.fetchall()
            df = pd.DataFrame(data,columns=use)
            st.table(df)
            c.execute("select start_date from Contract where Contract_ID={}".format(con))
            start=c.fetchone()
            start=start[0]
            c.execute("select duration from Contract where Contract_ID={}".format(con))
            duration=c.fetchone()
            duration=int(duration[0])
            args=[start,duration,0]
            ans=c.callproc('end_date_calc',args)
            st.info("This contract ends on {}".format(ans[2]))
            

            


def showpayments(ten_id):

    if "Tenant_ID" in st.session_state:

        result = view_all_data('Payment')
        cols = [i[0] for i in getcolumns("Payment")]
        df = pd.DataFrame(result,columns=cols)
        if st.button("Show all Payments"):
            st.table(df)
        with st.expander("New Payment"):
            Tenant_ID=st.number_input('Tenant_ID',value=ten_id,disabled=True)
            c.execute("SELECT Contract_ID from Contract where Tenant_ID={}".format(Tenant_ID))
            data=c.fetchall()
            contractid=[int(i[0]) for i in data]
            selected_con=st.selectbox("Select Contract_Id to make payment",contractid)
            if selected_con:
                Contract_ID=st.number_input('Contract_ID',value=selected_con,disabled=True)
                Pay_From=st.text_input("Enter name of Payee",max_chars=50)
                Payment_Date=st.date_input("Date of Payment",value=dt.datetime.today(),
                    min_value=dt.datetime.today(),
                    max_value=dt.datetime.today())
                
                c.execute('Select Rent_Cost_Duration from Contract where Contract_ID={}'.format(Contract_ID))
                totalrent=c.fetchone()
                totalrent=int(totalrent[0])

                Amount=st.number_input("Amount shouldn't exceed the total rent cost {})".format(totalrent),min_value=500)
            else:
                st.warning("The selected Tenant doesn't hold a Contract")

            c.execute("drop trigger if exists amount_exceed")
            qrystr = ("""CREATE TRIGGER amount_exceed AFTER INSERT ON Payment FOR EACH ROW BEGIN IF (select sum(Amount)+new.Amount from Payment where Contract_ID={}) > {} THEN SIGNAL SQLSTATE '45000' SET message_text="Amount can't exceed total Rent Cost";END IF;END""".format(Contract_ID,totalrent))
            c.execute(qrystr)
            mydb.commit()

            if st.button("Submit"):               
                c.execute('INSERT INTO Payment(Contract_ID,Tenant_ID, Pay_From, Payment_Date, Amount) VALUES (%s,%s,%s,%s,%s)',
                    (Contract_ID,Tenant_ID, Pay_From, Payment_Date, Amount))
                mydb.commit()
                st.success("💲Payment of Rs.{} Done💲✅".format(Amount))
            
        if st.button("ALL Payments of each Contract"):
            # result1 = view_all_data('Contract')
            cols1 = [i[0] for i in getcolumns("Contract")]
            # result2 = view_all_data('Payment')
            cols2 = [i[0] for i in getcolumns("Payment")]
            use=cols1+cols2
            del use[11]
            del use[11]
            del use[8]
            del use[8]
            use[7]="No.of Payments"
            use.append("Amount Left")
            c.execute("Select Contract.Contract_ID,Contract.Start_Date,Contract.Duration,Contract.Rent_Cost_Duration,Contract.Owner_ID,Contract.Tenant_ID,Contract.House_ID,count(Payment.Payment_ID),sum(Payment.Amount),rent_remain(sum(Payment.Amount),Rent_Cost_Duration) from Contract inner join Payment on Contract.Contract_ID=Payment.Contract_ID group by Contract_ID")
            data=c.fetchall()
            df = pd.DataFrame(data,columns=use)
            st.table(df)
                

            



def delcontract(ten_id):
    result = view_all_data('Contract')
    cols = [i[0] for i in getcolumns('Contract')]
    df = pd.DataFrame(result,columns=cols)
    if st.button("Current data"):
        st.table(df)
    if "Tenant_ID" in st.session_state:
        c.execute("Select Contract_ID,Tenant_ID from Contract")
        data=c.fetchall()
        contractid=[int(i[0]) for i in data]
        tenantid=[int(i[1]) for i in data]
        selected_contract=st.selectbox("Select the Contract belonging to Tenant to delete",zip(contractid,tenantid))
        if len(selected_contract)!=0:
            st.warning("Do you want to delete the selected contract record?")
        if st.button("Submit"):
            c.execute("Delete from Contract where Contract_ID={}".format(selected_contract[0]))
            c.execute('Update Tenant set Status={},Tenant_Addr="{}" where Tenant_ID={}'.format(0,None,selected_contract[1]))
            mydb.commit()
            st.success("Successfully deleted",icon="✅")
    
    new_result = view_all_data('Contract')
    df = pd.DataFrame(new_result,columns=cols)
    if st.button("New data"):
        st.table(df)



def login():
    c.execute("SELECT Tenant_ID from Tenant")
    data=c.fetchall()
    tenantid=[int(i[0]) for i in data]
    selected_tenant=st.selectbox("Select Tenant_ID to Login",tenantid)
    return selected_tenant
    
def application():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="tab1", title="NEW CONTRACT", description="Tenant,Owner gets into contract"),
        stx.TabBarItemData(id="tab2", title="SHOW CONTRACT AND ITS PAYMENTS", description="Showing payments related to that Contract_ID"),
        stx.TabBarItemData(id="tab3", title="ALL PAYMENTS", description="Each and every payment"),
        stx.TabBarItemData(id="tab4", title="DELETE CONTRACT", description="Clear contract details")])
    Tenant_ID=login()
    if "Tenant_ID" not in st.session_state:
        st.session_state["Tenant_ID"]=Tenant_ID
    
    placeholder = st.container()

    if chosen_id == "tab1":
        newcontract(Tenant_ID)

    elif chosen_id == "tab2":
        showconpay(Tenant_ID)

    elif chosen_id == "tab3":
        showpayments(Tenant_ID)
    elif chosen_id == "tab4":
        delcontract(Tenant_ID)

    else:
        placeholder = st.empty()
    
    
