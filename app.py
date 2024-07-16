import csv
from os import path
#from io import BytesIO
import streamlit as st
from streamlit_option_menu import option_menu
#from dev import *
from spots_classifier import SpotsClassifier
import pandas as pd

st.set_page_config(page_title="Page Title", layout="wide")

#st.set_page_config(page_icon="📊", page_title=" -- Spots Classifier -- !", layout="wide")
st.image("./images/imagen_portada.png", width=200)
## st.image("imagen_portada.png", width=200)
st.title("Determinación del alcance y tarifas de anuncios de TV")

#df_test3 = pd.DataFrame()


def load_file():        
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        # Bloque 1
        uploaded_file = st.file_uploader(
            label="Spots"
            "", type = 'xlsx',
            key="1",
        )
        
    return uploaded_file

def export_file():    
    ##df.to_excel('df_test3.xlsx')
    #file_name = file.to_excel('df_test3.xlsx')
        #with open('CONCENTRADO TV AZTECA MAYO FINAL.xlsx', "rb") as template_file:
    
    
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        if path.exists("df_test3.xlsx"):
            with open('df_test3.xlsx', "rb") as template_file:
                template_byte = template_file.read()
                st.download_button(label="Click to Download Template File", data=template_byte, file_name="template.xlsx", mime='application/octet-stream')  
        else: 
            st.write('First Run Process..')
        return 0


def analice():
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        uploaded_file = load_file()
        if uploaded_file is not None:
            file_name = uploaded_file.name
            st.write(f'file: {file_name}')

            # Bloque 2a
            info_box_wait = st.info('Realizando la clasificación...', icon="ℹ️")
            
            file_name = uploaded_file.name
            
            #st.write(f'file: {file_name}')
            
            clasificador = SpotsClassifier(file_name)
    
            clasificador.initial_configuration()

            st.write('Actualizando el alcance ..')
            if clasificador.actualiza_alcance_eventos() == 0:
                st.write('Actualización del alcance OK..')

            ## Se tiene en df_test3 los registros con el ALCANCE ya determinado
            ## Una vez que ya se determinó el ALCANCE se hace la..
            ## Implementación para cálculo de las tarifas 
            
            st.write('Iniciando la actualización de las tarifas... espere')

            clasificador.configurar_archivos_para_tarifas() ## se lee el archivo de excel con la tarifas por sede y los canales por Sede

            clasificador.actualiza_tarifa()
            
            st.write('Se concluyó la actualización de las tarifas')

            st.write('Process terminado! Puede descargar el archivo actualizado')
            st.write('---')

            clasificador.export_to_excel()
            
            #df_xlsx = to_excel(df_test3)
        else: 
            st.write('Suba el archivo de excel ..')
            
        
        st.write('---')
    return   

def mostrar_tarifas_actuales():
    st.write('---')
    st.write('Las tarifas actuales ..')
    
    filename_plazas_tarifas = "./data/" + "tarifas_GFM.xlsx"
    df_tx = pd.read_excel(filename_plazas_tarifas, sheet_name='PLAZAS_TARIFAS')
    
    st.dataframe(df_tx)
    
    st.write('---')

    st.write('Las tarifas Nacionales ..')
    
    df_nacional = pd.read_excel(filename_plazas_tarifas, sheet_name='TARIFAS_NACIONALES')
    
    st.dataframe(df_nacional)

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Show Tarifas File','Run process', 'Download Result File'], 
        icons=['house', 'gear', 'play', 'play'], menu_icon="cast", default_index=0)
    selected
    
if selected == 'Show Tarifas File':
    mostrar_tarifas_actuales()    
    
if selected == 'Run process':
        df = analice()    ## incluye cargar el archivo
        #GFM_1 export_file()
        # Bloque 2

if selected == 'Download Result File':
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        st.write('')
        st.write('')
        export_file()
        st.write('---')
        # Bloque 2



