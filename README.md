# Gartic Animator Pro - Premium Edition 🎨🎞️

Una aplicación de escritorio potente y divertida para crear animaciones **Stop Motion**, desarrollada complemente en Python. Este proyecto destaca por el uso de una **Estructura de Datos Lineal (Lista Doblemente Enlazada)** personalizada para gestionar la secuencia de fotogramas, demostrando la aplicación práctica de conceptos de ingeniería de software en una interfaz gráfica moderna inspirada en *Gartic Phone*.

## 🚀 Características Principales

- **Motor de Lista Doblemente Enlazada**: Implementación desde cero de una `DoublyLinkedList` para una navegación fluida, inserción y eliminación de fotogramas en tiempo real.
- **Interfaz Premium Rediseñada**: Bordes redondeados, botones personalizados con micro-animaciones y un elegante "Modo Oscuro" en los paneles para mayor contraste.
- **Onion Skinning (Piel de Cebolla)**: Visualiza una silueta tenue del cuadro anterior mientras dibujas el actual para crear movimientos perfectos.
- **Control de Velocidad (FPS)**: Ajusta la rapidez de tu animación con un deslizador intuitivo.
- **Herramientas de Dibujo Pro**:
  - Paleta de 12 colores vibrantes.
  - Ajuste de grosor del pincel.
  - **Deshacer (Undo)** y **Rehacer (Redo)** completos por cada trazo.
- **Integración Multimedia**: Sube tus propias fotos (JPG, PNG, etc.) para usarlas como fondo o fotogramas base.
- **Exportación a GIF**: Descarga tus animaciones terminadas como archivos `.gif` animados de alta calidad, listos para compartir.
- **Pizarra Estilo Cuaderno**: Lienzo de dibujo con estética de bloc de notas para una experiencia creativa única.

## 🛠️ Requisitos Técnico

Para ejecutar esta aplicación, necesitarás:

- **Python 3.x**
- **Bibliotecas**:
  - `tkinter` (incluida en la mayoría de las instalaciones de Python).
  - `Pillow` (para el manejo de imágenes y exportación a GIF).

### Instalación de Dependencias

Si no tienes Pillow instalado, puedes obtenerlo fácilmente con:

```bash
pip install Pillow
```

## 🎮 Cómo Usar

1. **Dibuja**: Usa el ratón para crear tus diseños en el lienzo central. Puedes cambiar el color y el tamaño del pincel en el panel izquierdo.
2. **Gestiona Cuadros**: Usa los botones delanteros/traseros (`⏮️`, `⏭️`) para moverte y el botón `➕` para crear un nuevo fotograma.
3. **Sube Fotos**: Usa el icono de imagen (`🖼️`) para cargar una foto de fondo en el cuadro actual.
4. **Edita**: Si te equivocas, usa los botones de `↩️ Deshacer` situados debajo del tablero.
5. **Finaliza**: ¡Presiona el gran botón verde de **REPRODUCIR** para ver tu magia o **DESCARGAR GIF** para guardar tu obra maestra!

## 🧠 Estructura del Código

El corazón de la aplicación es la clase `DoublyLinkedList`, que permite:
- **Nodos Inteligentes**: Cada `Node` almacena sus propios trazos (strokes), imagen de fondo y el historial local para deshacer.
- **O(1) Operaciones**: Las inserciones y eliminaciones de fotogramas son extremadamente eficientes.
- **Código Limpio**: La lógica del motor de datos está escrita en inglés siguiendo estándares profesionales, mientras que la interfaz de usuario está totalmente en español.

---
Desarrollado con ❤️ para entusiastas de la animación y las estructuras de datos.
