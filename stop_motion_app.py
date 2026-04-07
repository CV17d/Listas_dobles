import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

# --- Custom Doubly Linked List Engine ---

class Node:
    def __init__(self, data=None):
        self.strokes = data if data is not None else []  
        self.undone_strokes = [] 
        self.image_data = None  
        self.photo_ref = None   
        self.prev = None
        self.next = None

class DoublyLinkedList:
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
        if not current_node: return self.append(data)
        new_node = Node(data)
        new_node.next = current_node.next
        new_node.prev = current_node
        if current_node.next: current_node.next.prev = new_node
        else: self.tail = new_node
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

# --- Custom UI Components ---

class CustomButton(tk.Canvas):
    """
    A premium, rounded button with hover effects and animations.
    """
    def __init__(self, parent, text, command, color="#7d2ae8", hover_color="#9d4edd", text_color="white", width=120, height=45):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, cursor="hand2")
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        
        self.rect = self.draw_rounded_rect(5, 5, width-5, height-5, 10, fill=color)
        self.label = self.create_text(width/2, height/2, text=text, fill=text_color, font=("Arial", 10, "bold"))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color)

    def on_click(self, event):
        self.command()

# --- Gartic Animator Pro (Premium Edition) ---

class GarticAnimatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Gartic Animator Pro - Premium Edition")
        self.root.geometry("1200x850")
        
        # Premium Palette
        self.bg_main = "#ff4757"       # Vibrant watermelon
        self.bg_sidebar = "#2c1e3e"    # Darker, more professional purple
        self.accent_color = "#ffffff"
        self.onion_skin_color = "#e0e0e0" # Faint gray for onion skin
        self.palette = [
            "#000000", "#7f8c8d", "#ffffff", "#ff4757", 
            "#2ed573", "#1e90ff", "#ffa502", "#5352ed", 
            "#e84393", "#00d2d3", "#f9ca24", "#6c5ce7"
        ]

        # Engine & App State
        self.frame_list = DoublyLinkedList()
        self.current_frame_node = self.frame_list.append([])
        self.current_frame_index = 1
        self.current_color = "#000000"
        self.current_size = 5
        self.onion_skin_enabled = tk.BooleanVar(value=True)
        self.playback_speed = tk.IntVar(value=200) # ms delay
        
        self.last_x, self.last_y = None, None
        self.current_stroke_data = []

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        self.root.config(bg=self.bg_main)
        
        # 1. Header
        self.header = tk.Frame(self.root, bg=self.bg_main, pady=15)
        self.header.pack(fill=tk.X)
        self.status_label = tk.Label(
            self.header, text=f"CUADRO {self.current_frame_index} / {self.frame_list.size}",
            font=("Arial", 32, "bold"), fg="white", bg=self.bg_main
        )
        self.status_label.pack()

        # Main Layout
        self.main_container = tk.Frame(self.root, bg=self.bg_main)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30)

        # 2. Left Sidebar (Palette & Settings)
        self.left_panel = tk.Frame(self.main_container, bg=self.bg_sidebar, padx=15, pady=20)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 25))
        
        tk.Label(self.left_panel, text="HERRAMIENTAS", font=("Arial", 12, "bold"), bg=self.bg_sidebar, fg="#ff7f50").pack(pady=(0, 15))
        
        # Color Palette
        self.color_grid = tk.Frame(self.left_panel, bg=self.bg_sidebar)
        self.color_grid.pack()
        for i, color in enumerate(self.palette):
            r, c = i // 2, i % 2
            f = tk.Frame(self.color_grid, bg=color, width=40, height=40, cursor="hand2")
            f.grid(row=r, column=c, padx=4, pady=4)
            f.bind("<Button-1>", lambda e, clr=color: self.set_color(clr))

        # Size Slider
        tk.Label(self.left_panel, text="GROSOR", font=("Arial", 10, "bold"), bg=self.bg_sidebar, fg="white").pack(pady=(25, 5))
        self.size_scale = tk.Scale(
            self.left_panel, from_=2, to=30, orient=tk.HORIZONTAL, bg=self.bg_sidebar, 
            fg="white", highlightthickness=0, command=self.set_size
        )
        self.size_scale.set(self.current_size)
        self.size_scale.pack(fill=tk.X)

        # Onion Skin Toggle
        tk.Checkbutton(
            self.left_panel, text="Onion Skin", variable=self.onion_skin_enabled,
            bg=self.bg_sidebar, fg="white", selectcolor=self.bg_sidebar, 
            activebackground=self.bg_sidebar, font=("Arial", 10), command=self.update_display
        ).pack(pady=(30, 0))

        # 3. Middle Area (Canvas)
        self.middle_panel = tk.Frame(self.main_container, bg=self.bg_main)
        self.middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Styled Notebook Container
        self.notebook_outer = tk.Frame(self.middle_panel, bg="#000000", padx=2, pady=2)
        self.notebook_outer.pack(pady=10)
        
        self.notebook_inner = tk.Frame(self.notebook_outer, bg="white", padx=15, pady=15)
        self.notebook_inner.pack()
        
        # Decoration (Paper rings)
        self.rings = tk.Frame(self.notebook_inner, bg="white")
        self.rings.pack(fill=tk.X)
        for _ in range(12):
            tk.Label(self.rings, text="➰", font=("Arial", 10), fg="#bdc3c7", bg="white").pack(side=tk.LEFT, expand=True)

        self.canvas = tk.Canvas(
            self.notebook_inner, bg="white", width=750, height=500, 
            highlightthickness=0, cursor="pencil"
        )
        self.canvas.pack()

        # Canvas Undo/Redo Bar
        self.canvas_actions = tk.Frame(self.middle_panel, bg=self.bg_main, pady=15)
        self.canvas_actions.pack(fill=tk.X)
        
        CustomButton(self.canvas_actions, "↩️ Deshacer", self.undo, width=140).pack(side=tk.LEFT, expand=True)
        CustomButton(self.canvas_actions, "↪️ Rehacer", self.redo, width=140).pack(side=tk.LEFT, expand=True)

        # 4. Right Sidebar (Project Tools)
        self.right_panel = tk.Frame(self.main_container, bg=self.bg_sidebar, padx=15, pady=20)
        self.right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(25, 0))
        
        tk.Label(self.right_panel, text="PROYECTO", font=("Arial", 12, "bold"), bg=self.bg_sidebar, fg="#0fbcf9").pack(pady=(0, 15))
        
        tool_btns = [
            ("Anterior", "⏮️", self.prev_frame),
            ("Siguiente", "⏭️", self.next_frame),
            ("Nuevo", "➕", self.add_frame),
            ("Foto", "🖼️", self.upload_image),
            ("Borrar", "🗑️", self.delete_frame)
        ]
        
        for name, emoji, cmd in tool_btns:
            CustomButton(self.right_panel, f"{emoji} {name}", cmd, color="#4834d4", hover_color="#686de0", width=120, height=55).pack(pady=8)
            
        # 5. Footer (Playback Controls)
        self.footer = tk.Frame(self.root, bg=self.bg_main, pady=25)
        self.footer.pack(fill=tk.X)
        
        # Speed Control
        self.speed_bar = tk.Frame(self.footer, bg=self.bg_main)
        self.speed_bar.pack(pady=(0, 15))
        tk.Label(self.speed_bar, text="VELOCIDAD (FPS)", font=("Arial", 10, "bold"), bg=self.bg_main, fg="white").pack(side=tk.LEFT, padx=10)
        self.speed_scale = tk.Scale(
            self.speed_bar, from_=50, to=500, orient=tk.HORIZONTAL, bg=self.bg_main, 
            fg="white", highlightthickness=0, resolution=50, showvalue=False, variable=self.playback_speed
        )
        self.speed_scale.pack(side=tk.LEFT)

        CustomButton(self.footer, "▶️ REPRODUCIR", self.play_animation, color="#2ed573", hover_color="#7bed9f", width=250, height=60).pack(side=tk.LEFT, expand=True, padx=20)
        CustomButton(self.footer, "📥 DESCARGAR GIF", self.export_gif, color="#1e90ff", hover_color="#70a1ff", width=250, height=60).pack(side=tk.LEFT, expand=True, padx=20)

    # --- Methods ---

    def set_color(self, color): self.current_color = color
    def set_size(self, size): self.current_size = int(size)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke_data = []

    def draw(self, event):
        if self.last_x and self.last_y:
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, width=self.current_size, fill=self.current_color, capstyle=tk.ROUND, smooth=True)
            self.current_stroke_data.append({'coords': (self.last_x, self.last_y, x, y), 'color': self.current_color, 'size': self.current_size})
            self.last_x, self.last_y = x, y

    def stop_drawing(self, event):
        if self.current_stroke_data:
            self.current_frame_node.strokes.append(list(self.current_stroke_data))
            self.current_frame_node.undone_strokes.clear()
        self.last_x, self.last_y = None, None

    def update_display(self, show_onion=True):
        self.canvas.delete("all")
        cw, ch = int(self.canvas.cget("width")), int(self.canvas.cget("height"))

        # 1. Onion Skin (Previous frame in ghost mode)
        if show_onion and self.onion_skin_enabled.get() and self.current_frame_node.prev:
            prev = self.current_frame_node.prev
            for stroke in prev.strokes:
                for s in stroke:
                    self.canvas.create_line(s['coords'], width=s['size'], fill=self.onion_skin_color, capstyle=tk.ROUND, smooth=True)

        # 2. Background Image
        if self.current_frame_node.image_data:
            img = self.current_frame_node.image_data
            iw, ih = img.size
            ratio = min(cw/iw, ch/ih)
            new_size = (int(iw*ratio), int(ih*ratio))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            self.current_frame_node.photo_ref = ImageTk.PhotoImage(resized)
            self.canvas.create_image(cw/2, ch/2, image=self.current_frame_node.photo_ref, anchor=tk.CENTER)

        # 3. Current Strokes
        for stroke in self.current_frame_node.strokes:
            for s in stroke:
                self.canvas.create_line(s['coords'], width=s['size'], fill=s['color'], capstyle=tk.ROUND, smooth=True)
            
        self.status_label.config(text=f"CUADRO {self.current_frame_index} / {self.frame_list.size}")

    # Navigation & Core Logic
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
        self.current_frame_node = self.frame_list.insert_after(self.current_frame_node, [])
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

    def undo(self):
        if self.current_frame_node.strokes:
            self.current_frame_node.undone_strokes.append(self.current_frame_node.strokes.pop())
            self.update_display()

    def redo(self):
        if self.current_frame_node.undone_strokes:
            self.current_frame_node.strokes.append(self.current_frame_node.undone_strokes.pop())
            self.update_display()

    def upload_image(self):
        file = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file:
            try:
                self.current_frame_node.image_data = Image.open(file)
                self.update_display()
            except Exception as e: messagebox.showerror("Error", f"Error: {e}")

    def play_animation(self):
        self.playback_traverse(self.frame_list.head, 1)

    def playback_traverse(self, node, idx):
        if node:
            self.current_frame_node = node
            self.current_frame_index = idx
            self.update_display(show_onion=False) # No onion skin during playback
            self.root.after(self.playback_speed.get(), lambda: self.playback_traverse(node.next, idx + 1))
        else: messagebox.showinfo("Gartic", "¡Exportación en pantalla lista!")

    def export_gif(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if not file_path: return
        try:
            frames = []
            canvas_w, canvas_h = int(self.canvas.cget("width")), int(self.canvas.cget("height"))
            curr = self.frame_list.head
            while curr:
                frame_img = Image.new("RGB", (canvas_w, canvas_h), "white")
                draw = ImageDraw.Draw(frame_img)
                if curr.image_data:
                    img = curr.image_data
                    iw, ih = img.size
                    ratio = min(canvas_w/iw, canvas_h/ih)
                    new_size = (int(iw*ratio), int(ih*ratio))
                    resized = img.resize(new_size, Image.Resampling.LANCZOS)
                    frame_img.paste(resized, ((canvas_w - new_size[0]) // 2, (canvas_h - new_size[1]) // 2))
                for stroke in curr.strokes:
                    for s in stroke: draw.line(s['coords'], fill=s['color'], width=s['size'], joint="curve")
                frames.append(frame_img)
                curr = curr.next
            if frames:
                frames[0].save(file_path, save_all=True, append_images=frames[1:], duration=self.playback_speed.get(), loop=0)
                messagebox.showinfo("Éxito", "¡GIF guardado!")
        except Exception as e: messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GarticAnimatorPro(root)
    root.mainloop()
