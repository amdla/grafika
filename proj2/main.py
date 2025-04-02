import tkinter as tk
from app import App


def main():
    root = tk.Tk()
    root.title("BSP Tree Hidden-Surface Example with Extended Movement")
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
