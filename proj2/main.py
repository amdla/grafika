# main.py
import tkinter as tk
from renderer import Renderer
from bsp import build_bsp, classify_polygon
from camera import Camera
import math


def main():
    # Set up the Tkinter window
    root = tk.Tk()
    root.title("3D Renderer with BSP Hidden Edge Removal")

    # Set up the camera
    camera = Camera()

    # Set up the renderer with the camera
    app = Renderer(root, camera)
    root.mainloop()


if __name__ == "__main__":
    main()
