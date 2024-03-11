import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CodeX(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CodeX')
        self.geometry('800x600')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tabs = {}

        self.crear_menu()
        self.filename = None

    
    def crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label='Nuevo', command=self.nuevo_archivo)
        menu_archivo.add_command(label='Abrir', command=self.abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self.guardar_archivo)
        menu_archivo.add_command(label='Guardar como', command=self.guardar_como)
        menu_archivo.add_command(label='Cerrar archivo', command=self.cerrar_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Cerrar programa', command=self.cerrar_programa)
        menubar.add_cascade(label='Archivo', menu=menu_archivo)

        menu_analisis = tk.Menu(menubar, tearoff=0)
        menu_analisis.add_command(label='Lexico', command=self.lexical_analysis)
        menu_analisis.add_command(label='Semantico')
        menubar.add_cascade(label='Analisis', menu=menu_analisis)


    def nuevo_archivo(self):
        filename = 'Untitled'
        contenido = ''
        self.create_tab(filename, contenido)

    
    def abrir_archivo(self):
        self.filename = filedialog.askopenfilename(title='Abrir archivo', filetypes=[('Archivos de texto', '*.txt')])
        name = self.filename.split('/')[-1]
        if self.filename:
            with open(self.filename, 'r+') as f:
                contenido = f.read()
                self.create_tab(name, contenido)

    
    def guardar_archivo(self):
        indice_tab_actual = self.notebook.index(self.notebook.select())
        filename = self.notebook.tab(indice_tab_actual, 'text')
        contenido = self.tabs[filename]['text_area'].get(1.0, tk.END)
        if filename != 'Untitled':
            with open(filename, 'w+') as f:
                f.write(contenido)
        else:
            self.guardar_como()


    def guardar_como(self):
        indice_tab_actual = self.notebook.index(self.notebook.select())
        filename = self.notebook.tab(indice_tab_actual, 'text')
        contenido = self.tabs[filename]['text_area'].get(1.0, tk.END)
        nuevo_nombre = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Archivo de texto', '*.txt')])
        nombre_archivo = nuevo_nombre.split('/')[-1]
        if nuevo_nombre:
            with open(nuevo_nombre, 'w+') as f:
                f.write(contenido)
        if filename == 'Untitled':
            self.notebook.tab(indice_tab_actual, text=nombre_archivo)
            self.tabs[nombre_archivo]=self.tabs.pop(filename)

        
    def cerrar_archivo(self):
        indice_tab_actual = self.notebook.index(self.notebook.select())
        filename = self.notebook.tab(indice_tab_actual, 'text')
        contenido = self.tabs[filename]['text_area'].get(1.0, tk.END)
        if contenido.strip() != '':
            respuesta = messagebox.askyesnocancel('Guardar cambios', 'Desea guardar los cambios?')
            if respuesta is None:
                return
            elif respuesta:
                with open(filename, 'w+') as f:
                    f.write(contenido)
        del self.tabs[filename]
        self.notebook.forget(indice_tab_actual)
        if len(self.tabs == 0):
            self.title('CodeX')

    def cerrar_programa(self):
        if messagebox.askokcancel('Salir', 'Estas seguro que deseas salir?'):
            self.destroy()

    def create_tab(self, filename, contenido):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=filename)

        text_area = tk.Text(tab)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(1.0, contenido)

        self.tabs[filename] = {'tab': tab, 'text_area': text_area}

    def lexical_analysis(self):
        left_frame = ttk.LabelFrame(self, text='Entrada')


if __name__ == '__main__':
    editor = CodeX()
    editor.mainloop()
