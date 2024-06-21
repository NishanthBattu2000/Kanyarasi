import streamlit as st
import math
import pandas as pd
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate('kanyarasi-b2617-f793ab6a86db.json')
    firebase_admin.initialize_app(cred)

def app():
    
    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db

    if st.session_state.username == "":
        st.write("Please login to enter data")
    else:
        a1,a2,a3 = st.columns(3)
        a2.title("Enter your Data")
        collection = [collection.id for collection in db.collections()]
        option = a2.selectbox("Create/Select Client ID",["Create","Select"])
        if option == "Create":
            client_id = a2.text_input("Client ID")
        else:
            client_id = a2.selectbox("Client ID", collection)
        c1,c2,c3,c4,c5 = st.columns(5)
        A = c1.number_input("A", value = 7.5)
        B = c2.number_input("B", value = 12)
        C = c3.number_input("C", value = 20)
        D = c4.text_input("D", value = "MAG 135")
        E = c5.number_input("E", value = 2.74)
        FaktorenNebenzeitendf = pd.DataFrame({"Faktoren Nebenzeiten": [A,B,C,D,E]})

        #st.dataframe(FaktorenNebenzeitendf)


        ###Loding manual entry items to list
        inputnames = ["lfd. Nummer / Schweißnahtnummer","position","Stk","Nahtart","Naht","Größe","stk","Länge","Lage","Blechdicke [mm]",
                    "Fugenbreite [mm]","Fugenhöhe [mm]","vdr  [m/min]","vs [cm/min]","Drahtdurch-messer [mm]","Dichte [g/cm3]",
                    "Masse Drahtelektrode [kg]","Lauflänge Draht [m]","benötigte Raupen insgeamt","benötigte Lagen Höhe","Stundensatz Schweißer [€]"]

        ###inputvalues = [ifd,Position,Stk,Nahtart,Größe,stk,Länge,Lage,Blechdicke,Fugenbreite,Fugenhöhe,vdr,vs,Drahtdurch_messer,
        ###               Dichte,Masse_Drahtelektrode,Lauflänge_Draht,benötigte_Raupen_insgeamt,benötigte_Lagen_Höhe,Stundensatz_Schweißer]


        ###Loding calculating items to list
        outputnames =["lfd. Nummer / Schweißnahtnummer","Summe m", "Schweißnaht", "Positionsnummer", "Naht1", "Nahtlänge [mm]",
                        "Nahtbreite [mm]", "vs [mm/s]", "Volumen von 1m Draht [cm3]",
                        "Masse von 1m Draht [g]", "Abschmelz- leistung [kg/h]", "Schweißzeit Einzelraupe [s]",
                        "Schweißzeit gesamt [h]", "verbrauchter SZ [kg]", "benötigte Drahtrollen",
                        "Kosten Drahtelektrode [€/kg]", "Nebenzeit [h] (30min/m)", "Schweißzeit + Nebenzeit [h]",
                        "Kosten Schweißer [€]", "Kosten SZ [€]", "Gesamtkosten [€] / Stück"]

        ###outputvalues = [ifd,Summe_m, Schweißnaht, Positionsnummer, Naht, Nahtlänge,Nahtbreite, vs1, Volumen_von_1m_Draht, Masse_von_1m_Draht,
        ###                Abschmelz_leistung, Schweißzeit_Einzelraupe, Schweißzeit_gesamt,verbrauchter_SZ, benötigte_Drahtrollen, Kosten_Drahtelektrode,
        ###                Nebenzeit, Schweißzeit_Nebenzeit, Kosten_Schweißer, Kosten_SZ,Gesamtkosten_per_Stück]

        ###Converting input items to a dataframe
        inputdf = pd.DataFrame()
        for i in range(len(inputnames)):
            if i==8:
                inputdf.insert(loc=i,column=inputnames[i],value=None,allow_duplicates=True)
            else:
                inputdf.insert(loc=i,column=inputnames[i],value=[],allow_duplicates=True)

        ###Converting inputdf to editable df
        editedinputdf = st.data_editor(inputdf,num_rows="dynamic",
                                    column_config={
                                        "Naht": st.column_config.SelectboxColumn(
                                            "Naht",
                                            options=[
                                                'Kehlnaht',
                                                'HV 40°',
                                                'HV40/15',
                                                'HV45°',
                                                'HV45°/15',
                                                'V 45°',
                                                'V60°',
                                                'Schrägen'
                                            ],
                                            required=True
                                        )
                                    })
        a=len(editedinputdf.iloc[:,0])
        outputdf = pd.DataFrame()
        for i in range(len(outputnames)):
            outputdf.insert(loc=i,column=outputnames[i],value=[0.00]*a,allow_duplicates=True)

        Submit = st.button('Submit')

        for i in range(a):
            ###Calculating the output values
            if editedinputdf.iloc[i,3] == 1:
                outputdf.iloc[i,2] = 'Kehlnaht'
            elif editedinputdf.iloc[i,3] == 2:
                outputdf.iloc[i,2] = 'HV 40°'
            elif editedinputdf.iloc[i,3] == 3:
                outputdf.iloc[i,2] = 'HV40/15'
            elif editedinputdf.iloc[i,3] == 4:
                outputdf.iloc[i,2] = 'HV45°'
            elif editedinputdf.iloc[i,3] == 5:
                outputdf.iloc[i,2] = 'HV45°/15'
            elif editedinputdf.iloc[i,3] == 6:
                outputdf.iloc[i,2] = 'V 45°'
            elif editedinputdf.iloc[i,3] == 7:
                outputdf.iloc[i,2] = 'V60°'
            elif editedinputdf.iloc[i,3] == 9:
                outputdf.iloc[i,2] = 'Schrägen'

            #outputdf.iloc[i,2] = editedinputdf.iloc[i,4]

            ### calculating the value of AC
            ###if editedinputdf.iloc[i,3] == 8 or editedinputdf.iloc[i,3] == 9:
            ###    AC = 0
            ###elif editedinputdf.iloc[i,3] < 8:
            ###    AC = 1 

            outputdf.iloc[i,1] = round(editedinputdf.iloc[i,7] * editedinputdf.iloc[i,6] * editedinputdf.iloc[i,2] * (0 if editedinputdf.iloc[i,3] == 8 or editedinputdf.iloc[i,3] == 9 else 1),2)

            outputdf.iloc[i,0] = editedinputdf.iloc[i,0]
            outputdf.iloc[i,3] = round(editedinputdf.iloc[i,1],2)
            outputdf.iloc[i,4] = round(editedinputdf.iloc[i,18],2)
            outputdf.iloc[i,5] = round(outputdf.iloc[i,1],2)
            outputdf.iloc[i,6] = round(editedinputdf.iloc[i,5],2)
            outputdf.iloc[i,7] = round((editedinputdf.iloc[i,13]*10)/60,2)
            outputdf.iloc[i,8] = round(math.pi * ((editedinputdf.iloc[i,14] / 20) ** 2.0) * 100,2)
            outputdf.iloc[i,9] = round(outputdf.iloc[i,8] * editedinputdf.iloc[i,15],2)
            outputdf.iloc[i,10] = round((outputdf.iloc[i,9] * editedinputdf.iloc[i,12] * 60) / 1000,2)
            outputdf.iloc[i,11] = round(outputdf.iloc[i,5] / outputdf.iloc[i,7],2)
            outputdf.iloc[i,12] = round(outputdf.iloc[i,11] * editedinputdf.iloc[i,18] * editedinputdf.iloc[i,19],2)
            outputdf.iloc[i,13] = round(outputdf.iloc[i,10] * outputdf.iloc[i,12],2)
            outputdf.iloc[i,14] = round(outputdf.iloc[i,13] / editedinputdf.iloc[i,16],2)
            outputdf.iloc[i,15] = round(FaktorenNebenzeitendf.iloc[4,0],2)

            if editedinputdf.iloc[i,9]<25:
                outputdf.iloc[i,16] = round((FaktorenNebenzeitendf.iloc[0,0] * editedinputdf.iloc[i,19] * editedinputdf.iloc[i,20] * outputdf.iloc[i,5]) / (60 * 1000),2)
            if editedinputdf.iloc[i,9]<50:
                outputdf.iloc[i,16] = round((FaktorenNebenzeitendf.iloc[1,0] * editedinputdf.iloc[i,19] * editedinputdf.iloc[i,20] * outputdf.iloc[i,5]) / (60 * 1000),2)
            if editedinputdf.iloc[i,9]>49.99:
                outputdf.iloc[i,16] = round((FaktorenNebenzeitendf.iloc[2,0] * editedinputdf.iloc[i,19] * editedinputdf.iloc[i,20] * outputdf.iloc[i,5]) / (60 * 1000),2)

            outputdf.iloc[i,17] = round(outputdf.iloc[i,12] + outputdf.iloc[i,16],2)
            outputdf.iloc[i,18] = round(editedinputdf.iloc[i,20] * outputdf.iloc[i,17],2)
            outputdf.iloc[i,19] = round(outputdf.iloc[i,15] * outputdf.iloc[i,14] * editedinputdf.iloc[i,15],2)
            outputdf.iloc[i,20] = round(outputdf.iloc[i,18] + outputdf.iloc[i,19],2)
        if Submit:
            st.write(outputdf)
            for i in range(a):
                info = db.collection(client_id).document(str(editedinputdf.iloc[i,0])).get()
                if info.exists:
                    st.warning("Data already exists on this ID")
                    break
                else:
                    data = {}
                    for j in range(len(editedinputdf.iloc[i,:])):
                        data[inputnames[j]] = str(editedinputdf.iloc[i,j])
                    for j in range(1,len(outputdf.iloc[i])):
                        data[outputnames[j]] = str(outputdf.iloc[i,j])
                    db.collection(client_id).document(str(editedinputdf.iloc[i,0])).set(data)
                st.success("Data uploaded")
                        