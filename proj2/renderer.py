class Renderer:
    def __init__(self, root, camera, bsp_root):
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        self.camera = camera
        self.bsp_root = bsp_root

    def draw_controls_text(self):
        info = (
            "Controls:\n"
            "W/S - Move forward/backward\n"
            "A/D - Strafe left/right\n"
            "Q/E - Move up/down\n"
            "F/G - Roll clockwise/counter-clockwise\n"
            "Arrows - Turn / Look around"
        )
        self.canvas.create_text(10, 10, anchor="nw", text=info, fill="black",
                                font=("Consolas", 10))

    def render(self):
        self.canvas.delete("all")
        self.draw_controls_text()
        render_bsp(self.bsp_root, self.camera, self.canvas)
