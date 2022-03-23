from uuid import uuid4

from nordigen import NordigenClient

import streamlit as st
import requests

#
token = st.secrets["TOKEN"]
client = NordigenClient(secret_id=st.secrets["SECRET"],
                        secret_key=token
                        )
token_data = client.generate_token()
st.write("token: ", token)
new_token = client.exchange_token(token_data["refresh"])
# Get institution id by bank name and country
# institution_id = client.institution.get_institution_id_by_name(
#    country="IT",
#    institution="Unicredit"
# )
institution_id = "SANDBOXFINANCE_SFIN0000"
st.write("institution_id: ", institution_id)
# Initialize bank session
ref_id = str(uuid4())
st.write("ref_id: ", ref_id)
init = client.initialize_session(
    # institution id
    institution_id=institution_id,
    # redirect url after successful authentication
    redirect_uri="https://share.streamlit.io/fpini/pythonnordige/pyTHONNordige/bank01.py",
    #    redirect_uri="https://localhost:8501",
    # additional layer of unique ID defined by you
    reference_id=ref_id
)

st.write("init", init)
# Get requisition_id and link to initiate authorization process with a bank
link = init.link  # bank authorization link
st.write("link: ", link)

if st.button("Go on"):
    requisition_id = init.requisition_id
    st.write("init 1 ", init)
    st.write("ref_id_2: ", ref_id)
    # Get account id after you have completed authorization with a bank
    # requisition_id can be gathered from initialize_session response
    accounts = client.requisition.get_requisition_by_id(
        requisition_id=init.requisition_id
    )
    st.write("accounts :", accounts)
    st.write(type(accounts))
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )

    # Create account instance and provide your account id from previous step
    account = client.account_api(id=account_id)

    # Fetch account metadata
    meta_data = account.get_metadata()
    st.write("metadata: ", meta_data)
    st.write(type(meta_data))
    # Fetch details
    details = account.get_details()
    st.write("details :", details)
    st.write(type(details))
    # Fetch balances
    balances = account.get_balances()
    st.write("balances :", balances)
    st.write(type(balances))
    # Fetch transactions
    transactions = account.get_transactions()
    # Filter transactions by specific date range
    transactions = account.get_transactions(date_from="2022-01-01", date_to="2022-01-21")
    st.write("transactions :", transactionss)
    st.write(type(transactions))
    st.write("end")
