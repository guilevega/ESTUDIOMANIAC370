import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class FormularioContable:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Contable")
        self.root.geometry("700x800")

        # Lista para almacenar registros
        self.registros = self.cargar_datos()

        # Campos del formulario
        self.crear_formulario()

        # Botones
        self.boton_agregar = tk.Button(root, text="Agregar Registro", command=self.agregar_registro)
        self.boton_agregar.pack(pady=5)

        self.boton_consultar = tk.Button(root, text="Consultar Registros", command=self.consultar_registros)
        self.boton_consultar.pack(pady=5)

        self.boton_editar = tk.Button(root, text="Editar Registro", command=self.editar_registro)
        self.boton_editar.pack(pady=5)

        self.boton_imprimir = tk.Button(root, text="Imprimir Registros", command=self.imprimir_registros)
        self.boton_imprimir.pack(pady=5)

        self.boton_total = tk.Button(root, text="Calcular Total", command=self.calcular_total)
        self.boton_total.pack(pady=5)

        # Área de resultados
        self.resultado_texto = tk.Text(root, height=15, width=80)
        self.resultado_texto.pack(pady=10)

    def crear_formulario(self):
        # Fechas
        tk.Label(self.root, text="Fecha del Comprobante:").pack()
        self.fecha_comprobante = tk.Entry(self.root)
        self.fecha_comprobante.pack()

        tk.Label(self.root, text="Fecha de Contabilidad:").pack()
        self.fecha_contabilidad = tk.Entry(self.root)
        self.fecha_contabilidad.pack()

        # Neto y alícuota
        tk.Label(self.root, text="Neto:").pack()
        self.neto = tk.Entry(self.root)
        self.neto.pack()

        tk.Label(self.root, text="Alícuota IVA:").pack()
        self.alicuota = ttk.Combobox(self.root, values=["10.5%", "21%", "27%"])
        self.alicuota.set("21%")  # Valor por defecto
        self.alicuota.pack()

        # Otros campos
        tk.Label(self.root, text="Impuestos Internos:").pack()
        self.impuestos_internos = tk.Entry(self.root)
        self.impuestos_internos.pack()

        tk.Label(self.root, text="Neto No Gravado:").pack()
        self.neto_no_gravado = tk.Entry(self.root)
        self.neto_no_gravado.pack()

        tk.Label(self.root, text="Exento:").pack()
        self.exento = tk.Entry(self.root)
        self.exento.pack()

        tk.Label(self.root, text="Retención IVA:").pack()
        self.retencion_iva = tk.Entry(self.root)
        self.retencion_iva.pack()

        tk.Label(self.root, text="Retención Ganancias:").pack()
        self.retencion_ganancias = tk.Entry(self.root)
        self.retencion_ganancias.pack()

        tk.Label(self.root, text="Retención SICOES:").pack()
        self.retencion_sicoss = tk.Entry(self.root)
        self.retencion_sicoss.pack()

        # Retención Ingresos Brutos
        tk.Label(self.root, text="Retención Ingresos Brutos - Provincia:").pack()
        self.provincia = ttk.Combobox(self.root, values=["Buenos Aires", "CABA", "Córdoba", "Santa Fe", "Otras"])
        self.provincia.set("Buenos Aires")
        self.provincia.pack()

        tk.Label(self.root, text="Monto Retención IIBB:").pack()
        self.retencion_iibb = tk.Entry(self.root)
        self.retencion_iibb.pack()

    def calcular_iva(self, neto, alicuota):
        alicuota_valor = {"10.5%": 0.105, "21%": 0.21, "27%": 0.27}
        return neto * alicuota_valor[alicuota]

    def agregar_registro(self):
        try:
            # Obtener valores
            fecha_comp = self.fecha_comprobante.get()
            fecha_cont = self.fecha_contabilidad.get()
            neto = float(self.neto.get() or 0)
            alicuota = self.alicuota.get()
            iva = self.calcular_iva(neto, alicuota)
            impuestos_int = float(self.impuestos_internos.get() or 0)
            neto_no_grav = float(self.neto_no_gravado.get() or 0)
            exento = float(self.exento.get() or 0)
            ret_iva = float(self.retencion_iva.get() or 0)
            ret_gan = float(self.retencion_ganancias.get() or 0)
            ret_sicoss = float(self.retencion_sicoss.get() or 0)
            provincia = self.provincia.get()
            ret_iibb = float(self.retencion_iibb.get() or 0)

            # Guardar registro
            registro = {
                "fecha_comprobante": fecha_comp,
                "fecha_contabilidad": fecha_cont,
                "neto": neto,
                "alicuota": alicuota,
                "iva": iva,
                "impuestos_internos": impuestos_int,
                "neto_no_gravado": neto_no_grav,
                "exento": exento,
                "retencion_iva": ret_iva,
                "retencion_ganancias": ret_gan,
                "retencion_sicoss": ret_sicoss,
                "provincia": provincia,
                "retencion_iibb": ret_iibb
            }
            self.registros.append(registro)
            self.guardar_datos()

            # Limpiar formulario
            self.limpiar_formulario()

            messagebox.showinfo("Éxito", "Registro agregado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

    def limpiar_formulario(self):
        self.fecha_comprobante.delete(0, tk.END)
        self.fecha_contabilidad.delete(0, tk.END)
        self.neto.delete(0, tk.END)
        self.impuestos_internos.delete(0, tk.END)
        self.neto_no_gravado.delete(0, tk.END)
        self.exento.delete(0, tk.END)
        self.retencion_iva.delete(0, tk.END)
        self.retencion_ganancias.delete(0, tk.END)
        self.retencion_sicoss.delete(0, tk.END)
        self.retencion_iibb.delete(0, tk.END)

    def consultar_registros(self):
        self.resultado_texto.delete(1.0, tk.END)
        if not self.registros:
            self.resultado_texto.insert(tk.END, "No hay registros para mostrar.\n")
            return

        self.resultado_texto.insert(tk.END, "Lista de Registros:\n\n")
        for i, reg in enumerate(self.registros):
            self.resultado_texto.insert(tk.END, f"Registro {i+1}: Fecha: {reg['fecha_comprobante']} | Neto: {reg['neto']} | IVA: {reg['iva']:.2f} | Provincia: {reg['provincia']}\n")

    def editar_registro(self):
        def guardar_edicion(index):
            try:
                self.registros[index]["fecha_comprobante"] = edit_fecha_comp.get()
                self.registros[index]["fecha_contabilidad"] = edit_fecha_cont.get()
                self.registros[index]["neto"] = float(edit_neto.get() or 0)
                self.registros[index]["alicuota"] = edit_alicuota.get()
                self.registros[index]["iva"] = self.calcular_iva(self.registros[index]["neto"], edit_alicuota.get())
                self.registros[index]["impuestos_internos"] = float(edit_impuestos.get() or 0)
                self.registros[index]["neto_no_gravado"] = float(edit_no_gravado.get() or 0)
                self.registros[index]["exento"] = float(edit_exento.get() or 0)
                self.registros[index]["retencion_iva"] = float(edit_ret_iva.get() or 0)
                self.registros[index]["retencion_ganancias"] = float(edit_ret_gan.get() or 0)
                self.registros[index]["retencion_sicoss"] = float(edit_ret_sicoss.get() or 0)
                self.registros[index]["provincia"] = edit_provincia.get()
                self.registros[index]["retencion_iibb"] = float(edit_ret_iibb.get() or 0)
                self.guardar_datos()
                edit_window.destroy()
                messagebox.showinfo("Éxito", "Registro editado correctamente")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para editar")
            return

        index = int(messagebox.askstring("Editar", "Ingrese el número del registro a editar (1 a {}):".format(len(self.registros)))) - 1
        if index < 0 or index >= len(self.registros):
            messagebox.showerror("Error", "Número de registro inválido")
            return

        reg = self.registros[index]
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Registro")
        edit_window.geometry("400x500")

        tk.Label(edit_window, text="Fecha del Comprobante:").pack()
        edit_fecha_comp = tk.Entry(edit_window)
        edit_fecha_comp.insert(0, reg["fecha_comprobante"])
        edit_fecha_comp.pack()

        tk.Label(edit_window, text="Fecha de Contabilidad:").pack()
        edit_fecha_cont = tk.Entry(edit_window)
        edit_fecha_cont.insert(0, reg["fecha_contabilidad"])
        edit_fecha_cont.pack()

        tk.Label(edit_window, text="Neto:").pack()
        edit_neto = tk.Entry(edit_window)
        edit_neto.insert(0, reg["neto"])
        edit_neto.pack()

        tk.Label(edit_window, text="Alícuota IVA:").pack()
        edit_alicuota = ttk.Combobox(edit_window, values=["10.5%", "21%", "27%"])
        edit_alicuota.set(reg["alicuota"])
        edit_alicuota.pack()

        tk.Label(edit_window, text="Impuestos Internos:").pack()
        edit_impuestos = tk.Entry(edit_window)
        edit_impuestos.insert(0, reg["impuestos_internos"])
        edit_impuestos.pack()

        tk.Label(edit_window, text="Neto No Gravado:").pack()
        edit_no_gravado = tk.Entry(edit_window)
        edit_no_gravado.insert(0, reg["neto_no_gravado"])
        edit_no_gravado.pack()

        tk.Label(edit_window, text="Exento:").pack()
        edit_exento = tk.Entry(edit_window)
        edit_exento.insert(0, reg["exento"])
        edit_exento.pack()

        tk.Label(edit_window, text="Retención IVA:").pack()
        edit_ret_iva = tk.Entry(edit_window)
        edit_ret_iva.insert(0, reg["retencion_iva"])
        edit_ret_iva.pack()

        tk.Label(edit_window, text="Retención Ganancias:").pack()
        edit_ret_gan = tk.Entry(edit_window)
        edit_ret_gan.insert(0, reg["retencion_ganancias"])
        edit_ret_gan.pack()

        tk.Label(edit_window, text="Retención SICOES:").pack()
        edit_ret_sicoss = tk.Entry(edit_window)
        edit_ret_sicoss.insert(0, reg["retencion_sicoss"])
        edit_ret_sicoss.pack()

        tk.Label(edit_window, text="Provincia:").pack()
        edit_provincia = ttk.Combobox(edit_window, values=["Buenos Aires", "CABA", "Córdoba", "Santa Fe", "Otras"])
        edit_provincia.set(reg["provincia"])
        edit_provincia.pack()

        tk.Label(edit_window, text="Retención IIBB:").pack()
        edit_ret_iibb = tk.Entry(edit_window)
        edit_ret_iibb.insert(0, reg["retencion_iibb"])
        edit_ret_iibb.pack()

        tk.Button(edit_window, text="Guardar Cambios", command=lambda: guardar_edicion(index)).pack(pady=10)

    def imprimir_registros(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para imprimir")
            return

        with open("registros_contables.txt", "w", encoding="utf-8") as f:
            f.write("Registros Contables:\n\n")
            for i, reg in enumerate(self.registros):
                f.write(f"Registro {i+1}:\n")
                f.write(f"Fecha Comprobante: {reg['fecha_comprobante']}\n")
                f.write(f"Fecha Contabilidad: {reg['fecha_contabilidad']}\n")
                f.write(f"Neto: {reg['neto']:.2f}\n")
                f.write(f"IVA ({reg['alicuota']}): {reg['iva']:.2f}\n")
                f.write(f"Impuestos Internos: {reg['impuestos_internos']:.2f}\n")
                f.write(f"Neto No Gravado: {reg['neto_no_gravado']:.2f}\n")
                f.write(f"Exento: {reg['exento']:.2f}\n")
                f.write(f"Retención IVA: {reg['retencion_iva']:.2f}\n")
                f.write(f"Retención Ganancias: {reg['retencion_ganancias']:.2f}\n")
                f.write(f"Retención SICOES: {reg['retencion_sicoss']:.2f}\n")
                f.write(f"Provincia: {reg['provincia']}\n")
                f.write(f"Retención IIBB: {reg['retencion_iibb']:.2f}\n\n")

        messagebox.showinfo("Éxito", "Registros impresos en 'registros_contables.txt'")

    def calcular_total(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para calcular")
            return

        total_neto = 0
        total_iva = 0
        total_impuestos = 0
        total_no_gravado = 0
        total_exento = 0
        total_retenciones = 0

        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, "Resumen de Registros:\n\n")

        for reg in self.registros:
            total_neto += reg["neto"]
            total_iva += reg["iva"]
            total_impuestos += reg["impuestos_internos"]
            total_no_gravado += reg["neto_no_gravado"]
            total_exento += reg["exento"]
            total_retenciones += (reg["retencion_iva"] + reg["retencion_ganancias"] +
                                 reg["retencion_sicoss"] + reg["retencion_iibb"])

            self.resultado_texto.insert(tk.END, f"Fecha: {reg['fecha_comprobante']} | Neto: {reg['neto']} | IVA: {reg['iva']:.2f} | Provincia: {reg['provincia']}\n")

        total_final = total_neto + total_iva + total_impuestos + total_no_gravado + total_exento - total_retenciones

        self.resultado_texto.insert(tk.END, "\nTotales:\n")
        self.resultado_texto.insert(tk.END, f"Neto: {total_neto:.2f}\n")
        self.resultado_texto.insert(tk.END, f"IVA: {total_iva:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Impuestos Internos: {total_impuestos:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Neto No Gravado: {total_no_gravado:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Exento: {total_exento:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Retenciones: {total_retenciones:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Final: {total_final:.2f}\n")

    def guardar_datos(self):
        with open("registros_contables.json", "w", encoding="utf-8") as f:
            json.dump(self.registros, f, ensure_ascii=False, indent=4)

    def cargar_datos(self):
        if os.path.exists("registros_contables.json"):
            with open("registros_contables.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioContable(root)
    root.mainloop()
