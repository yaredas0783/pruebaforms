import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# Conectarse a Google Sheets usando las credenciales desde st.secrets
credenciales = Credentials.from_service_account_info(
    st.secrets["Credenciales"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credenciales)
sheet = gc.open("Respuestas Formulario").sheet1

st.title("📋 Formulario de Registro")

# Campos del formulario
nombre = st.text_input("Nombre completo")
edad = st.number_input("Edad", 0, 120)
correo = st.text_input("Correo electrónico")
comentario = st.text_area("Comentario")

if st.button("Enviar"):
    # Añadir fila a Google Sheets
    fila = [nombre, edad, correo, comentario]
    sheet.append_row(fila)

    st.success("✅ ¡Gracias por enviar tu respuesta!")
