import streamlit as st
import ollama
import subprocess
import sys
import importlib.util

def get_ai_response(message):
    try:
        response = ollama.chat(
            model='llama3:8b',
            messages=[{
                'role': 'system',
                'content': 'Eres un profesor experto. SIEMPRE responde en español. Usa un lenguaje claro y educativo, tambien ten en cuenta el grado de estudio del usuario {grado}.'
            },
            {
                'role': 'user',
                'content': f"Responde en español de manera educativa: {message}"
            }]
        )
        return response['message']['content']
    except Exception as e:
        st.error(f"Error al conectar con Ollama: {str(e)}")
        st.info("Asegúrate de que Ollama esté ejecutándose con 'ollama serve' y que el modelo tinyllama esté instalado con 'ollama pull tinyllama'")
        return "Lo siento, hay un problema con el servicio de IA. Por favor, verifica que Ollama esté ejecutándose correctamente."

def check_package(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except:
        return False

def check_dependencies():
    required_packages = {
        'werkzeug': 'werkzeug',
        'streamlit': 'streamlit',
        'ollama': 'ollama'
    }
    
    missing_packages = []
    for package, pip_name in required_packages.items():
        if not check_package(package):
            missing_packages.append(pip_name)
    
    if missing_packages:
        st.warning("Se necesita instalar algunas dependencias para que la aplicación funcione correctamente.")
        st.write("Paquetes faltantes:")
        for package in missing_packages:
            st.write(f"- {package}")
        
        if st.button("Instalar dependencias"):
            progress_bar = st.progress(0)
            for i, package in enumerate(missing_packages, 1):
                with st.spinner(f'Instalando {package}...'):
                    if install_package(package):
                        st.success(f"{package} instalado correctamente")
                    else:
                        st.error(f"Error al instalar {package}")
                progress_bar.progress(i/len(missing_packages))
            st.success("¡Instalación completada! Por favor, reinicia la aplicación.")
            st.rerun()
        return False
    return True

def get_materias_por_grado(grado_num):
    if grado_num < 6: 
        return {
            "Lengua Castellana": {"emoji": "📚", "color": "#FF6B6B"},
            "Matemáticas": {"emoji": "📐", "color": "#4ECDC4"},
            "Ciencias Naturales": {"emoji": "🌱", "color": "#45B7D1"},
            "Ciencias Sociales": {"emoji": "🌍", "color": "#96CEB4"},
            "Educación Artística": {"emoji": "🎨", "color": "#FFEEAD"},
            "Ética y Valores": {"emoji": "🤝", "color": "#D4A5A5"},
            "Educación Física": {"emoji": "⚽", "color": "#88D8B0"},
            "Religión": {"emoji": "🕊️", "color": "#FFB6B9"}
        } 
    else: 
        return {
            "Lengua Castellana": {"emoji": "📚", "color": "#FF6B6B"},
            "Matemáticas": {"emoji": "📐", "color": "#4ECDC4"},
            "Ciencias Sociales": {"emoji": "🌍", "color": "#96CEB4"},
            "Educación Artística": {"emoji": "🎨", "color": "#FFEEAD"},
            "Educación Física": {"emoji": "⚽", "color": "#88D8B0"},
            "Religión": {"emoji": "🕊️", "color": "#FFB6B9"},
            "Programación": {"emoji": "👨‍💻", "color": "#7b0d8a"},
            "Fisica": {"emoji": "🧑‍🔬", "color": "#117c9c"},
            "Quimica": {"emoji": "👨‍🔬", "color": "#779c11"},
        } 

def get_temas_por_materia_y_grado(materia, grado):
    temas = {
    "Lengua Castellana": {
        "Primero de primaria": {
            "temas": [
                "Escritura de textos sencillos y descripciones",
                "Identificación de personajes, escenarios y eventos",
                "Cuentos, fábulas y poesías",
                "Señales y símbolos en el entorno",
                "Escucha activa y respeto por opiniones"
            ],
            "nivel": "básico"
        },
        "Segundo de primaria": {
            "temas": [
                "Lectura y comprensión de cuentos y textos informativos",
                "Escritura de frases y párrafos con coherencia",
                "Uso de mayúsculas y signos de puntuación",
                "Identificación de la idea principal en un texto",
                "Participación en conversaciones y exposiciones sencillas"
            ],
            "nivel": "básico"
        },
    },
    "Matemáticas": {
        "Primero de primaria": {
            "temas": [
                "Comprensión básica de los números",
                "Operaciones simples (suma y resta)",
                "Reconocimiento de figuras geométricas básicas",
                "Medición con unidades no convencionales",
                "Representación de datos sencillos"
            ],
            "nivel": "básico"
        },
        "Segundo de primaria": {
            "temas": [
                "Números hasta el 1000 y su descomposición",
                "Suma y resta con llevadas",
                "Introducción a la multiplicación como suma repetida",
                "Medición de longitud, peso y capacidad con unidades estándar",
                "Lectura e interpretación de pictogramas y tablas simples"
            ],
            "nivel": "básico"
        }
    },
    "Ciencias Naturales": {
        "Primero de primaria": {
            "temas": [
                "Características de los seres vivos y su clasificación básica",
                "Partes del cuerpo humano y sus funciones",
                "Diferencias entre seres vivos y objetos inertes",
                "Estado del agua y su ciclo",
                "Importancia de la luz y el calor en la vida diaria",
                "Prácticas de cuidado del medio ambiente"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "Necesidades y características de los seres vivos",
                "Hábitos de higiene y cuidado personal",
                "Propiedades de los materiales y objetos",
                "El agua: estados y usos",
                "Fenómenos naturales y su observación"
            ]
        }
    },
    "Ciencias Sociales": {
        "Primero de primaria": {
            "temas": [
                "Identificación de miembros de la familia y roles",
                "Reconocimiento de la escuela y sus espacios",
                "Ubicación espacial: izquierda, derecha, cerca, lejos",
                "Diferenciación entre pasado, presente y futuro",
                "Símbolos patrios y su significado",
                "Normas de convivencia en el hogar y la escuela"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "Los derechos de los niños",
                "Lugares importantes de la comunidad",
                "La historia familiar: pasado y presente",
                "Orientación espacial: planos y mapas sencillos",
                "Normas sociales y comportamiento ciudadano"
            ]
        }
    },
    "Educación Artística": {
        "Primero de primaria": {
            "temas": [
                "Dibujo y pintura: técnicas básicas",
                "Reconocimiento de colores primarios y secundarios",
                "Estilos artísticos sencillos: formas, figuras y líneas",
                "El arte en el entorno",
                "Expresión artística individual y en grupo"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "Exploración de texturas, formas y colores",
                "Interpretación de obras artísticas sencillas",
                "Creación de composiciones con diferentes materiales",
                "El cuerpo y el movimiento en la expresión artística",
                "Valoración de producciones propias y ajenas"
            ]
        }
    },
    "Ética y Valores": {
        "Primero de primaria": {
            "temas": [
                "Valores fundamentales: respeto, responsabilidad, honestidad",
                "La importancia de la amistad y el trabajo en equipo",
                "Normas de convivencia en el hogar y la escuela",
                "Empatía y respeto por los demás",
                "La importancia del cuidado del medio ambiente"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "La importancia de la verdad y la justicia",
                "Resolución pacífica de conflictos",
                "El respeto por la diversidad",
                "Actitudes responsables en la casa y la escuela",
                "Convivencia con normas y acuerdos"
            ]
        }
    },
    "Educación Física": {
        "Primero de primaria": {
            "temas": [
                "Desarrollo de habilidades motrices básicas: correr, saltar, lanzar",
                "Juegos cooperativos y competitivos",
                "Cuidado del cuerpo y hábitos saludables",
                "Importancia de la actividad física diaria",
                "Trabajo en equipo a través del deporte"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "Coordinación y equilibrio en actividades físicas",
                "Juegos tradicionales y recreativos",
                "Rutinas de cuidado del cuerpo y alimentación saludable",
                "Participación activa y respetuosa en juegos de grupo",
                "Valoración del ejercicio como hábito de vida"
            ]
        }
    },
    "Religión": {
        "Primero de primaria": {
            "temas": [
                "Los valores de la religión: amor, respeto, paz",
                "La importancia de la solidaridad y el servicio al prójimo",
                "Principales enseñanzas de Jesús",
                "Respeto por las creencias religiosas de los demás",
                "El valor de la oración y la meditación"
            ]
        },
        "Segundo de primaria": {
            "temas": [
                "Relatos bíblicos y su enseñanza",
                "La familia como lugar de amor y respeto",
                "El perdón y la reconciliación",
                "Celebraciones religiosas importantes",
                "Convivencia basada en el amor y el respeto"
            ]
        }
    }
}
    return temas.get(materia, {}).get(grado, {})

def main():
    st.set_page_config(page_title="Educa Antioquia", layout="wide")

    st.markdown("""<style>
        .materia-card {
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
            text-align: center;
        }
        .emoji-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
    </style>""", unsafe_allow_html=True)
    
    st.title("Educa Antioquia")

    grados = {
        "Primero de primaria": 1,
        "Segundo de primaria": 2,
        "Decimo de secundaria": 10,
        "Once de secundaria": 11
    }

    grado_nombre = st.selectbox("Selecciona el grado:", list(grados.keys()))
    grado_valor = grados[grado_nombre]
    
    materias = get_materias_por_grado(grado_valor)

    cols = st.columns(4)
    for idx, (materia, info) in enumerate(materias.items()):
        with cols[idx % 4]:
            st.markdown(f"""
                <div class="materia-card" style="background-color: {info['color']}">
                    <div class="emoji-icon">{info['emoji']}</div>
                    <h3>{materia}</h3>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seleccionar {materia}", key=materia):
                st.session_state.materia_actual = materia

    if 'materia_actual' in st.session_state:
        st.subheader(f"Temas de {st.session_state.materia_actual}")
        temas_info = get_temas_por_materia_y_grado(st.session_state.materia_actual, grado_nombre)

        if temas_info and 'temas' in temas_info:
            tema_seleccionado = st.selectbox("Selecciona un tema:", temas_info['temas'])
            
            if tema_seleccionado:
                prompt = (
                    f"Eres un profesor de primaria. Explica a un niño pequeño el tema '{tema_seleccionado}', el niño es de grado {grado_nombre}. "
                    "No uses conceptos avanzados. "
                    "Da una explicación clara y sencilla. "
                    "Incluye un ejemplo práctico fácil de entender. "
                    "Propón una actividad corta para practicar. "
                    "Termina con dos preguntas fáciles para comprobar si entendió. "
                    "Responde solo con la explicación, ejemplo, actividad y preguntas, en español, usando palabras simples."
                )
                if st.button("Generar contenido"):
                    with st.spinner("Generando contenido educativo..."):
                        contenido = get_ai_response(prompt)
                        st.write(contenido)
        else:
            st.warning("No hay temas disponibles para esta materia y grado.")

    # Sección de preguntas/chat
    st.markdown("---")
    st.subheader("¿Tienes dudas? Pregúntame")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Escribe tu pregunta aquí"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = get_ai_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
