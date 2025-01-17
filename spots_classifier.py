import pandas as pd
import numpy as np
from datetime import datetime

class SpotsClassifier:
  def __init__(self, cadena):
    self.lista_nacionales=[]
    self.lista_asociados=[]
    self.lista_locales=[]

    self.df_test = pd.DataFrame() 
    self.df_test3 = pd.DataFrame()
    self.df_spots_fecha_ordenado = pd.DataFrame()
    self.df_canales_nacionales = pd.DataFrame()
    self.df_canales_asociados = pd.DataFrame()
    self.df_canales_locales = pd.DataFrame()
    

    #ruta = "/content/drive/MyDrive/proy_anun/"
    self.ruta = "./data/"  #dev\utils\spots_classifier.py
    self.errors = 0

    ## self.fileName = self.ruta + "CONCENTRADO TV AZTECA MAYO FINAL_GFM_4000.xlsx"

    self.fileName = self.ruta + cadena
 
    ## para obtener las tarifas
    self.df_tarifas = pd.DataFrame()   # El Dataframe para recuperar las tarifas por plazas
    self.df_plazas_canales = pd.DataFrame()   # El Dataframe para recuerar las los canales por plazas
    self.df_tarifas_nacionales = pd.DataFrame()  # El Dataframe para recuperar las tarifas nacionales

    
    #self.fileName = cadena
    #self.file_log = '_spots_analizer.log'     ## Archivo de logs
    self.file_log = open('./data/_spots_analizer.log','w+')

  def initial_configuration(self):

    df = pd.read_excel(self.fileName, sheet_name='Hoja1')
    self.df_test = df

    self.configura_db_test_fechas()
  
    self.filtra_df_spots()

    self.ordenar_spots_fecha()

    # archivo de logs
    #self.file_log = open('_spots_analizer.log','w+')
    

    return 0

  def print_initial_condition():
    #GFM print(self.fileName)
    #GFM print(self.lista_nacionales)
    #GFM print(self.lista_asociados)
    #GFM print(self.lista_locales)
    
    
    #print(self.df_test3)
    #GFM print (self.df_spots_fecha_ordenado)
    ## print(self.df_canales_nacionales)

    return 0


  def f_errors(self):
    return self.errors

  def write_a_log_reg(self, reg):
    #file_log = open('./data/_spots_analizer.log','a')
    
    f1 = datetime.now()
    self.file_log.write(f'event: {reg}\n')
    ##self.file_log.write('---------\n')
    self.errors = self.errors + 1 
    #self.file_log.close()
    return 0
  
  def configura_db_test_fechas(self):
    self.df_test['FECHA_NEW'] = self.df_test.FECHA.astype(str) + " " + self.df_test.HORA.astype(str)
    # convert the 'Date' column to datetime format -- usando la funcio datetime de pandas

    self.df_test['FECHA_NEW'] = pd.to_datetime(self.df_test['FECHA_NEW'], format='mixed')

    self.df_test2 = pd.DataFrame(self.df_test.DURACION.str.split(':').tolist(), columns = ['dur_min','dur_seg'])
    #dfq1['new'] = dfq1['DURACION'].str[3:5]

    self.df_test2['dur_min'] = self.df_test2['dur_min'].astype(int)*1
    self.df_test2['dur_seg'] = self.df_test2['dur_seg'].astype(int)*1

    self.df_test3 = pd.concat([self.df_test, self.df_test2], axis=1)
    #print(df_test3)

    #GFM print('Configura_fechas_OK')

    return 0 ## self.df_test3



  ## Generar un dataFrame auxiliar para manipular solo el CANAL, VERSION (Spot) y la FECHA en formato datetime
  ## Integrar en un dataset CANAL, VERSION (El Anuncio) y la FECHA COMPLETA
  ## df_test_articulos_canales_fechas

  def filtra_df_spots(self):
    df_test_spots_canales_fechas = self.df_test3[['CANAL', 'VERSION', 'FECHA_NEW']]

    ## df_spots_fecha_ordenado es el dataframe con los tres atributos ORDENADO por VERSION y FECHA_NEW

    #df_spots_fecha_ordenado = df_test_spots_canales_fechas.sort_values(['VERSION','FECHA_NEW'])

    self.df_spots_fecha_ordenado = df_test_spots_canales_fechas.sort_values(['VERSION','FECHA_NEW'])
    self.df_spots_fecha_ordenado.sort_values(['VERSION','FECHA_NEW'], ascending=True, inplace= True)


    # GFM print('OK... filtra_df-spots')
    return 0 ## df_spots_fecha_ordenado

  def ordenar_spots_fecha(self):
    df_test_spots_canales_fechas = self.df_test3[['CANAL', 'VERSION', 'FECHA_NEW']]
    #df_test_spots_canales_fechas.sort_values(['VERSION','FECHA_NEW'], ascending=True, inplace= True)
    df_test_spots_canales_fechas.sort_values(['VERSION','FECHA_NEW'], ascending=True)
    self.df_spots_fecha_ordenado = df_test_spots_canales_fechas

    return 0

  ## Definir para el calculo de la diferencia de dos fechas en segundos
  def dif_fechas_segundos_fechas(self, fecha1, fecha2):
    dif = fecha2 - fecha1
    result = dif.days * 24 * 3600 + dif.seconds
    return result

  ## Definir para el calculo de la diferencia de dos fechas en segundos integrando un margen en segundos
  def dif_fecha_con_margen_segundos_fechas(self, fecha1, fecha2, margen):
    dif = abs(fecha2 - fecha1)
    result = dif.days * 24 * 3600 + dif.seconds
    result =  result    #abs(result - margen)
    #print(result)
    return result

  def adicionar_en_lista_nacionales(self, canal, version, fecha):
    flag = 0
    reg2 = [canal, version, fecha] in self.lista_asociados

    if reg2:
      flag = 0  # ya no se hace nada .. existe en asociados..
    else:
      reg2 = [canal, version, fecha] in self.lista_nacionales
      if reg2:
        flag = 1 # entonces insertar en asociados
      else:
        self.lista_nacionales.append([canal, version, fecha])
        flag = 0      # se insertó en nacionales  NO insertar en asociados

      return flag

  def adicionar_en_lista_asociados(self, canal, version, fecha):
    out = 0
    reg2 = [canal, version, fecha] in self.lista_asociados
    if not reg2:
      self.lista_asociados.append([canal, version, fecha])
      out = 1
    else:
      out = -1 

    return out

  def adicionar_en_lista_nacionales_v2(self, canal, version, fecha):
    out = 0
    reg2 = [canal, version, fecha] in self.lista_asociados
    if not reg2:
      reg3 = [canal, version, fecha] in self.lista_nacionales
      if not reg3:
        self.lista_nacionales.append([canal, version, fecha])
        out = 1
      else:
        out = -1 

    return out

  ##  --
  def actualiza_alcance_para_nacionales(self):
    for i in range(len(self.df_test3)):
      canal = self.df_test3.loc[i,'CANAL']
      version = self.df_test3.loc[i,'VERSION']
      fecha = self.df_test3.loc[i,'FECHA_NEW']
      if [canal, version, fecha] in self.lista_nacionales:
        self.df_test3.loc[i,'SELECCIÓN'] = 'NACIONAL'
    #GFM print('OK .. Actualizado nacionales')

  # actualizar el alcance para Asociados
  def actualiza_alcance_para_asociados(self):
    for i in range(len(self.df_test3)):
      canal = self.df_test3.loc[i,'CANAL']
      version = self.df_test3.loc[i,'VERSION']
      fecha = self.df_test3.loc[i,'FECHA_NEW']
      if [canal, version, fecha] in self.lista_asociados:
        self.df_test3.loc[i,'SELECCIÓN'] = 'N'

    #GFM print ('OK .. Actualizado Asociados')   
    return 0
  # ---------------
  #Actualiza el alcance para los registros locales
  def actualiza_alcance_para_locales(self):
    for i in range(len(self.df_test3)):
      canal = self.df_test3.loc[i,'CANAL']
      version = self.df_test3.loc[i,'VERSION']
      fecha = self.df_test3.loc[i,'FECHA_NEW']
      alcance = self.df_test3.loc[i,'SELECCIÓN']
      if alcance == '':
        #print ([canal, version, fecha])
        self.df_test3.loc[i,'SELECCIÓN'] = 'LOCAL'
      ## else:
        ## print(f'elemento: {[canal, version, fecha]} NO es LOCAL..')
    #GFM print('OK..LOCALES')

    return 0

  ## ------------- determina el alcance ------------
  def determina_nivel_alcance(self):
    self.lista_nacionales.clear()
    self.lista_asociados.clear()

    df_global = self.df_spots_fecha_ordenado[['CANAL', 'VERSION', 'FECHA_NEW']]
    df_global = df_global.sort_values(['VERSION', 'FECHA_NEW'], ascending = True)

    nDatos = len(df_global)
    #nDatos = 200

    bande = False

    ## f = open('resultados4.txt','a') para cuando se necesite depurar
    #for i in range(0, nDatos):
    i = 0
    while i in range(0, nDatos):
      #print(f'i= {i}')
      loc_n = df_global.index[i]
      canal1 = df_global.loc[loc_n,'CANAL']
      version1 = df_global.loc[loc_n, 'VERSION']
      fecha1 = df_global.loc[loc_n,'FECHA_NEW']

      df_w1 = self.df_spots_fecha_ordenado.VERSION == version1
      df_w1 = self.df_spots_fecha_ordenado[df_w1]
      ## revisando
      df_w1 = df_w1.sort_values(['FECHA_NEW'], ascending=True)

      n_df = len(df_w1)
      k = 0
      
      # for j in range(i+1, num_df_filtrado):

      while k < n_df:
        loc_n = df_w1.index[k]
        canal1 = df_w1.loc[loc_n,'CANAL']
        version1 = df_w1.loc[loc_n, 'VERSION']
        fecha1 = df_w1.loc[loc_n,'FECHA_NEW']
        j = k + 1 #  = k + 1
        bande = False
        bande_asociados = False
        while (j < n_df):
          loc = df_w1.index[j]
          canal2 = df_w1.loc[loc,'CANAL']
          version2 = df_w1.loc[loc,'VERSION']
          fecha2  = df_w1.loc[loc, 'FECHA_NEW']

          dif_fecha = self.dif_fecha_con_margen_segundos_fechas(fecha1, fecha2, 120)
          flag_fecha = dif_fecha <= 120

          flag_canal = (canal1 == canal2)
          flag_version = version1 == version2

          es_nacional = version1 == version2 and flag_fecha

          # inicio del algoritmo

          if es_nacional:
            flag_n = self.adicionar_en_lista_nacionales_v2(canal1, version1, fecha1)
            if flag_n == 1 or flag_n == -1 :  ## si se pudo adicionar a 
              self.adicionar_en_lista_asociados(canal2, version2, fecha2)
            
          # fin de lógica de detección de nacionales y asociados
          if es_nacional: 
            j = j + 1
          else:
            j = n_df  
        k = k + 1
      
      #GFM if i % 150 == 0:
      #GFM  print(f'.{i}.')
      #GFMelse:
      #GFM  print (f'.{i}.', end="")  
      
      i = i + n_df

    #imprime la lista
    #GFM print('-------------- lista de asociados -------------')
    #print(lista_asociados)
        #imprime la lista
    # GFM print('-------------- lista de Nacionales -------------')
    #print(lista_nacionales)

    return 0

    #### fin determina nivdel de alcance
    
  def determina_eventos_tipo_MEGAPLAZA(self):
    print(self.lista_nacionales)
    print(self.lista_asociados)
    lista_new = []
    start = 0
    ## si el resultado ya se tiene en df_test3, ahora lo recorremos y formamos una lista para cada nacional con sus N
    enum_nacionales = enumerate(self.lista_nacionales)
    enum_asociados = enumerate(self.lista_asociados)
    print('--inicio---')
    #print(enum_nacionales[0:1])

     
      
    


  ## método que exporta los resultados a archivo de excel
  def export_to_excel(self):
    
    ## export el archivo df_test3 a excel
    ## SI Se desean eliminar os registros Asociados ('N') desde aquí
    #df_test_SinN = df_test3_sinN = self.df_test3.drop(self.df_test3[(self.df_test3['SELECCIÓN'] =='N')].index);
    df_test3_sinN = self.df_test3.drop(self.df_test3[(self.df_test3['SELECCIÓN'] =='N')].index)
    df_test3_sinN.to_excel(self.ruta + 'df_test3_sinN.xlsx')
    self.df_test3.to_excel(self.ruta + 'df_test3.xlsx')
    #GFM print('Se exportó el archivo de resultados: .. df_test3.xlsx')
    return self.df_test3

  def actualiza_alcance_eventos(self):
    ## GFM_1 self.df_test3.loc[:, 'SELECCIÓN'] = ""
    
    self.df_test3['SELECCIÓN'] = None
    #self.df_test3=self.df_test3['SELECCIÓN'].astype(str)
    self.df_test3.loc[:, 'SELECCIÓN'] = ""
    self.determina_nivel_alcance()
    ## self.determina_eventos_tipo_MEGAPLAZA()
    self.actualiza_alcance_para_nacionales()
    self.actualiza_alcance_para_asociados()
    self.actualiza_alcance_para_locales()
    
    # regresa todo el dataframe, pero omite los asociados
    
    #self.df_result = self.df_test3[self.df_test3['SELECCIÓN' == 'NACIONAL' AND 'SELECCIÓN' == 'LOCAL']]
    #self.df_no_registros_N = self.df_test3[(self.df_test3['SELECCIÓN'] != 'N')]
    df_test3_sinN = self.df_test3.drop(self.df_test3[(self.df_test3['SELECCIÓN'] =='N')].index)
    
    filename_sin_n = self.ruta + "df_test3_sinN.xlsx"
    df_test3_sinN.to_excel(filename_sin_n)
    

#### Fin de métodos para implementar el Algoritmo para determinar el ALCANCE

## Regresa L-V si el día está entre 0-4 y  S-D si es 5-6 
  def determina_diastr(self, dia):
    dia_LV = [0, 1, 2, 3, 4]
    dia_SD = [5,6]
    if dia in dia_LV:
      strdia = 'L-V'
    elif dia in dia_SD:
      strdia = 'L-D'
    
    return strdia


  ## Regresa S si es sabado y D si es domingo
  def es_sabado_o_domingo(self, dia):
    if dia == 5:
      dia_o = 'S'
    elif dia == 6:
      dia_o = 'D'   
    return dia_o

  def configurar_archivos_para_tarifas(self):
    #filename_plazas_tarifas = self.ruta + "Tarifas2024_4_Actualizado.xlsx"
    filename_plazas_tarifas = self.ruta + "Tarifas2024_26_07_v2.xlsx"
    self.df_tarifas = pd.read_excel(filename_plazas_tarifas, sheet_name='PLAZAS_TARIFAS')

    #filename_plazas_canales = "/content/drive/MyDrive/proy_anun/tarifas_GFM.xlsx"
    self.df_plazas_canales = pd.read_excel(filename_plazas_tarifas, sheet_name='PLAZAS_CANALES')

    #self.df_tarifas_nacionales = pd.read_excel(filename_plazas_tarifas, sheet_name='TARIFAS_NACIONALES')

    # Se abre la hoja donde están los nombres de los canales que corresponden a cada Televisora 
    self.df_canales_reales = pd.read_excel(filename_plazas_tarifas, sheet_name='CANALES_REALES')

    return 0
## fin del métod para configurar archivos para Tarifas

## método para ubicar la tarifa de acuerdo a la PLAZA
  def busca_tarifa_por_sede_hora(self, plaza, hora, minuto, x_dia):
    

    cond1 = plaza == self.df_tarifas.PLAZA  ## and canal == self.df_tarifas.ALIAS_CANAL         # ['PLAZA']
    cond2 = (hora * 60 + minuto) >= (self.df_tarifas.T_INICIO_HOR *60 + self.df_tarifas.T_INICIO_MIN )
    #cond2 = hora >= self.df_tarifas.T_INICIO_HOR  and minuto >= self.df_tarifas.T_INICIO_MIN       # ['HOR_INI']
    cond3 = ( hora * 60 + minuto)  < (self.df_tarifas.T_FIN_HOR * 60 + self.df_tarifas.T_FIN_MIN)
    #cond3 = hora < self.df_tarifas.T_FIN_HOR and minuto < self.df_tarifas.T_FIN_MIN               #['HOR_FIN']

    
    df_filtrado_tarifa = self.df_tarifas[['PLAZA', 'TARIFA', 'DIA' ]].query('@cond1 & @cond2 & @cond3')      ## &)   (@cond4 | @cond5) | @cond6')
  
    
    ## DEBUG print(f'en busca_tarifa_por_sede_hora: {df_filtrado_tarifa}')
    
    #DEBUG print(f"Dia desde el DF: {df_filtrado_tarifa}")
    result = -1
    
    # EL DataFrame filtrado o resultante arroja varios registros de acuerdo al día 
    ## Si es L-V o L-D o S-D y se implementa la lógica para determinar cuál de los registros tomar.
    ## 
    
    flag_dia = False
    i = 0
    res = df_filtrado_tarifa.DIA.values[0]
    #if df_filtrado_tarifa.size > 0 :
    if len(df_filtrado_tarifa) > 0 :
      while not flag_dia and i < len(df_filtrado_tarifa):
        x_str_dia = df_filtrado_tarifa.DIA.values[i]
        
        if df_filtrado_tarifa.DIA.values[i] == 'L-D' and x_dia in [0,1,2,3,4,5,6]:               
          res =  df_filtrado_tarifa.TARIFA.values[i]
          
          flag_dia = True
        elif df_filtrado_tarifa.DIA.values[i] == 'L-V' and x_dia in [0,1,2,3,4]:                
          res =  df_filtrado_tarifa.TARIFA.values[i]
          flag_dia = True
        elif df_filtrado_tarifa.DIA.values[i] == 'S-D' and x_dia in [5,6]:
          res =  df_filtrado_tarifa.TARIFA.values[i]
          flag_dia = True
        elif df_filtrado_tarifa.DIA.values[i] == 'S' and x_dia in [5]:
          res =  df_filtrado_tarifa.TARIFA.values[i]
          flag_dia = True
        elif df_filtrado_tarifa.DIA.values[i] == 'D' and x_dia in [6]:
          res =  df_filtrado_tarifa.TARIFA.values[i]
          flag_dia = True
        else:
          i = i + 1
      if res >= 0:
        result =  res  #df_filtrado_tarifa.TARIFA.values[i]
      else:
        msg = 'TARIFA no encontrada -> PLAZA: ' + str(plaza) + ' ' + ' hora: ' + ' ' + str(hora) + ' '  + ' minuto:' + ' ' + str(minuto)  + ' ' + ' x_str_dia: ' +  x_str_dia + ' dia: ' + str(x_dia) 
        #print (f'no se encontró la tarifa para la plaza: {plaza} -  hora: {hora} - min: {minuto} y dia: {x_dia}')
        print(msg)
        result = 0     
      #result = df_filtrado_tarifa.TARIFA.values[0]
    else:    
      msg = 'TARIFA no se encontró -> PLAZA: ' + str(plaza) + ' ' + 'hora:' + ' ' + str(hora) + ' '  + 'minuto:' + ' ' + str(minuto)  + ' ' + 'x_str_dia: ' +  x_str_dia  
      self.write_a_log_reg(msg)
      
      ##print(f'NO SE ENCONTRÓ LA TARIFA -> plaza: {plaza} - hora: {hora}')
      
      ## print(f'NO SE ENCONTRÓ LA TARIFA -> plaza: {plaza} hora: {hora}')
    ## DEBUG print(f'result{result}')

    return result
## fin del método

## método para buscar la plaza de acuerdo al CANAL que aplique
  def busca_plaza_por_canal(self, canal):
    #cond1 = canal == self.df_plazas_canales.CANAL
    cond1 = canal == self.df_plazas_canales.CANAL
    df_filtrado_plaza = self.df_plazas_canales[cond1]
    #print(df_filtrado_plaza['PLAZA'])
    plaza = -1 
    if len(df_filtrado_plaza) > 0:
      plaza =  df_filtrado_plaza.PLAZA.values[0]    ###['PLAZA']    
    else:
      msg = 'NO SE ENCONTRÓ LA PLAZA PARA EL CANAL: -> canal:' + str(canal) 
      ##print(f'NO SE ENCONTRÓ LA PLAZA -> canal: {canal}')
      self.write_a_log_reg(msg)
      
  
    ## DEBUG print(f'plaza: {plaza}')
    #where[cond1 and cond2 and cond3]
    #print(f'Plaza : {plaza}')
    return plaza
## fin del método

## método para determinar la tarifa para un evento NACIONAL de acuerdo a la HORA

  def determina_tarifa_en_nacional_hora(self, canal, hora, minuto, x_dia):
    plaza = 'NACIONAL'
  
    #cond1 = plaza == self.df_tarifas_nacionales.PLAZA           # ['PLAZA']
    #cond2 = hora >= self.df_tarifas_nacionales.T_INICIO_HOR         # ['HOR_INI']
    #cond3 = hora < self.df_tarifas_nacionales.T_FIN_HOR                 #['HOR_FIN']

    cond1 = plaza == self.df_tarifas.PLAZA and self.df_tarifas.ALIAS_CANAL == canal          # ['PLAZA']
    cond2 = (hora * 60 + minuto) >= (self.df_tarifas.T_INICIO_HOR *60 + self.df_tarifas.T_INICIO_MIN )
    #cond2 = hora >= self.df_tarifas.T_INICIO_HOR  and minuto >= self.df_tarifas.T_INICIO_MIN       # ['HOR_INI']
    cond3 = ( hora * 60 + minuto)  < (self.df_tarifas.T_FIN_HOR * 60 + self.df_tarifas.T_FIN_MIN)
    
    x_str_dia = self.determina_diastr(x_dia) 
    if x_str_dia == 'S-D':
      x_str_dia_sd = self.es_sabado_o_domingo(x_dia)

    cond4 = x_str_dia == self.df_tarifas.DIA or x_str_dia_sd == self.df_tarifas.DIA  
    

    #df_filtrado_tarifa_nal = self.df_tarifas_nacionales[['TARIFA']].query('@cond1 & @cond2 & @cond3')
    tarifa_x = self.busca_tarifa_por_sede_hora(plaza, hora, minuto, x_dia)
    
    #df_filtrado_tarifa_nal = self.df_tarifas[['TARIFA']].query('@cond1 & @cond2 & @cond3')
  
    ## DEBUG print(f'filtrado antes: {df_filtrado_tarifa_nal}')
    
    ## DEBUG print(f'filtrado: {result}')
    #print(result)

    return tarifa_x
## fin del método

# Método para recuperar la Tarifa usando el CANAL como argumento
  def determina_tarifa_local(self, canal, hora, minuto, dia_evento):
    ## DEBUG print(f'Buscando tarifa: canal: {canal} - hora: {hora}')
    plaza = self.busca_plaza_por_canal(canal)
    tarifa_x = self.busca_tarifa_por_sede_hora(plaza, hora, minuto, dia_evento)
    #print(f'determina_tarifa local -> tarifa: {tarifa_x} - {plaza} - {hora} - {minuto} - {dia_evento}')
    return tarifa_x
## fin del método

# Función para recuperar la Tarifa usando el CANAL como argumento
  
  def nacional(self, hora):
    tarifa_x = self.busca_tarifa_en_nacional_hora(hora)
    ##print(f'Tarifa a aplicar: {tarifa_x}')
    return tarifa_x
## fin del método

## método para obtener el factor a aplicar dependiendo del rango de la duración
  def determina_factor_aplicar_tarifa(self, duracion):
    if duracion <= 10:
      factor = 0.5
    elif duracion > 10 and duracion <= 20:
      factor = 1.0
    elif duracion > 20 and duracion <= 30:
      factor = 1.5
    elif duracion > 30 and duracion <= 40:
      factor = 2
    elif duracion > 40:
      factor = 2.5
    return factor
## fin del método

# Método para buscar el nombre del CANAL cuando es posible nacional 
  def busca_canal_real(self, canal):
    
    found = False
    len_df = len(self.df_canales_reales)
    i = 0
    result = -1
    while not found and i < len_df:
      x_canal = self.df_canales_reales.loc[i, 'CANAL_P']      
      if self.df_canales_reales.loc[i,'CANAL_P'] in canal:
        result = x_canal 
        found = True  
      else:
        i = i+1
      #print(f'El nombre real del canal es: {result}\n')
    return result

## método integrador para actualizar la tarifa de cada uno de los registros
  def actualiza_tarifa(self):
    for i in range(len(self.df_test3)):
      canal = self.df_test3.loc[i,'CANAL']
      version = self.df_test3.loc[i,'VERSION']
      fecha = self.df_test3.loc[i,'FECHA_NEW']
      alcance = self.df_test3.loc[i,'SELECCIÓN']
      dia_evento = fecha.weekday()
      hora = fecha.hour
      minuto = fecha.minute

      #print(f'CANAL: {canal} -- VERSION: {version} hora: {hora}')

      duracion = self.df_test3.loc[i,'dur_min']*60 + self.df_test3.loc[i,'dur_seg']
      factor = self.determina_factor_aplicar_tarifa(duracion)


      ##if  i% 150 == 0:
      ##  print('.')
      ##else:
      ##  print('.' , end="")

      if alcance == 'LOCAL':
        self.df_test3.loc[i,'TARIFA'] = self.determina_tarifa_local(canal, hora, minuto, dia_evento) * factor  
      elif alcance == 'NACIONAL':
        #print(f'Evaluando tarifa NACIONAL alcance:{alcance} - canal: {canal} ')

        canal_p = self.busca_canal_real(canal)  
        #print(f'at. tarifa: CANAL REAL {canal}- {version} - {fecha} - {dia_evento} ')

        canal = 'NACIONAL' + canal_p
        
        ##self.df_test3.loc[i,'TARIFA'] = self.determina_tarifa_en_nacional_hora(canal, hora, minuto) * factor
        #print(f'at. tarifa {canal}- {hora} - {minuto} -{dia_evento} - {factor}')
        self.df_test3.loc[i,'TARIFA'] = self.determina_tarifa_local(canal, hora, minuto, dia_evento) * factor 
        
      
      #elif self.df_test3.loc[i,'SELECCIÓN'] == 'NACIONAL':   
      #  self.df_test3.loc[i,'TARIFA'] = self.determina_tarifa_en_nacional_hora(hora, minuto) * factor

      ## print('OK..tarifas actualizadas')
      ## Cierra el archivo de registro de logs
      
    self.file_log.close()
      
    return self.df_test3
## fin del método



def consulta_archivo_plazas_tarifas(self):
  #filename_plazas_tarifas = self.ruta + "Tarifas2024_4_Actualizado.xlsx"
  filename_plazas_tarifas = self.ruta + "Tarifas2024_26_07_v2.xlsx"
  
  self.df_tarifas = pd.read_excel(filename_plazas_tarifas, sheet_name='PLAZAS_TARIFAS')
  
  return self.df_tarifas
  
  
# Abre el archivo de logs y escribe un registro.

### ============ FIN DE LA CLASE =================
 
def main():
  str_file_name = input("ingrese el nombre del archivo: ")

  clasificador = SpotsClassifier(str_file_name)
 
  clasificador.initial_configuration()

  clasificador.actualiza_alcance_eventos()

  ## Se tiene en df_test3 los registros con el ALCANCE ya determinado
  ## Una vez que ya se determinó el ALCANCE se hace la..
  ## Implementación para cálculo de las tarifas 

  clasificador.configurar_archivos_para_tarifas() ## se lee el archivo de excel con la tarifas por sede y los canales por Sede

  clasificador.actualiza_tarifa()

  ## clasificador.export_to_excel()



if __name__ == "__main__":
  main()