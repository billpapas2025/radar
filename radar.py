import streamlit as st
import numpy as np
import cv2
import time
from PIL import Image

# Parámetros de la simulación
width, height = 640, 480
robot_pos = [width // 2, height // 2]
goal_pos = [np.random.randint(0, width), np.random.randint(0, height)]

# Velocidad del robot
speed = st.sidebar.slider("Velocidad del robot", 1, 20, 5)

# Cargar la imagen de fondo
background_image_path = 'portada.webp'
background_image = cv2.imread(background_image_path)
background_image = cv2.resize(background_image, (width, height))

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
    
    # Dibujar el objetivo y el robot
    cv2.circle(env, (int(goal_pos[0]), int(goal_pos[1])), 10, (0, 255, 0), -1)  # Objetivo en verde
    cv2.circle(env, (int(robot_pos[0]), int(robot_pos[1])), 10, (255, 0, 0), -1)  # Robot en azul
    cv2.line(env, (int(robot_pos[0]), int(robot_pos[1])), (int(goal_pos[0]), int(goal_pos[1])), (255, 255, 255), 1)  # Línea blanca entre robot y objetivo
    
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
        image_container.image(env, channels="BGR")
        time.sleep(0.05)  # Pausa para hacer el movimiento más suave

# Dibujar el entorno final
env = draw_environment(robot_pos, goal_pos, background_image)
image_container.image(env, channels="BGR")
