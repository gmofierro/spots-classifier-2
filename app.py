import csv
from os import path
#from io import BytesIO
import streamlit as st
from streamlit_option_menu import option_menu
#from dev import *
from spots_classifier import SpotsClassifier
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Spots Classifier", layout="wide")

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
        
    # guarda el archivo
    
    
        
    return uploaded_file

def export_file():    
    ##df.to_excel('df_test3.xlsx')
    #file_name = file.to_excel('df_test3.xlsx')
        #with open('CONCENTRADO TV AZTECA MAYO FINAL.xlsx', "rb") as template_file:
    
    
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        if path.exists("./data/df_test3_sinN.xlsx"):
            with open('./data/df_test3_sinN.xlsx', "rb") as template_file:
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
            
            df_uploaded = pd.read_excel(uploaded_file)
            
            path_file = "./data/" + file_name
            df_uploaded.to_excel(path_file, sheet_name="Hoja1")
            
            st.write('Se guardó el archivo')
            
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
            
            err = clasificador.f_errors()
            if err > 0:
                st.write('El archivo de logs..')
                with  open('./data/_spots_analizer.log','r') as file:
                    st.write(file.readlines())    
            
            
            #df_xlsx = to_excel(df_test3)
        else: 
            st.write('revise el archivo de excel con el registro de eventos ..')
    
        st.write('---')
    return   

def mostrar_tarifas_actuales():
    
    c30, c31 = st.columns([8,1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        st.write('---')
        st.write('Las tarifas actuales ..')
        
        filename_plazas_tarifas = "./data/" + "Tarifas2024_4_Actualizado.xlsx"
        df_tx = pd.read_excel(filename_plazas_tarifas, sheet_name='PLAZAS_TARIFAS')
        
        #df_tx1 = df_tx[['ID', 'CANAL', 'CIUDAD', 'TARIFA', 'TELEVISORA', 'HORARIO', 'DIA']]
        #df_vista = df_tx[['CIUDAD',  'CANAL', 'TELEVISORA' ,'HORARIO', 'TARIFA', 'PERIODO', 'CIUDAD_CANAL', 'ALIAS_1_CANAL']]
        df_vista =df_tx[['PLAZA',  'CANAL', 'TELEVISORA' ,'HORARIO', 'TARIFA']] 
        
        #df_formato = df_vista.style.format({"PLAZA" : "{      }  -PLAZA-  ",  "CANAL" : "  - CANAL -  ", "TELEVISORA" : "  -  TELEVISORA -  ", "HORARIO" : "  -  HORARIO -  ", "TARIFA" : "  -  TARIFA -  "})
        
        st.dataframe(df_vista, width=450, use_container_width=True)
        #st.dataframe(df_formato)
        
        st.write(df_vista)
        
        st.write('---')

        #st.write('Las tarifas Nacionales ..')
        
        #df_nacional = pd.read_excel(filename_plazas_tarifas, sheet_name='TARIFAS_NACIONALES')
        
        #st.dataframe(df_nacional)

def mostrar_log_eventos():
    filename_log = ".data/_spots_analizer.log"
    if path.exists(filename_log) :
        df_log = pd.read_excel(filename_log, sheet_name='Hoja1')
        if len(df_log) > 0:  
            st.write(df_log)       
        else:           
            st.write('No hubo eventos de log..')
   


def reporte_anunciantes_televisora():
    
    c30, c31 = st.columns([10,1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        
        ruta = "./data/"
        
        ##st.write('---')
        ##st.write('Reporte: Anunciantes por Televisora ..')
        
        filename_anunciantes = ruta + "df_test3_sinN.xlsx"
        df_anunciantes = pd.read_excel(filename_anunciantes, sheet_name='Sheet1')
        df_anunciantes_2 =df_anunciantes[['CANAL', 'MARCA', 'SELECCIÓN', 'TARIFA']] 
        
        filename_plazas_tarifas = ruta + "Tarifas2024_4_Actualizado.xlsx"
        df_televisora_canal = pd.read_excel(filename_plazas_tarifas, sheet_name='TELEVISORA_CANAL')
        #print(df_televisora_canal)

        #df_televisora_canal.set_index(['ALIAS_CANAL']) 
        
        ## La union de estos dos Dataframes produce la salida del resultado
        ## de los ANUNCIANTES (MARCAS) por TELEVISORA
        
        ##  st.dataframe(df_anunciantes_2)  
        ##  st.dataframe(df_televisora_canal)

        # st.write('-- OK ---')
        ## sample df.set_index("key").join(other.set_index("key"))
        ## Se realiza el JOIN
        df_res = df_anunciantes_2.set_index(["CANAL"]).join(df_televisora_canal.set_index(['ALIAS_CANAL'])) 

        ## st.write(' --  TODOS LOS Eventos Registrados Para las Televisoras  ----')
        df_vista = df_res 
        
        df_vista2= df_res.groupby(['TELEVISORA', 'MARCA'], as_index = False).nunique() #['MARCA']
        
        
        df_vista3 = df_vista2[['TELEVISORA', 'MARCA']]
        
        
        st.write(' ---  ANUNCIANTES POR TELEVISORA  ---')
        st.dataframe(df_vista3, width=450, use_container_width=False)
        
        
        st.write('---')        
        st.write('---Cantidad de Anunciantes por Televisora -- ')
        
        df_cuantas_marcas_por_televisora= df_res.groupby(['TELEVISORA'], as_index = True)['MARCA'].nunique() #.count() 

        st.dataframe(df_cuantas_marcas_por_televisora)
            #pie_chart = px.pie(df_cuantas_marcas_por_televisora, 
            #               title = 'Cantidad de anunciantes por Televisora',
            #               values = 'MARCA',
            #               names = 'MARCA')
            #                
            #st.plotly_chart(pie_chart)          
        
         
         
        df_suma_tarifa= df_res.groupby(['TELEVISORA'], as_index = False).sum(['TARIFA'])
        
        st.write('---')
        st.write('--- MONTOS POR TELEVISORA ---')
        st.dataframe(df_suma_tarifa)

               
        ## primer SALIDA -- Todos los eventos por Televisora
        
        st.write('---')
        st.write(' --  TODOS LOS EVENTOS REGISTRADOS  ----')
        st.dataframe(df_vista, width=450, use_container_width=True)
        #st.dataframe(df_formato)
        
        #st.write(df_vista)
        ## st.write(' --  GROUP BY ----')
        ## st.dataframe(df_vista2, width=450, use_container_width=False)
        #st.dataframe(df_formato)
        
        #st.write(df_vista2)
        
        st.write('---')

        #st.write('Las tarifas Nacionales ..')
        
        #df_nacional = pd.read_excel(filename_plazas_tarifas, sheet_name='TARIFAS_NACIONALES')
        
        #st.dataframe(df_nacional)

##
##
##  INICIA EL MENU DE LA APLICACION
##
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Show Tarifas File','Run process', 'Download Result File', 'Anunciantes x Televisora'], 
        icons=['house', 'gear', 'play', 'play', 'play'], menu_icon="cast", default_index=0)
    selected
    
if selected == 'Show Tarifas File':
    mostrar_tarifas_actuales()    
    
if selected == 'Run process':
    with st.spinner('Wait for it...'):
        df = analice()    ## incluye cargar el archivo
    st.success('Done!')  

    mostrar_log_eventos()
    
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

if selected == 'Anunciantes x Televisora':
    c30, c31 = st.columns([8, 1]) # 3 columnas: 10%, 60%, 10%
    with c30:
        st.subheader('Reporte de los Anunciantes por televisora')
        #st.write('Reporte de los Anunciantes por televisora')
        #st.write('')
        # del dataframe df_test3_sin_N hacer un join con CANALES-TELEVISORA a través de los campos
        # df_test3_sin_N(CANAL) y df_canales_televisora(ALIAS_CANAL) 
        # PRIMERO deben establecer el índice a ALIAS_CANAL en canales_TELEVISORAS..
        # La ventaja de hacerlo con DataFrames es que aun no se necesita la conexión a la BD 
        # 
        
        reporte_anunciantes_televisora()    
        
        st.write('---')
        # Bloque 2



