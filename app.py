import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

st.title("📋 Formulario de Registro")

def validar_correo(correo):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

# Cargar archivo con provincias, cantones y distritos
archivo_ubicaciones = "división_territorial_CR.xlsx"

if not os.path.exists(archivo_ubicaciones):
    st.error("Archivo de ubicaciones no encontrado. Por favor, sube el archivo 'ubicaciones.xlsx' con las columnas Provincia, Cantón y Distrito.")
    st.stop()

df_ubicaciones = pd.read_excel(archivo_ubicaciones)


# Limpieza rápida para evitar espacios extras
df_ubicaciones['Provincia'] = df_ubicaciones['Provincia'].str.strip()
df_ubicaciones['Cantón'] = df_ubicaciones['Cantón'].str.strip()
df_ubicaciones['Distrito'] = df_ubicaciones['Distrito'].str.strip()

# Inicializar session_state para inputs si no existen
for key, default in [("nombre", ""), ("edad", 0), ("correo", ""), ("comentario", ""),
                     ("provincia", ""), ("canton", ""), ("distrito", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

def limpiar_formulario():
    for key in ["nombre", "edad", "correo", "comentario", "provincia", "canton", "distrito"]:
        if isinstance(st.session_state[key], int):
            st.session_state[key] = 0
        else:
            st.session_state[key] = ""

# Campos del formulario
nombre = st.text_input("Nombre completo", key="nombre")
edad = st.number_input("Edad", 0, 120, key="edad")
correo = st.text_input("Correo electrónico", key="correo")
grupo = st.selectbox(
    "¿Cuál es el número de grupo donde te inscribiste? *",
    options=["", "Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5", "Grupo 6", "Grupo 7", "Grupo 8", "Grupo 9", "Grupo 10"],
    key="grupo"
)
asististe = st.radio(
    "¿Asististe a las cuatro clases? *",
    options=["Si", "No"],
    key="asististe"
)
motivo_ausencia = st.selectbox(
    "Si faltaste a algunas de las clases, ¿por qué fue? *",
    options=[
        "",
        "Tuve problemas de internet",
        "Tuve que atender otras situaciones",
        "Sentía que las clases no me eran útiles",
        "No entendía la materia",
        "No me gustaban las clases",
        "El horario me resultaba muy incómodo",
        "No falté a ninguna clase",
        "Otros"
    ],
    key="motivo_ausencia"
)
clase_favorita = st.text_area(
    "¿Cuál de las clases te gustó más? Porfa contanos por qué *",
    key="clase_favorita"
)
clase_menos_gusto = st.text_area(
    "¿Cuál de las clases te gustó menos? Porfa contanos por qué *",
    key="clase_menos_gusto"
)
recomendaciones = st.text_area(
    "¿Qué recomendaciones nos harías para el futuro? *",
    key="recomendaciones"
)

experiencia = st.text_area(
    "¿Podrías escribir unas pocas líneas comentándonos tu experiencia y resumiéndonos cuál ha sido tu apreciación general del curso? (Por ejemplo, podrías responder a alguna o algunas de estas preguntas: ¿cómo ha sido el contacto con tus tutores? ¿te has sentido acompañado(a) y apoyado(a)? ¿El curso ha cumplido tus expectativas? ¿qué fue lo que más te gustó? ¿qué fue lo que menos te gustó? ¿recomendarías el curso a otras personas? ¿te sentís contento(a) de haber llevado el curso?, o simplemente contarnos qué te ha parecido todo…)*",
    key="experiencia"
)

calificacion = st.slider(
    "En general, ¿qué calificación le das al curso? *",
    min_value=1, max_value=10, value=5, step=1,
    format="%d",
    key="calificacion"
)
interes_cursos = st.multiselect(
    "Interés por otros cursos que impartimos y que no hayas llevado *",
    options=[
        "Economía para la Vida",
        "Redacción Consciente",
        "Excel Intermedio",
        "Economía para entender el Mercado y la Sociedad",
        "Indicadores Macroeconómicos",
        "Ninguno"
    ],
    key="interes_cursos"
)

otro_curso = st.text_input(
    "¿Qué otro curso te gustaría recibir de manera virtual?",
    key="otro_curso"
)

# Select provincia
provincias = df_ubicaciones['Provincia'].unique()
provincia = st.selectbox("Provincia", options=[""] + list(provincias), key="provincia")

# Select cantón según provincia
if provincia:
    cantones = df_ubicaciones[df_ubicaciones['Provincia'] == provincia]['Cantón'].unique()
else:
    cantones = []
canton = st.selectbox("Cantón", options=[""] + list(cantones), key="canton")

# Select distrito según cantón
if canton:
    distritos = df_ubicaciones[(df_ubicaciones['Provincia'] == provincia) & (df_ubicaciones['Cantón'] == canton)]['Distrito'].unique()
else:
    distritos = []
distrito = st.selectbox("Distrito", options=[""] + list(distritos), key="distrito")

archivo = "respuestas.csv"

col1, col2 = st.columns(2)

with col1:
    if st.button("Enviar"):
        if not nombre.strip():
            st.error("Por favor ingresa tu nombre completo.")
        elif not validar_correo(correo):
            st.error("Por favor ingresa un correo válido.")
        elif not provincia or not canton or not distrito:
            st.error("Por favor selecciona provincia, cantón y distrito.")
        else:
            nueva_respuesta = pd.DataFrame({
                'Nombre': [nombre],
                'Edad': [edad],
                'Correo': [correo],
                'Comentario': [comentario],
                'Provincia': [provincia],
                'Cantón': [canton],
                'Distrito': [distrito],
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
