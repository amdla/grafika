import tkinter as tk
from renderer import Renderer
from camera import Camera


def main():
    root = tk.Tk()
    root.title("3D Renderer with BSP Hidden Edge Removal")

    camera = Camera()

    app = Renderer(root, camera)
    root.mainloop()


if __name__ == "__main__":
    main()
