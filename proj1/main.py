import tkinter as tk

from renderer import Renderer


def main():
    root = tk.Tk()
    root.title("3D Renderer")
    app = Renderer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
