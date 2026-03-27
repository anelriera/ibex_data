# IBEX 35 Data Pipeline 📈

Un script en Python que automatiza la extracción de datos financieros de las empresas del IBEX 35 (usando Yahoo Finance) y los envía directamente a Google Sheets mediante su API oficial. 

Ideal para usar como fuente de datos en directo para dashboards de **Looker Studio** o PowerBI.

## ¿Qué hace el script?
1. **Descarga en tiempo real** los precios de las 35 empresas del IBEX español.
2. **Extrae la fecha técnica (Metadata)**: Sector, Industria, País, P/E Ratio, Dividend Yield, etc.
3. **Calcula métricas clave**: Variación Diaria/Semanal/Mensual, Volatilidad anualizada y distancias a los máximos/mínimos de 52 semanas.
4. **Sincroniza con la Nube**: Borra los datos antiguos y escribe la tabla actualizada en un Google Sheet a través de una Cuenta de Servicio (Service Account) de Google Cloud.

## Requisitos Previos (Instalación)

Asegúrate de tener instalado Python y luego instala las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## Configuración de Google Sheets (Service Account)

Para que el script tenga permisos de editar tu hoja de Google Sheets, necesitas:
1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/) y activar la **Google Sheets API** y **Google Drive API**.
2. Crear una **Service Account** y generar una clave privada en formato JSON.
3. Descargar ese archivo, renombrarlo a `credentials.json` y guardarlo en la misma carpeta que este script.
4. Copiar el `client_email` que hay dentro de ese JSON, ir a tu Google Sheet en el navegador y **darle permisos de Editor** a ese email.
5. Pegar la URL de tu Google Sheet al final del archivo `ibex_scraper.py`.

> **⚠️ ADVERTENCIA DE SEGURIDAD**: Nunca subas tu archivo `credentials.json` a repositorios públicos como GitHub. El archivo `.gitignore` incluido en este proyecto ya está configurado para ignorarlo automáticamente.

## Uso

Simplemente ejecuta el script en tu terminal. Tardará entre 1 y 2 minutos en recabar toda la información de Yahoo Finance y la subirá automáticamente.

```bash
python ibex_scraper.py
```
