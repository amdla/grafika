import tkinter as tk

from camera import CameraApp

from generate_cubes import save_cube_data


def main():
    save_cube_data("cube_data.json")

    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
