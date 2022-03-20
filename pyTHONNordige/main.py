import streamlit as st
# from streamlit_folium import folium_static
# import folium
# from folium import plugins
import pandas as pd
from nordigen import NordigenClient
import requests
# from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder
import altair as alt
import io


def read_wb_country(iso2code):
        WB_COUNTRIES_ENDPOINT = 'https://api.worldbank.org/v2/country/' + iso2code + '?format=json'
        r = requests.get(WB_COUNTRIES_ENDPOINT).json()
        return pd.DataFrame(r[len(r)-1])

def create_df_Country_institutions(iso2code):
        institutions = client.institution.get_institutions(iso2code)
        df_institutions = pd.DataFrame.from_dict(institutions)
        df_wb_country = read_wb_country(iso2code)
        latitude = float(df_wb_country['latitude'][0])
        longitude = float(df_wb_country['longitude'][0])
        df_institutions = df_institutions.assign(lat=latitude)
        df_institutions = df_institutions.assign(lon=longitude)
        df_institutions = df_institutions.assign(countryname=df_wb_country['name'][0])
        return df_institutions


st.set_page_config(layout='wide')
st.title("Nordigen Institutions")

countries = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU",
             "IE", "IS", "IT", "LV", "LT", "LI", "LU", "MT", "NL", "NO", "PL", "PT", "RO", "SK",
             "SI", "ES", "SE", "UK"]
# df_biclei = pd.read_csv(r'C:\Users\pinizzot\Downloads\bic_lei_gleif_v1_monthly_full_20220225.csv')
url = "https://raw.githubusercontent.com/Fpini/pyTHONNordige/master/pyTHONNordige/bic_lei_gleif_v1_monthly_full_20220225.csv"  # Make sure the url is the raw version of the file on GitHub
download = requests.get(url).content
# Reading the downloaded content and turning it into a pandas dataframe
df_biclei = pd.read_csv(io.StringIO(download.decode('utf-8')))

with st.sidebar.form("Sidebar form"):
        options = st.multiselect("Countries", countries, default="BE")
        sb_Country = st.form_submit_button("Submit")
        token = st.secrets["TOKEN"]
        client = NordigenClient(secret_id=st.secrets["SECRET"],
                                secret_key=token
                                )

        token_data = client.generate_token()
        # Use existing token
        # client.token = token
        new_token = client.exchange_token(token_data["refresh"])

        # Get all institution by providing country code in ISO 3166 format
        #country = "IT"
        df_global = []
        flg=0


        for country in options:
                df_institutions = create_df_Country_institutions(country)
                if flg == 0:
                        df_global = df_institutions
                        flg = 1
                else:
                        df_global = pd.concat([df_global, df_institutions], ignore_index=True)
                # Exchange refresh token for new access token
                new_token = client.exchange_token(token_data["refresh"])

# st.write("Number of selected institutions:", str(df_global.shape[0]) )
# longitude=df_global['lat'][0]
# latitude=df_global['lon'][0]
#
# m = folium.Map(location=[longitude, latitude],tiles='CartoDB dark_matter',zoom_start=1)
# marker_cluster = plugins.MarkerCluster().add_to(m)
# for i in range(df_global.shape[0]):
#         folium.Marker(
#                 [df_global['lat'][i],df_global['lon'][i]],tooltip =df_global['name'][i]).add_to(marker_cluster)
# folium_static(m)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# urllogo=df_global['logo'][0]
# im = Image.open(requests.get(urllogo, stream=True).raw)
# im=im.resize((64,64), Image.ANTIALIAS)
# st.image(im, caption=df_global['name'][0])

for i in range(df_global.shape[0]):
        bicvalue = df_global['bic'][i]
        if len(df_global['bic'][i]) == 8:
                df_global.loc[i, 'bic'] = bicvalue + 'XXX'
df_global = df_global.merge(df_biclei, left_on='bic', right_on='BIC', how='left')
#
gb = GridOptionsBuilder.from_dataframe(df_global)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True)
gridOptions = gb.build()
AgGrid(df_global, gridOptions=gridOptions, enable_enterprise_modules=True)
#
s = df_global.groupby(['countryname'])['countryname'].count()
source = pd.DataFrame({
        'a': options,
        'b': s})
c = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b')

st.altair_chart(c)
