import streamlit as st
import requests
import fitz  # PyMuPDF
import io

# ID del archivo en Google Drive
FILE_ID = "1b3SlIV2Tbb0wpm7vMnD5Ua3Q9MhuvWvc"  # reemplaza por tu ID
FILE_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def obtener_folios_desde_drive(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("No se pudo descargar el archivo PDF.")
    
    # Leer PDF en memoria
    with fitz.open(stream=io.BytesIO(response.content), filetype="pdf") as doc:
        texto_completo = ""
        for page in doc:
            texto_completo += page.get_text()

    import re
    folios = re.findall(r'\b[A-Z0-9]{10}\b', texto_completo)
    return set(folios)

st.title("🔍 Buscador de Folios Aceptados del Programa Corazon de Mujer Morelos By: Emiliano Dorantes")
st.write("Introduce tu folio para verificar si fue aceptado.")

try:
    folios_validos = obtener_folios_desde_drive(FILE_URL)

    folio_usuario = st.text_input("Escribe tu folio").strip().upper()

    if folio_usuario:
        if folio_usuario in folios_validos:
            st.success("✅ ¡Tu folio ha sido aceptado!")
        else:
            st.error("❌ Tu folio no se encuentra en la lista.")
except Exception as e:
    st.error(f"Ocurrió un error: {e}")
