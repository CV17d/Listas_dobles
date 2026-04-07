import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

# --- Custom Doubly Linked List Engine ---

class Node:
    """
    Represents a single frame in the animation sequence.
    Stores drawing data (strokes), image backgrounds, and list pointers.
    """
    def __init__(self, data=None):
        # data will store a list of: {'coords': (x1,y1,x2,y2), 'color': '#hex', 'size': int}
        self.strokes = data if data is not None else []  
        self.undone_strokes = [] # Stack for redo functionality
        self.image_data = None  # Original PIL image
        self.photo_ref = None   # Ref for Tkinter display
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """
    The core engine managing the sequence of animation frames.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return new_node

    def insert_after(self, current_node, data):
        if not current_node:
            return self.append(data)
        new_node = Node(data)
        new_node.next = current_node.next
        new_node.prev = current_node
        if current_node.next:
            current_node.next.prev = new_node
        else:
            self.tail = new_node
        current_node.next = new_node
        self.size += 1
        return new_node

    def remove(self, node):
        if not node: return None
        next_to_show = node.next if node.next else node.prev
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev
        self.size -= 1
        return next_to_show

# --- Modern UI Application (Gartic Phone Theme) ---

class GarticStopMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gartic Animator Pro")
        self.root.geometry("1100x750")
        
        # Colors (Gartic Theme)
        self.bg_main = "#ff4757"      # Vibrant watermelon pink
        self.bg_sidebar = "#5a189a"   # Deep purple
        self.bg_canvas_bg = "#3d0066" # Very dark purple
        self.accent_color = "#ffffff" # White
        self.palette_colors = [
            "#000000", "#ffffff", "#ff4757", "#2f3542",
            "#2ed573", "#1e90ff", "#ffa502", "#5352ed",
            "#747d8c", "#a4b0be", "#ff6b81", "#70a1ff"
        ]

        # Drawing state
        self.current_color = "#000000"
        self.current_size = 5
        self.last_x, self.last_y = None, None
        
        # Core Engine
        self.frame_list = DoublyLinkedList()
        self.current_frame_node = self.frame_list.append([])
        self.current_frame_index = 1

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        self.root.config(bg=self.bg_main)
        
        # 1. Header (Status)
        self.header = tk.Frame(self.root, bg=self.bg_main, pady=10)
        self.header.pack(fill=tk.X)
        self.status_label = tk.Label(
            self.header, text=f"{self.current_frame_index} / {self.frame_list.size}",
            font=("Luckiest Guy", 28, "bold"), fg="white", bg=self.bg_main
        )
        self.status_label.pack()

        # Main horizontal container
        self.root_container = tk.Frame(self.root, bg=self.bg_main)
        self.root_container.pack(fill=tk.BOTH, expand=True, padx=20)

        # 2. Left Sidebar (Colors)
        self.left_panel = tk.Frame(self.root_container, bg=self.bg_sidebar, padx=10, pady=10)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        tk.Label(self.left_panel, text="COLORES", font=("Arial", 10, "bold"), bg=self.bg_sidebar, fg="white").pack(pady=5)
        
        # Color Grid
        self.color_grid = tk.Frame(self.left_panel, bg=self.bg_sidebar)
        self.color_grid.pack()
        
        for i, color in enumerate(self.palette_colors):
            r, c = i // 2, i % 2
            btn = tk.Frame(self.color_grid, bg=color, width=40, height=40, relief=tk.RAISED, borderwidth=2)
            btn.grid(row=r, column=c, padx=5, pady=5)
            btn.bind("<Button-1>", lambda e, clr=color: self.set_color(clr))

        # Size Slider
        tk.Label(self.left_panel, text="TAMAÑO", font=("Arial", 10, "bold"), bg=self.bg_sidebar, fg="white").pack(pady=(20, 5))
        self.size_slider = tk.Scale(
            self.left_panel, from_=2, to=30, orient=tk.VERTICAL, bg=self.bg_sidebar, 
            fg="white", highlightthickness=0, command=self.set_size
        )
        self.size_slider.set(self.current_size)
        self.size_slider.pack(fill=tk.Y, expand=True)

        # 3. Central Canvas (Notebook Style)
        self.middle_container = tk.Frame(self.root_container, bg=self.bg_main)
        self.middle_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # The "Notebook" Frame
        self.notebook_frame = tk.Frame(self.middle_container, bg="#ffffff", padx=10, pady=10)
        self.notebook_frame.pack(pady=10)
        
        # Decoration for Notebook rings
        self.rings_frame = tk.Frame(self.notebook_frame, bg="#ffffff")
        self.rings_frame.pack(fill=tk.X)
        for _ in range(8):
            tk.Label(self.rings_frame, text="OO", font=("Arial", 12, "bold"), fg="#cccccc", bg="white").pack(side=tk.LEFT, expand=True)

        self.canvas = tk.Canvas(
            self.notebook_frame, bg="white", width=700, height=450, 
            highlightthickness=0, cursor="pencil"
        )
        self.canvas.pack()

        # New: Undo/Redo Bar below the canvas
        self.canvas_controls = tk.Frame(self.middle_container, bg=self.bg_main, pady=10)
        self.canvas_controls.pack(fill=tk.X)
        
        btn_style = {"font": ("Arial", 12, "bold"), "width": 12, "bg": "#7d2ae8", "fg": "white", "relief": tk.RAISED}
        
        self.btn_undo = tk.Button(self.canvas_controls, text="↩️ Deshacer", command=self.undo, **btn_style)
        self.btn_undo.pack(side=tk.LEFT, expand=True, padx=5)
        
        self.btn_redo = tk.Button(self.canvas_controls, text="↪️ Rehacer", command=self.redo, **btn_style)
        self.btn_redo.pack(side=tk.LEFT, expand=True, padx=5)

        # 4. Right Sidebar (Actions)
        self.right_panel = tk.Frame(self.root_container, bg=self.bg_sidebar, padx=10, pady=10)
        self.right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 0))
        
        actions = [
            ("Anterior", "⏮️", self.prev_frame),
            ("Siguiente", "⏭️", self.next_frame),
            ("Nuevo", "➕", self.add_frame),
            ("Subir Foto", "🖼️", self.upload_image),
            ("Borrar", "🗑️", self.delete_frame)
        ]
        
        for name, emoji, cmd in actions:
            btn = tk.Button(
                self.right_panel, text=f"{emoji}\n{name}", command=cmd, 
                font=("Arial", 10, "bold"), width=10, height=3, 
                bg="#7d2ae8", fg="white", relief=tk.FLAT, activebackground="#9d4edd"
            )
            btn.pack(pady=8)

        # 5. Bottom Bar (Play button)
        self.footer = tk.Frame(self.root, bg=self.bg_main, pady=20)
        self.footer.pack(fill=tk.X)
        
        self.btn_play = tk.Button(
            self.footer, text="▶️ REPRODUCIR", command=self.play_animation,
            font=("Luckiest Guy", 18), bg="#2ed573", fg="white", width=15, pady=5,
            relief=tk.RAISED, borderwidth=3
        )
        self.btn_play.pack(side=tk.LEFT, expand=True, padx=10)

        self.btn_download = tk.Button(
            self.footer, text="📥 DESCARGAR GIF", command=self.export_gif,
            font=("Luckiest Guy", 18), bg="#1e90ff", fg="white", width=15, pady=5,
            relief=tk.RAISED, borderwidth=3
        )
        self.btn_download.pack(side=tk.LEFT, expand=True, padx=10)

    def set_color(self, color):
        self.current_color = color
        # Alert removed as requested

    def set_size(self, size):
        self.current_size = int(size)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    # --- Drawing Logic ---

    def start_drawing(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke_data = []

    def draw(self, event):
        if self.last_x and self.last_y:
            x, y = event.x, event.y
            self.canvas.create_line(
                self.last_x, self.last_y, x, y, 
                width=self.current_size, fill=self.current_color,
                capstyle=tk.ROUND, smooth=tk.TRUE
            )
            # Add to temporary stroke buffer
            self.current_stroke_data.append({
                'coords': (self.last_x, self.last_y, x, y),
                'color': self.current_color,
                'size': self.current_size
            })
            self.last_x, self.last_y = x, y

    def stop_drawing(self, event):
        if self.current_stroke_data:
            # Add the ENTIRE stroke to the history
            self.current_frame_node.strokes.append(list(self.current_stroke_data))
            self.current_frame_node.undone_strokes.clear()
        self.last_x, self.last_y = None, None

    # --- Engine Logic ---

    def update_display(self):
        self.canvas.delete("all")
        
        # 1. Draw image background
        if self.current_frame_node.image_data:
            img = self.current_frame_node.image_data
            cw, ch = int(self.canvas.cget("width")), int(self.canvas.cget("height"))
            iw, ih = img.size
            ratio = min(cw/iw, ch/ih)
            new_size = (int(iw*ratio), int(ih*ratio))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            self.current_frame_node.photo_ref = ImageTk.PhotoImage(resized)
            self.canvas.create_image(cw/2, ch/2, image=self.current_frame_node.photo_ref, anchor=tk.CENTER)

        # 2. Draw strokes on top (iterate through nested list)
        for stroke in self.current_frame_node.strokes:
            for s in stroke:
                self.canvas.create_line(
                    s['coords'][0], s['coords'][1], s['coords'][2], s['coords'][3],
                    width=s['size'], fill=s['color'], capstyle=tk.ROUND, smooth=tk.TRUE
                )
            
        self.status_label.config(text=f"{self.current_frame_index} / {self.frame_list.size}")

    def prev_frame(self):
        if self.current_frame_node.prev:
            self.current_frame_node = self.current_frame_node.prev
            self.current_frame_index -= 1
            self.update_display()

    def next_frame(self):
        if self.current_frame_node.next:
            self.current_frame_node = self.current_frame_node.next
            self.current_frame_index += 1
            self.update_display()

    def add_frame(self):
        new_node = self.frame_list.insert_after(self.current_frame_node, [])
        self.current_frame_node = new_node
        self.current_frame_index += 1
        self.update_display()

    def delete_frame(self):
        if self.frame_list.size <= 1:
            self.current_frame_node.strokes = []
            self.current_frame_node.image_data = None
            self.update_display()
            return
        node_to_del = self.current_frame_node
        res = self.frame_list.remove(node_to_del)
        if node_to_del.prev is None: self.current_frame_index = 1
        else:
            if node_to_del.next is None: self.current_frame_index -= 1
        self.current_frame_node = res
        self.update_display()

    def upload_image(self):
        file = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file:
            try:
                self.current_frame_node.image_data = Image.open(file)
                self.update_display()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    def undo(self):
        """Removes the last stroke and adds it to the undone stack."""
        if self.current_frame_node.strokes:
            last_stroke = self.current_frame_node.strokes.pop()
            self.current_frame_node.undone_strokes.append(last_stroke)
            self.update_display()

    def redo(self):
        """Adds back the last undone stroke."""
        if self.current_frame_node.undone_strokes:
            last_undone = self.current_frame_node.undone_strokes.pop()
            self.current_frame_node.strokes.append(last_undone)
            self.update_display()

    def play_animation(self):
        self.btn_play.config(state=tk.DISABLED)
        self.playback_traverse(self.frame_list.head, 1)

    def playback_traverse(self, node, idx):
        if node:
            self.current_frame_node = node
            self.current_frame_index = idx
            self.update_display()
            self.root.after(200, lambda: self.playback_traverse(node.next, idx + 1))
        else:
            self.btn_play.config(state=tk.NORMAL)
            messagebox.showinfo("Gartic", "¡Animación lista!")

    def export_gif(self):
        """Renders all frames and saves them as an animated GIF."""
        if self.frame_list.size == 0:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF Animado", "*.gif")],
            title="Guardar Animación"
        )
        
        if not file_path:
            return

        try:
            frames = []
            canvas_w = int(self.canvas.cget("width"))
            canvas_h = int(self.canvas.cget("height"))
            
            curr = self.frame_list.head
            while curr:
                # 1. Create base white image
                frame_img = Image.new("RGB", (canvas_w, canvas_h), "white")
                draw = ImageDraw.Draw(frame_img)
                
                # 2. Draw background image if present
                if curr.image_data:
                    img = curr.image_data
                    iw, ih = img.size
                    ratio = min(canvas_w/iw, canvas_h/ih)
                    new_size = (int(iw*ratio), int(ih*ratio))
                    resized = img.resize(new_size, Image.Resampling.LANCZOS)
                    # Paste centered
                    x_off = (canvas_w - new_size[0]) // 2
                    y_off = (canvas_h - new_size[1]) // 2
                    frame_img.paste(resized, (x_off, y_off))
                
                # 3. Draw strokes
                for stroke in curr.strokes:
                    for s in stroke:
                        draw.line(
                            s['coords'], 
                            fill=s['color'], 
                            width=s['size'], 
                            joint="curve"
                        )
                
                frames.append(frame_img)
                curr = curr.next
            
            # 4. Save sequence
            if frames:
                frames[0].save(
                    file_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=200,
                    loop=0,
                    optimize=False
                )
                messagebox.showinfo("Éxito", "¡Animación guardada correctamente!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    # Try to use a better font if available, else standard bold
    try:
        from tkinter import font
        # Define a mock for 'Luckiest Guy' if not installed
        available = font.families()
        if 'Luckiest Guy' not in available:
            # Fallback
            pass
    except: pass
    
    app = GarticStopMotionApp(root)
    root.mainloop()
