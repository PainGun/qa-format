import tkinter as tk
from tkinter import messagebox

def eliminar_seleccionado(listbox):
    seleccion = listbox.curselection()
    if seleccion:
        listbox.delete(seleccion[0])

def agregar_ambiente_pr():
    ambiente = entry_ambiente.get().strip()
    pr = entry_pr.get().strip()
    if ambiente and pr:
        item = f"Ambiente: {ambiente} - PR: {pr}"
        lista_ambientes_prs.insert(tk.END, item)
        entry_ambiente.delete(0, tk.END)
        entry_pr.delete(0, tk.END)

def agregar_comentario():
    tipo = entry_tipo_qa.get().strip()
    link = entry_link_qa.get().strip()
    ambiente = entry_ambiente_qa.get().strip()
    instruccion = txt_instruccion.get("1.0", tk.END).strip()
    if tipo and link and ambiente and instruccion:
        comentario = f"Para {tipo} (Ambiente: {ambiente}):\nPrueba en {link}\nInstrucción:\n{instruccion}"
        lista_comentarios.insert(tk.END, comentario)
        entry_tipo_qa.delete(0, tk.END)
        entry_link_qa.delete(0, tk.END)
        entry_ambiente_qa.delete(0, tk.END)
        txt_instruccion.delete("1.0", tk.END)

def agregar_qa_usu():
    qa = entry_qa_usu.get()
    if qa:
        lista_qa_usu.insert(tk.END, qa)
        entry_qa_usu.delete(0, tk.END)

def agregar_qa_cod():
    qa = entry_qa_cod.get()
    if qa:
        lista_qa_cod.insert(tk.END, qa)
        entry_qa_cod.delete(0, tk.END)

def generar_texto():
    titulo_tarea = entry_titulo.get()
    jira = entry_jira.get()
    ambientes_prs = "\n".join(f"- {item}" for item in lista_ambientes_prs.get(0, tk.END))
    comentarios = "\n\n".join(lista_comentarios.get(0, tk.END))
    qa_usu = "\n".join(f"- {item}" for item in lista_qa_usu.get(0, tk.END))
    qa_cod = "\n".join(f"- {item}" for item in lista_qa_cod.get(0, tk.END))

    resultado = f"""*Tarea:* {titulo_tarea}
*Jira:* {jira}

*Ambientes + PRs:*
{ambientes_prs if ambientes_prs else '- Sin registros agregados'}

*Comentarios:*
{comentarios if comentarios else '- Sin comentarios agregados'}

*Responsables:*
*QA Usabilidad:*
{qa_usu if qa_usu else '- Ninguno'}
*QA Código:*
{qa_cod if qa_cod else '- Ninguno'}
"""

    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, resultado)

def copiar_texto():
    root.clipboard_clear()
    root.clipboard_append(resultado_text.get("1.0", tk.END))
    messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")

# Interfaz
root = tk.Tk()
root.title("Generador Paso a QA")

# Título de la tarea
tk.Label(root, text="Título de la Tarea:").grid(row=0, column=0, sticky="e")
entry_titulo = tk.Entry(root, width=60)
entry_titulo.grid(row=0, column=1)

# Jira
tk.Label(root, text="Link Jira:").grid(row=1, column=0, sticky="e")
entry_jira = tk.Entry(root, width=60)
entry_jira.grid(row=1, column=1)

# Ambientes + PRs
tk.Label(root, text="Ambiente:").grid(row=2, column=0, sticky="e")
entry_ambiente = tk.Entry(root, width=30)
entry_ambiente.grid(row=2, column=1, sticky="w")

tk.Label(root, text="PR:").grid(row=3, column=0, sticky="e")
entry_pr = tk.Entry(root, width=30)
entry_pr.grid(row=3, column=1, sticky="w")

tk.Button(root, text="Agregar Ambiente + PR", command=agregar_ambiente_pr).grid(row=3, column=2)
lista_ambientes_prs = tk.Listbox(root, width=80, height=4)
lista_ambientes_prs.grid(row=4, column=1, columnspan=2)
tk.Button(root, text="❌", command=lambda: eliminar_seleccionado(lista_ambientes_prs)).grid(row=4, column=3)

# Comentarios
tk.Label(root, text="Tipo QA (Usabilidad/Código):").grid(row=5, column=0, sticky="e")
entry_tipo_qa = tk.Entry(root, width=60)
entry_tipo_qa.grid(row=5, column=1)

tk.Label(root, text="Link para prueba:").grid(row=6, column=0, sticky="e")
entry_link_qa = tk.Entry(root, width=60)
entry_link_qa.grid(row=6, column=1)

tk.Label(root, text="Ambiente de prueba:").grid(row=7, column=0, sticky="e")
entry_ambiente_qa = tk.Entry(root, width=60)
entry_ambiente_qa.grid(row=7, column=1)

tk.Label(root, text="Instrucción:").grid(row=8, column=0, sticky="ne")
txt_instruccion = tk.Text(root, width=60, height=4)
txt_instruccion.grid(row=8, column=1)

tk.Button(root, text="Agregar Comentario", command=agregar_comentario).grid(row=9, column=1, sticky="w")
lista_comentarios = tk.Listbox(root, width=60, height=4)
lista_comentarios.grid(row=10, column=1)
tk.Button(root, text="❌", command=lambda: eliminar_seleccionado(lista_comentarios)).grid(row=10, column=2)

# QA Usabilidad
tk.Label(root, text="QA Usabilidad:").grid(row=11, column=0, sticky="e")
entry_qa_usu = tk.Entry(root, width=45)
entry_qa_usu.grid(row=11, column=1, sticky="w")
tk.Button(root, text="Agregar", command=agregar_qa_usu).grid(row=11, column=1, sticky="e")
lista_qa_usu = tk.Listbox(root, width=60, height=2)
lista_qa_usu.grid(row=12, column=1)
tk.Button(root, text="❌", command=lambda: eliminar_seleccionado(lista_qa_usu)).grid(row=12, column=2)

# QA Código
tk.Label(root, text="QA Código:").grid(row=13, column=0, sticky="e")
entry_qa_cod = tk.Entry(root, width=45)
entry_qa_cod.grid(row=13, column=1, sticky="w")
tk.Button(root, text="Agregar", command=agregar_qa_cod).grid(row=13, column=1, sticky="e")
lista_qa_cod = tk.Listbox(root, width=60, height=2)
lista_qa_cod.grid(row=14, column=1)
tk.Button(root, text="❌", command=lambda: eliminar_seleccionado(lista_qa_cod)).grid(row=14, column=2)

# Botones finales
tk.Button(root, text="Generar", command=generar_texto).grid(row=15, column=0, pady=10)
tk.Button(root, text="Copiar", command=copiar_texto).grid(row=15, column=1, sticky="w")

# Resultado
resultado_text = tk.Text(root, height=15, width=100, bg="#f0f0f0")
resultado_text.grid(row=16, column=0, columnspan=4, pady=10)

root.mainloop()
