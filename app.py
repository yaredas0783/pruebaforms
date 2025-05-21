import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

st.title("📋 Formulario de Registro")

def validar_correo(correo):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

@st.cache_data
def cargar_ubicaciones(ruta):
    df = pd.read_excel(ruta)
    df['Provincia'] = df['Provincia'].str.strip()
    df['Cantón'] = df['Cantón'].str.strip()
    df['Distrito'] = df['Distrito'].str.strip()
    return df

archivo_ubicaciones = "división_territorial_CR.xlsx"
if not os.path.exists(archivo_ubicaciones):
    st.error("Archivo de ubicaciones no encontrado. Por favor, sube el archivo 'ubicaciones.xlsx' con las columnas Provincia, Cantón y Distrito.")
    st.stop()

df_ubicaciones = cargar_ubicaciones(archivo_ubicaciones)

# Inicializar session_state para inputs si no existen
campos = {
    "nombre": "", "edad": 0, "correo": "", "comentario": "",
    "provincia": "", "canton": "", "distrito": "", "grupo": "", "asististe": "Seleccione...", "motivo_ausencia": [],
    "clase_favorita": "", "clase_menos_gusto": "", "recomendaciones": "", "experiencia": "",
    "calificacion": 5, "interes_cursos": [], "otro_curso": ""
}
for key, default in campos.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Campos del formulario (igual)
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
    options=["Seleccione...", "Si", "No"],
    key="asististe"
)
motivo_ausencia = st.multiselect(
    "Si faltaste a algunas de las clases, ¿por qué fue? *",
    options=[
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
clase_favorita = st.text_area("¿Cuál de las clases te gustó más? Porfa contanos por qué *", key="clase_favorita")
clase_menos_gusto = st.text_area("¿Cuál de las clases te gustó menos? Porfa contanos por qué *", key="clase_menos_gusto")
recomendaciones = st.text_area("¿Qué recomendaciones nos harías para el futuro? *", key="recomendaciones")
experiencia = st.text_area("¿Podrías escribir unas pocas líneas comentándonos tu experiencia y resumiéndonos cuál ha sido tu apreciación general del curso? *", key="experiencia")
calificacion = st.slider(
    "En general, ¿qué calificación le das al curso? *",
    1, 10,
    step=1,
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
otro_curso = st.text_input("¿Qué otro curso te gustaría recibir de manera virtual?", key="otro_curso")

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
        # Validaciones
        if not nombre.strip():
            st.error("Por favor ingresa tu nombre completo.")
        elif not validar_correo(correo):
            st.error("Por favor ingresa un correo válido.")
        elif not provincia or not canton or not distrito:
            st.error("Por favor selecciona provincia, cantón y distrito.")
        elif not grupo:
            st.error("Por favor selecciona el grupo.")
        elif asististe == "Seleccione...":
            st.error("Por favor indica si asististe a las cuatro clases.")
        elif not motivo_ausencia:
            st.error("Por favor selecciona el motivo de ausencia.")
        elif not clase_favorita.strip():
            st.error("Por favor escribe cuál fue tu clase favorita.")
        elif not clase_menos_gusto.strip():
            st.error("Por favor escribe cuál fue la clase que menos te gustó.")
        elif not recomendaciones.strip():
            st.error("Por favor escribe tus recomendaciones.")
        elif not experiencia.strip():
            st.error("Por favor escribe tu experiencia general del curso.")
        else:
            nueva_respuesta = pd.DataFrame({
                'Nombre': [nombre],
                'Edad': [edad],
                'Correo': [correo],
                'Grupo': [grupo],
                'Asistió a todas las clases': [asististe],
                'Motivo de ausencia': [", ".join(motivo_ausencia)],
                'Clase favorita': [clase_favorita],
                'Clase que menos gustó': [clase_menos_gusto],
                'Recomendaciones': [recomendaciones],
                'Experiencia general': [experiencia],
                'Calificación curso': [calificacion],
                'Interés en otros cursos': [", ".join(interes_cursos) if interes_cursos else ""],
                'Otro curso deseado': [otro_curso],
                'Provincia': [provincia],
                'Cantón': [canton],
                'Distrito': [distrito],
                'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })

            # Guardar respuesta sin leer todo el CSV (append mode)
            if not os.path.exists(archivo):
                nueva_respuesta.to_csv(archivo, index=False)
            else:
                nueva_respuesta.to_csv(archivo, mode='a', header=False, index=False)

            st.success("✅ ¡Gracias por enviar tu respuesta!")

if st.checkbox("Mostrar respuestas"):
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    usuario_correcto = "admin"
    contraseña_correcta = st.secrets["CONTRASENA_ADMIN"]

    if user == usuario_correcto and password == contraseña_correcta:
        if os.path.exists(archivo):
            st.write(pd.read_csv(archivo))
        else:
            st.write("Aún no hay respuestas.")
    else:
        st.warning("❌ Usuario o contraseña incorrectos")
