import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

st.title("📋 Formulario de Registro")

def validar_correo(correo):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

# Inicializar valores en session_state si no existen
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "edad" not in st.session_state:
    st.session_state.edad = 0
if "correo" not in st.session_state:
    st.session_state.correo = ""
if "comentario" not in st.session_state:
    st.session_state.comentario = ""

# Función para limpiar formulario
def limpiar_formulario():
    st.session_state.nombre = ""
    st.session_state.edad = 0
    st.session_state.correo = ""
    st.session_state.comentario = ""

# Campos del formulario vinculados a session_state
nombre = st.text_input("Nombre completo", key="nombre")
edad = st.number_input("Edad", 0, 120, key="edad")
correo = st.text_input("Correo electrónico", key="correo")
comentario = st.text_area("Comentario", key="comentario")

archivo = "respuestas.csv"

col1, col2 = st.columns(2)

with col1:
    if st.button("Enviar"):
        if not nombre.strip():
            st.error("Por favor ingresa tu nombre completo.")
        elif not validar_correo(correo):
            st.error("Por favor ingresa un correo válido.")
        else:
            nueva_respuesta = pd.DataFrame({
                'Nombre': [nombre],
                'Edad': [edad],
                'Correo': [correo],
                'Comentario': [comentario],
                'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })
            
            if os.path.exists(archivo):
                df_existente = pd.read_csv(archivo)
                df_actualizado = pd.concat([df_existente, nueva_respuesta], ignore_index=True)
            else:
                df_actualizado = nueva_respuesta

            df_actualizado.to_csv(archivo, index=False)
            st.success("✅ ¡Gracias por enviar tu respuesta!")

with col2:
    if st.button("Limpiar formulario"):
        limpiar_formulario()
        st.info("Formulario limpiado.")

if st.checkbox("Mostrar respuestas"):
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    usuario_correcto = "admin"
    contraseña_correcta = "1234"

    if user == usuario_correcto and password == contraseña_correcta:
        if os.path.exists(archivo):
            st.write(pd.read_csv(archivo))
        else:
            st.write("Aún no hay respuestas.")
    else:
        st.warning("❌ Usuario o contraseña incorrectos")
