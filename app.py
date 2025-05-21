import streamlit as st
import pandas as pd
import os

st.title("📋 Formulario de Registro")

# Campos del formulario
nombre = st.text_input("Nombre completo")
edad = st.number_input("Edad", 0, 120)
correo = st.text_input("Correo electrónico")
comentario = st.text_area("Comentario")

# Nombre del archivo donde se guardarán las respuestas
archivo = "respuestas.csv"

if st.button("Enviar"):
    nueva_respuesta = pd.DataFrame({
        'Nombre': [nombre],
        'Edad': [edad],
        'Correo': [correo],
        'Comentario': [comentario]
    })
    
    if os.path.exists(archivo):
        df_existente = pd.read_csv(archivo)
        df_actualizado = pd.concat([df_existente, nueva_respuesta], ignore_index=True)
    else:
        df_actualizado = nueva_respuesta

    df_actualizado.to_csv(archivo, index=False)
    st.success("✅ ¡Gracias por enviar tu respuesta!")

# Sección para mostrar respuestas protegida con usuario y contraseña
if st.checkbox("Mostrar respuestas"):
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # Aquí defines usuario y contraseña correctos (puedes cambiar por los que quieras)
    usuario_correcto = "admin"
    contraseña_correcta = "1234"

    if user == usuario_correcto and password == contraseña_correcta:
        if os.path.exists(archivo):
            st.write(pd.read_csv(archivo))
        else:
            st.write("Aún no hay respuestas.")
    else:
        st.warning("❌ Usuario o contraseña incorrectos")
