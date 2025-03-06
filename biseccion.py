import os
import sympy as sp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import messagebox

def metodo_biseccion(f, xi, xs, ea_deseado, max_iter=100, precision=6):
    x = sp.Symbol('x')
    f_lambda = sp.lambdify(x, f)

    iteraciones = []
    xr_ant = None
    for i in range(max_iter):
        xr = round((xi + xs) / 2, precision)
        f_xr = f_lambda(xr)

        if xr_ant is not None:
            ea = round(abs((xr - xr_ant) / xr * 100), precision)
        else:
            ea = 100

        iteraciones.append((i + 1, xi, xs, xr, f_lambda(xi), f_lambda(xs), f_xr, ea))

        if ea <= ea_deseado:
            break

        if f_lambda(xi) * f_xr < 0:
            xs = xr
        else:
            xi = xr

        xr_ant = xr

    return xr, iteraciones

def generar_pdf(funcion, xi, xs, xr, iteraciones, ea_deseado, precision):
    nombre_archivo = f"biseccion_{str(funcion).replace('**', '^').replace('*', '·').replace('/', '÷').replace(' ', '_')}.pdf"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_directory, nombre_archivo)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    y = 750
    page_number = 1

    def nueva_pagina():
        nonlocal y, page_number
        c.showPage()
        c.setFont("Helvetica", 12)
        y = 750
        page_number += 1

    c.drawString(100, y, "Método de Bisección - Procedimiento y Resultados")
    y -= 20
    c.drawString(100, y, "Presentado por: Cristian Enrique Espinosa Agudelo - William David Nuñez Santiago")
    y -= 20
    c.drawString(100, y, f"Función: {funcion}")
    y -= 20
    c.drawString(100, y, f"Intervalo inicial: [{round(xi, precision)}, {round(xs, precision)}]")
    y -= 20
    c.drawString(100, y, f"Error absoluto deseado: {round(ea_deseado, precision)}%")
    y -= 20
    c.drawString(100, y, f"Precisión: {precision} decimales")
    y -= 40

    c.drawString(100, y, "Procedimiento de cada iteración:")
    y -= 20
    for it, xi_it, xs_it, xr_it, f_xi, f_xs, f_xr, ea in iteraciones:
        if y < 100:
            nueva_pagina()
        c.drawString(100, y, f"Iteración {it}")
        y -= 20
        c.drawString(120, y, f"xi = {round(xi_it, precision)}, xs = {round(xs_it, precision)}, xr = {round(xr_it, precision)}")
        y -= 20
        c.drawString(120, y, f"f(xi) = {round(f_xi, precision)}")
        y -= 20
        c.drawString(120, y, f"f(xs) = {round(f_xs, precision)}")
        y -= 20
        c.drawString(120, y, f"f(xr) = {round(f_xr, precision)}")
        y -= 20
        c.drawString(120, y, f"Error Aproximado (Ea) = {round(ea, precision)}%")
        y -= 40

    if y < 100:
        nueva_pagina()
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Tabla de Resultados")
    y -= 20
    c.setFont("Helvetica", 12)
    
    col_widths = [30, 70, 70, 70, 70, 70, 70, 70]
    x_start = 50
    
    headers = ['i', 'xi', 'xs', 'xr', 'f(xi)', 'f(xs)', 'f(xr)', 'Ea(%)']
    x_pos = x_start
    
    c.line(x_start, y+15, x_start + sum(col_widths), y+15)
    
    for header, width in zip(headers, col_widths):
        c.drawString(x_pos + 5, y, header)
        x_pos += width
    
    y -= 20
    
    c.line(x_start, y+15, x_start + sum(col_widths), y+15)
    
    for it, xi_it, xs_it, xr_it, f_xi, f_xs, f_xr, ea in iteraciones:
        if y < 60:
            nueva_pagina()
            x_pos = x_start
            for header, width in zip(headers, col_widths):
                c.drawString(x_pos + 5, y, header)
                x_pos += width
            y -= 20
            c.line(x_start, y+35, x_start + sum(col_widths), y+35)
            c.line(x_start, y+15, x_start + sum(col_widths), y+15)
        
        x_pos = x_start
        valores = [str(it), 
                  f"{round(xi_it, precision)}", 
                  f"{round(xs_it, precision)}", 
                  f"{round(xr_it, precision)}", 
                  f"{'+' if f_xi > 0 else '-'}", 
                  f"{'+' if f_xs > 0 else '-'}", 
                  f"{'+' if f_xr > 0 else '-'}", 
                  f"{round(ea / 100, precision)}"]
        
        for valor, width in zip(valores, col_widths):
            c.drawString(x_pos + 5, y, valor)
            x_pos += width
        
        x_line = x_start
        for width in col_widths:
            c.line(x_line, y+15, x_line, y-5)
            x_line += width
        c.line(x_line, y+15, x_line, y-5)
        
        c.line(x_start, y-5, x_start + sum(col_widths), y-5)
        
        y -= 20

    if y < 100:
        nueva_pagina()
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Resultado")
    y -= 20
    c.setFont("Helvetica", 12)
    _, _, _, _, _, _, f_xr_final, _ = iteraciones[-1]
    c.drawString(120, y, f"Raíz encontrada: {round(xr, precision)}")
    y -= 20
    c.drawString(120, y, f"f({round(xr, precision)}) = {round(f_xr_final, precision)}")
    y -= 40

    c.save()
    print(f"📄 PDF generado: {pdf_path}")
    return pdf_path

def ejecutar_biseccion():
    try:
        expr_str = entrada_funcion.get()
        xi = entrada_xi.get()
        xs = entrada_xs.get()
        ea_deseado = entrada_ea_deseado.get()
        precision = entrada_precision.get()

        if not expr_str or not xi or not xs or not ea_deseado or not precision:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        xi = float(xi)
        xs = float(xs)
        ea_deseado = float(ea_deseado)
        precision = int(precision)

        if xi >= xs:
            messagebox.showerror("Error", "El límite inferior (xi) debe ser menor que el límite superior (xs).")
            return

        funcion = sp.sympify(expr_str)
        f_lambda = sp.lambdify(sp.Symbol('x'), funcion)

        if f_lambda(xi) * f_lambda(xs) > 0:
            messagebox.showerror("Error", "No se cumple el Teorema de Bolzano en el intervalo dado. No hay raíz en este intervalo.")
            return

        raiz, iteraciones = metodo_biseccion(funcion, xi, xs, ea_deseado, precision=precision)

        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, f"Raíz encontrada: {round(raiz, precision)}\n")
        resultado_texto.insert(tk.END, f"f({round(raiz, precision)}) = {round(f_lambda(raiz), precision)}\n\n")
        resultado_texto.insert(tk.END, "Iteraciones:\n")
        for it, xi_it, xs_it, xr, f_xi, f_xs, f_xr, ea in iteraciones:
            resultado_texto.insert(tk.END, f"Iteración {it}: xi = {round(xi_it, precision)}, xs = {round(xs_it, precision)}, xr = {round(xr, precision)}\n")
            resultado_texto.insert(tk.END, f"f(xi) = {round(f_xi, precision)}, f(xs) = {round(f_xs, precision)}, f(xr) = {round(f_xr, precision)}, Ea = {round(ea, precision)}%\n\n")

        pdf_path = generar_pdf(funcion, xi, xs, raiz, iteraciones, ea_deseado, precision)
        messagebox.showinfo("Éxito", f"PDF generado: {pdf_path}")

    except ValueError as ve:
        messagebox.showerror("Error", f"Error de valor: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def limpiar_campos():
    entrada_funcion.delete(0, tk.END)
    entrada_xi.delete(0, tk.END)
    entrada_xs.delete(0, tk.END)
    entrada_ea_deseado.delete(0, tk.END)
    entrada_precision.delete(0, tk.END)
    resultado_texto.delete(1.0, tk.END)

ventana = tk.Tk()
ventana.title("Método de Bisección")
ventana.geometry("600x500")
ventana.configure(bg="#f0f0f0")

tk.Label(ventana, text="Función (en términos de x):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
entrada_funcion = tk.Entry(ventana, width=30)
entrada_funcion.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Límite inferior (xi):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
entrada_xi = tk.Entry(ventana, width=30)
entrada_xi.grid(row=1, column=1, padx=10, pady=10)

tk.Label(ventana, text="Límite superior (xs):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
entrada_xs = tk.Entry(ventana, width=30)
entrada_xs.grid(row=2, column=1, padx=10, pady=10)

tk.Label(ventana, text="Error absoluto deseado (%):", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
entrada_ea_deseado = tk.Entry(ventana, width=30)
entrada_ea_deseado.grid(row=3, column=1, padx=10, pady=10)

tk.Label(ventana, text="Precisión (decimales):", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10)
entrada_precision = tk.Entry(ventana, width=30)
entrada_precision.grid(row=4, column=1, padx=10, pady=10)

boton_ejecutar = tk.Button(ventana, text="Ejecutar Método", command=ejecutar_biseccion, bg="#4CAF50", fg="white")
boton_ejecutar.grid(row=5, column=0, columnspan=2, pady=20)

boton_limpiar = tk.Button(ventana, text="Limpiar Campos", command=limpiar_campos, bg="#FF5733", fg="white")
boton_limpiar.grid(row=6, column=0, columnspan=2, pady=10)

resultado_texto = tk.Text(ventana, height=10, width=60)
resultado_texto.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit, bg="#333333", fg="white")
boton_salir.grid(row=8, column=0, columnspan=2, pady=10)

ventana.mainloop()