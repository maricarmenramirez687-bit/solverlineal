import streamlit as st
import re
import random

# Configuración de la página
st.set_page_config(
    page_title="Resolvedor de Ecuaciones de Primer Grado",
    page_icon="🧮",
    layout="centered"
)

# Título y descripción
st.title("🧮 Resolvedor de Ecuaciones de Primer Grado")
st.markdown("""
Esta aplicación resuelve ecuaciones de primer grado de la forma:
**ax + b = c**
""")

# Función para resolver ecuaciones de primer grado
def resolver_ecuacion(ecuacion):
    # Patrón para reconocer ecuaciones de primer grado
    patron = r'^(-?\d*)x\s*([+-]\s*\d+)?\s*=\s*(-?\d+)$'
    match = re.match(patron, ecuacion.replace(" ", ""))
    
    if not match:
        return None, "Formato incorrecto. Usa: ax + b = c"
    
    # Extraer coeficientes
    a_str, b_str, c_str = match.groups()
    
    # Convertir coeficiente a
    if a_str == "" or a_str == "-":
        a = -1 if a_str == "-" else 1
    else:
        a = int(a_str)
    
    # Convertir coeficiente b (si existe)
    b = 0
    if b_str:
        # Eliminar espacios y convertir
        b_str = b_str.replace(" ", "")
        if b_str.startswith('+'):
            b = int(b_str[1:]) if b_str[1:] else 1
        else:
            b = int(b_str) if b_str else 1
    
    # Convertir coeficiente c
    c = int(c_str)
    
    # Resolver ecuación: x = (c - b) / a
    if a == 0:
        return None, "No es una ecuación de primer grado (a no puede ser 0)"
    
    solucion = (c - b) / a
    
    # Verificar si la solución es entera
    if solucion.is_integer():
        solucion = int(solucion)
    
    return solucion, f"Ecuación: {a}x + {b} = {c}"

# Función para mostrar globitos de celebración
def mostrar_globitos():
    # Crear HTML/CSS para los globitos
    globitos_html = """
    <style>
    @keyframes flotar {
        0% { transform: translateY(100vh) scale(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) scale(1.5); opacity: 0; }
    }
    
    .globo {
        position: fixed;
        bottom: -50px;
        width: 30px;
        height: 40px;
        background-color: #ff6b6b;
        border-radius: 50%;
        animation: flotar 5s linear infinite;
        z-index: 1000;
    }
    
    .globo::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 5px;
        height: 15px;
        background-color: #ff6b6b;
    }
    
    .globo:nth-child(2n) {
        background-color: #4ecdc4;
        animation-delay: 0.5s;
    }
    
    .globo:nth-child(3n) {
        background-color: #ffe66d;
        animation-delay: 1s;
    }
    
    .globo:nth-child(4n) {
        background-color: #6a0572;
        animation-delay: 1.5s;
    }
    
    .globo:nth-child(5n) {
        background-color: #1a936f;
        animation-delay: 2s;
    }
    </style>
    """
    
    # Añadir los globitos
    for i in range(15):
        left = random.randint(5, 95)
        delay = random.uniform(0, 2)
        size = random.randint(25, 40)
        globitos_html += f"""
        <div class="globo" style="left: {left}%; animation-delay: {delay}s; width: {size}px; height: {size*1.3}px;"></div>
        """
    
    # Mostrar los globitos
    st.markdown(globitos_html, unsafe_allow_html=True)

# Interfaz de usuario
ecuacion = st.text_input(
    "Ingresa tu ecuación (ejemplo: 2x + 3 = 7):",
    placeholder="2x + 3 = 7"
)

if st.button("Resolver"):
    if ecuacion:
        solucion, mensaje = resolver_ecuacion(ecuacion)
        
        if solucion is not None:
            st.success(f"✅ {mensaje}")
            st.info(f"**Solución: x = {solucion}**")
            
            # Guardar la solución en el estado de la sesión
            st.session_state.solucion_correcta = solucion
            st.session_state.ecuacion_resuelta = True
        else:
            st.error(f"❌ {mensaje}")
            st.session_state.ecuacion_resuelta = False
    else:
        st.warning("⚠️ Por favor, ingresa una ecuación.")

# Verificación de la respuesta del usuario
if st.session_state.get('ecuacion_resuelta', False):
    st.markdown("---")
    st.subheader("Verifica tu respuesta")
    
    respuesta_usuario = st.number_input(
        "¿Cuál crees que es el valor de x?",
        step=1,
        value=0
    )
    
    if st.button("Verificar respuesta"):
        if respuesta_usuario == st.session_state.solucion_correcta:
            st.success("🎉 ¡Correcto! ¡Has resuelto la ecuación!")
            mostrar_globitos()
            
            # Mensaje adicional de felicitación
            mensajes_felicidad = [
                "¡Excelente trabajo! 🏆",
                "¡Eres un genio de las matemáticas! 🧠",
                "¡Perfecto! Sigue así 💪",
                "¡Increíble! Nada puede detenerte 🚀",
                "¡Respuesta correcta! Eres fantástico/a 🌟"
            ]
            st.balloons()
            st.success(random.choice(mensajes_felicidad))
        else:
            st.error(f"❌ Incorrecto. La solución correcta es x = {st.session_state.solucion_correcta}")

# Información adicional
st.markdown("---")
st.markdown("""
### ¿Cómo usar esta aplicación?
1. Ingresa una ecuación de primer grado en el formato: **ax + b = c**
2. Haz clic en "Resolver" para ver la solución
3. Intenta resolverla por tu cuenta e ingresa tu respuesta
4. Haz clic en "Verificar respuesta" para comprobar si es correcta

### Ejemplos de ecuaciones válidas:
- `2x + 3 = 7`
- `-x - 5 = 10`
- `3x = 9`
- `x - 4 = 0`
- `5x + 2 = -3`
""")

# Nota al pie
st.markdown("---")
st.caption("Creado con Streamlit | Resolvedor de ecuaciones de primer grado")
