import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw

# Parámetros de la simulación
width, height = 640, 480
robot_pos = [width // 2, height // 2]
goal_pos = [np.random.randint(0, width), np.random.randint(0, height)]

# Velocidad del robot
speed = st.sidebar.slider("Velocidad del robot", 1, 20, 5)

# Cargar la imagen de fondo
background_image_path = 'portada.webp'
background_image = Image.open(background_image_path).resize((width, height))

# Simulación simple de movimiento del robot
def move_robot_towards_goal(robot_pos, goal_pos, speed):
    direction = np.array(goal_pos) - np.array(robot_pos)
    distance = np.linalg.norm(direction)
    
    if distance < speed:
        return goal_pos  # Si estamos cerca del objetivo, no nos movemos más allá de él
    
    direction = direction / distance * speed  # Normalizar y escalar según la velocidad
    new_robot_pos = np.array(robot_pos) + direction
    return new_robot_pos.tolist()

# Función para dibujar el entorno
def draw_environment(robot_pos, goal_pos, background_image):
    # Crear una copia de la imagen de fondo
    env = background_image.copy()
    draw = ImageDraw.Draw(env)
    
    # Dibujar el objetivo y el robot
    draw.ellipse((goal_pos[0] - 10, goal_pos[1] - 10, goal_pos[0] + 10, goal_pos[1] + 10), fill=(0, 255, 0))  # Objetivo en verde
    draw.ellipse((robot_pos[0] - 10, robot_pos[1] - 10, robot_pos[0] + 10, robot_pos[1] + 10), fill=(0, 0, 255))  # Robot en azul
    draw.line((robot_pos[0], robot_pos[1], goal_pos[0], goal_pos[1]), fill=(255, 255, 255), width=1)  # Línea blanca entre robot y objetivo
    
    return env

st.title("Simulación de Navegación Autónoma de un Robot")
st.write("Esta aplicación simula un robot móvil que navega de manera autónoma hacia una meta.")

start_simulation = st.button("Iniciar Simulación")

if st.button("Reiniciar"):
    robot_pos = [width // 2, height // 2]
    goal_pos = [np.random.randint(0, width), np.random.randint(0, height)]

# Controles manuales para mover el objetivo
new_goal_x = st.sidebar.slider("Nueva posición X del objetivo", 0, width, goal_pos[0])
new_goal_y = st.sidebar.slider("Nueva posición Y del objetivo", 0, height, goal_pos[1])

# Actualizar la posición del objetivo
if st.sidebar.button("Actualizar posición del objetivo"):
    goal_pos = [new_goal_x, new_goal_y]

# Calcular la distancia al objetivo
distance_to_goal = np.linalg.norm(np.array(goal_pos) - np.array(robot_pos))
st.sidebar.write(f"Distancia al objetivo: {distance_to_goal:.2f} píxeles")

# Crear un contenedor para la imagen de la simulación
image_container = st.empty()

if start_simulation:
    while np.linalg.norm(np.array(goal_pos) - np.array(robot_pos)) > speed:
        robot_pos = move_robot_towards_goal(robot_pos, goal_pos, speed)
        env = draw_environment(robot_pos, goal_pos, background_image)
        image_container.image(env, use_column_width=True)
        time.sleep(0.05)  # Pausa para hacer el movimiento más suave

# Dibujar el entorno final
env = draw_environment(robot_pos, goal_pos, background_image)
image_container.image(env, use_column_width=True)
