import yfinance as yf
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
def traducir_es(texto):
    if not isinstance(texto, str) or texto == "N/D": return texto
    diccionario = {
        "Financial Services": "Servicios Financieros", "Utilities": "Servicios Públicos",
        "Industrials": "Industriales", "Consumer Cyclical": "Consumo Cíclico",
        "Consumer Defensive": "Consumo Defensivo", "Healthcare": "Salud",
        "Technology": "Tecnología", "Real Estate": "Inmobiliaria",
        "Energy": "Energía", "Communication Services": "Telecomunicaciones",
        "Basic Materials": "Materiales Básicos", "Spain": "España",
        "Luxembourg": "Luxemburgo", "Netherlands": "Países Bajos",
        "United Kingdom": "Reino Unido", "Banks - Regional": "Bancos Regionales",
        "Banks - Diversified": "Bancos", "Utilities - Regulated Electric": "Eléctricas",
        "Utilities - Renewable": "Renovables", "Engineering & Construction": "Ingeniería y Construcción",
        "Airlines": "Aerolíneas", "Telecom Services": "Telecomunicaciones",
        "Drug Manufacturers - General": "Farmacéuticas", "Aerospace & Defense": "Aeroespacial y Defensa",
        "Oil & Gas Integrated": "Petróleo y Gas", "Retail - Apparel & Shoes": "Textil y Moda",
        "Airports & Air Services": "Aeropuertos", "Travel Services": "Turismo",
        "Medical Instruments & Supplies": "Equipamiento Médico", "Specialty Chemicals": "Química",
        "Steel": "Acero", "Information Technology Services": "Servicios TI",
        "REIT - Diversified": "SOCIMI", "REIT - Office": "SOCIMI (Oficinas)",
        "Biotechnology": "Biotecnología", "Building Products & Equipment": "Construcción",
        "Auto Parts": "Componentes de Automoción", "Infrastructure Operations": "Infraestructuras"
    }
    return diccionario.get(texto, texto)

def fetch_market_data():
    """
    Descarga los datos actuales, históricos (1 año) y metadatos de las empresas del IBEX 35.
    """
    print("Descargando historial de 1 año y metadatos de las 35 empresas del IBEX (esto tomará ~1 minuto)...")
    
    tickers_ibex = [
        "ANA.MC", "ANE.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", 
        "BBVA.MC", "SAB.MC", "SAN.MC", "BKT.MC", "CABK.MC", "CLNX.MC", 
        "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", 
        "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "NTGY.MC", "MEL.MC", 
        "MRL.MC", "PHM.MC", "RED.MC", "REP.MC", "ROVI.MC", "SCYR.MC", 
        "SLR.MC", "TEF.MC", "UNI.MC"
    ]
    
    # 1. Bajar el historial de 1 año (para calcular variaciones semanales/mensuales y máximos/mínimos)
    df_raw = yf.download(tickers_ibex, period="1y", progress=False)
    
    filas = []
    
    for tk in tickers_ibex:
        try:
            # 2. Descargar la "ficha técnica" (metadata) de la empresa
            stock = yf.Ticker(tk)
            info = stock.info
            
            # Series históricas
            closes = df_raw['Close'][tk].dropna()
            highs = df_raw['High'][tk].dropna()
            lows = df_raw['Low'][tk].dropna()
            
            if len(closes) < 22: # Necesitamos historial mínimo de 1 mes
                continue
                
            ultimo = closes.iloc[-1]
            ayer = closes.iloc[-2]
            hace_1_sem = closes.iloc[-6] if len(closes) >= 6 else closes.iloc[0]
            hace_1_mes = closes.iloc[-22] if len(closes) >= 22 else closes.iloc[0]
            
            # Máximos y Mínimos anuales (52 semanas = 1 año)
            max_52w = highs.max()
            min_52w = lows.min()
            
            # Variaciones históricas
            var_diaria = ((ultimo - ayer) / ayer) * 100
            var_semanal = ((ultimo - hace_1_sem) / hace_1_sem) * 100
            var_mensual = ((ultimo - hace_1_mes) / hace_1_mes) * 100
            
            # Volatilidad anualizada (Desviación Típica del retorno diario * raíz de 252 días hábiles)
            retornos_diarios = closes.pct_change().dropna()
            volatilidad = retornos_diarios.std() * (252 ** 0.5) * 100
            
            # Distancias
            dist_max = ((ultimo - max_52w) / max_52w) * 100
            dist_min = ((ultimo - min_52w) / min_52w) * 100
            
            # Posición en Rango (0% a 100% de donde está hoy respecto a su mínimo y máximo anual)
            rango = max_52w - min_52w
            rango_pct = ((ultimo - min_52w) / rango) * 100 if rango > 0 else 0
            
            # Extraer metadata de `.info` (fallbacks seguros con "N/D" o 0)
            nombre_largo = info.get("longName", tk.replace(".MC", ""))
            sector = traducir_es(info.get("sector", "N/D"))
            industria = traducir_es(info.get("industry", "N/D"))
            pais = traducir_es(info.get("country", "N/D"))
            
            pe_ratio = info.get("trailingPE", info.get("forwardPE", "N/D"))
            pb_ratio = info.get("priceToBook", "N/D")
            div_yield = info.get("dividendYield", 0) 
            div_yield_pct = (div_yield * 100) if div_yield else 0
            beta = info.get("beta", "N/D")
            
            mcap = info.get("marketCap", 0)
            if not mcap:
                mcap_cat = "N/D"
                mcap_val = "N/D"
            else:
                mcap_val = mcap
                if mcap >= 10_000_000_000:
                    mcap_cat = "Grande"
                elif mcap >= 2_000_000_000:
                    mcap_cat = "Mediana"
                elif mcap >= 300_000_000:
                    mcap_cat = "Pequeña"
                else:
                    mcap_cat = "Micro"
            
            # Construir la fila final con las 18 variables solicitadas
            fila = {
                "Símbolo": tk.replace(".MC", ""),
                "Nombre Completo": nombre_largo,
                "Sector": sector,
                "Industria": industria,
                "País de Sede": pais,
                "Último": float(ultimo),
                "Variación Diaria %": float(var_diaria),
                "Variación Semanal %": float(var_semanal),
                "Variación Mensual %": float(var_mensual),
                "P/E Ratio": float(pe_ratio) if pe_ratio != "N/D" else "N/D",
                "P/B Ratio": float(pb_ratio) if pb_ratio != "N/D" else "N/D",
                "Dividend Yield %": float(div_yield_pct),
                "Beta": float(beta) if beta != "N/D" else "N/D",
                "Volatilidad Anual %": float(volatilidad),
                "Distancia del Máximo %": float(dist_max),
                "Distancia del Mínimo %": float(dist_min),
                "Posición en Rango %": float(rango_pct),
                "Market Cap": mcap_val,
                "Market Cap Categoría": mcap_cat
            }
            filas.append(fila)
            print(f" -> Extraído: {tk}")
        except Exception as e:
            print(f" -> Error con {tk}: {e}")
            pass
            
    df_final = pd.DataFrame(filas)
    print(f"¡Éxito! Base de datos maestra generada con {len(df_final)} empresas.")
    return df_final

def enrich_data(df):
    """
    Da formato final a los números y porcentajes para Looker y Google Sheets.
    """
    if df.empty:
        return df
        
    print("Dando formato visual a las columnas (redondeando decimales)...")
    df = df.copy()
    
    # Definir qué columnas necesitan redondeo a 2 decimales
    cols_porcentaje = [
        "Variación Diaria %", "Variación Semanal %", "Variación Mensual %", 
        "Dividend Yield %", "Volatilidad Anual %", "Distancia del Máximo %", 
        "Distancia del Mínimo %", "Posición en Rango %"
    ]
    
    for c in cols_porcentaje:
        if c in df.columns:
            # Redondeamos sin añadir el string '%' para que Looker detecte que es un número (recomendado)
            # o podemos añadir el '%' si solo se va a leer en Google Sheets. Dejémoslo numérico.
            df[c] = pd.to_numeric(df[c], errors='coerce').round(2)
    
    if 'Último' in df.columns:
        df['Último'] = pd.to_numeric(df['Último'], errors='coerce').round(3)

    return df.fillna("N/D")

def upload_to_google_sheets(df, spreadsheet_url):
    """
    Autentica con Google Cloud y sube el dataframe procesado a Google Sheets.
    """
    print("Subiendo datos a Google Sheets...")
    
    # 1. Definir los alcances (scopes) necesarios
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # 2. Cargar credenciales desde el archivo JSON de tu Service Account
        # (Debe llamarse 'credentials.json' y estar en la misma carpeta que este script)
        credentials = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scopes
        )
        
        # 3. Autorizar el cliente usando la cuenta de servicio
        gc = gspread.authorize(credentials)
        
        spreadsheet = gc.open_by_url(spreadsheet_url)
        
        # 5. Seleccionar la primera pestaña (Workshet 1)
        worksheet = spreadsheet.sheet1
        
        # 6. Preparar los datos
        # Trabajamos sobre una copia para no modificar el data original
        df_to_upload = df.copy()
        
        # Si la fecha está en el "índice", lo pasamos a una columna normal
        if df_to_upload.index.name is not None or type(df_to_upload.index) == pd.DatetimeIndex:
            df_to_upload = df_to_upload.reset_index()
            
        # Convertimos columnas de formato fecha a texto para que Google Sheets lo lea bien
        for col in df_to_upload.select_dtypes(include=['datetime64', 'datetimetz']).columns:
            df_to_upload[col] = df_to_upload[col].dt.strftime('%Y-%m-%d')
            
        # Rellenamos celdas vacías (NaN) con textos vacíos para no dar error
        df_to_upload = df_to_upload.fillna('')
        
        # 7. Convertimos todo a una lista de listas (cabeceras + filas de datos)
        data = [df_to_upload.columns.tolist()] + df_to_upload.values.tolist()
        
        # 8. Limpiamos la pestaña y subimos los datos actualizados a partir de A1
        worksheet.clear()
        worksheet.update(values=data, range_name='A1')
        
        print(f"¡Éxito! {len(df_to_upload)} filas subidas correctamente a Google Sheets.")
        
    except FileNotFoundError:
        print("ERROR: No se encontró el archivo 'credentials.json'.")
        print("Recuerda descargar tu clave JSON desde Google Cloud, renombrarla a 'credentials.json' y guardarla en la misma carpeta donde está este script.")
    except gspread.exceptions.APIError as e:
        print("ERROR de Permiso:")
        print("Asegúrate de haber compartido tu Google Sheet con el correo de tu Service Account (dándole permisos de Editor).")
        print(f"Detalle técnico: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado al subir a Google Sheets: {type(e).__name__} - {e}")

def main():
    print("Iniciando pipeline de datos del IBEX 35...")
    
    # Descargamos datos
    df = fetch_market_data()
    
    # Calculamos indicadores
    df = enrich_data(df)
    
    # Subimos a internet
    # ATENCIÓN: Recuerda pegar la URL de tu Google Sheet y darle permiso de edición al email de service account
    upload_to_google_sheets(df, "https://docs.google.com/spreadsheets/d/14CgYsWnJOe2g5SxH-2jpi4jLUKi19eC9gv6NI0CyE5s/edit?gid=0#gid=0")
    print("Proceso finalizado con éxito.")

if __name__ == "__main__":
    main()
