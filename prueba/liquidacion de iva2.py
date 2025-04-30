import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog  # Importar simpledialog para askstring
import json
import os

class FormularioContable:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Contable")
        self.root.geometry("800x1000")

        # Lista para almacenar registros
        self.registros = self.cargar_datos()

        # Crear secciones del formulario
        self.crear_secciones()

        # Botones de acciones
        self.crear_botones()

        # Área de resultados
        self.resultado_texto = tk.Text(root, height=15, width=90)
        self.resultado_texto.pack(pady=10)

    def crear_secciones(self):
        # Sección Comprobante
        frame_comprobante = tk.LabelFrame(self.root, text="Comprobante", padx=10, pady=10)
        frame_comprobante.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_comprobante, text="Fecha del Comprobante:").grid(row=0, column=0, sticky="w")
        self.fecha_comprobante = tk.Entry(frame_comprobante)
        self.fecha_comprobante.grid(row=0, column=1)

        tk.Label(frame_comprobante, text="Número de Comprobante (00000-00000000):").grid(row=1, column=0, sticky="w")
        self.num_comprobante = tk.Entry(frame_comprobante)
        self.num_comprobante.grid(row=1, column=1)

        tk.Label(frame_comprobante, text="Tipo de Comprobante:").grid(row=2, column=0, sticky="w")
        self.tipo_comprobante = ttk.Combobox(frame_comprobante, values=["A", "B", "C", "E", "Ticket", "ND", "NC", "FC"])
        self.tipo_comprobante.set("A")
        self.tipo_comprobante.grid(row=2, column=1)

        # Sección Cliente
        frame_cliente = tk.LabelFrame(self.root, text="Cliente", padx=10, pady=10)
        frame_cliente.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_cliente, text="Denominación:").grid(row=0, column=0, sticky="w")
        self.denominacion = tk.Entry(frame_cliente)
        self.denominacion.grid(row=0, column=1)

        tk.Label(frame_cliente, text="Domicilio:").grid(row=1, column=0, sticky="w")
        self.domicilio = tk.Entry(frame_cliente)
        self.domicilio.grid(row=1, column=1)

        tk.Label(frame_cliente, text="CUIT:").grid(row=2, column=0, sticky="w")
        self.cuit = tk.Entry(frame_cliente)
        self.cuit.grid(row=2, column=1)

        tk.Label(frame_cliente, text="Mail:").grid(row=3, column=0, sticky="w")
        self.mail = tk.Entry(frame_cliente)
        self.mail.grid(row=3, column=1)

        tk.Label(frame_cliente, text="Teléfono:").grid(row=4, column=0, sticky="w")
        self.telefono = tk.Entry(frame_cliente)
        self.telefono.grid(row=4, column=1)

        # Sección Carga de Factura
        frame_factura = tk.LabelFrame(self.root, text="Carga de Factura", padx=10, pady=10)
        frame_factura.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_factura, text="Neto:").grid(row=0, column=0, sticky="w")
        self.neto = tk.Entry(frame_factura)
        self.neto.grid(row=0, column=1)

        tk.Label(frame_factura, text="Alícuota IVA:").grid(row=1, column=0, sticky="w")
        self.alicuota = ttk.Combobox(frame_factura, values=["10.5%", "21%", "27%"])
        self.alicuota.set("21%")
        self.alicuota.grid(row=1, column=1)

        tk.Label(frame_factura, text="IVA (Calculado):").grid(row=2, column=0, sticky="w")
        self.iva = tk.Entry(frame_factura, state="readonly")
        self.iva.grid(row=2, column=1)
        self.neto.bind("<KeyRelease>", self.calcular_iva_auto)

        # Sección Otros Conceptos
        frame_otros = tk.LabelFrame(self.root, text="Otros Conceptos", padx=10, pady=10)
        frame_otros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_otros, text="Impuestos Internos:").grid(row=0, column=0, sticky="w")
        self.impuestos_internos = tk.Entry(frame_otros)
        self.impuestos_internos.grid(row=0, column=1)

        tk.Label(frame_otros, text="Neto No Gravado:").grid(row=1, column=0, sticky="w")
        self.neto_no_gravado = tk.Entry(frame_otros)
        self.neto_no_gravado.grid(row=1, column=1)

        tk.Label(frame_otros, text="Exento:").grid(row=2, column=0, sticky="w")
        self.exento = tk.Entry(frame_otros)
        self.exento.grid(row=2, column=1)

        # Sección Retenciones Nacionales
        frame_ret_nacionales = tk.LabelFrame(self.root, text="Retenciones Nacionales", padx=10, pady=10)
        frame_ret_nacionales.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ret_nacionales, text="Retención IVA:").grid(row=0, column=0, sticky="w")
        self.retencion_iva = tk.Entry(frame_ret_nacionales)
        self.retencion_iva.grid(row=0, column=1)

        tk.Label(frame_ret_nacionales, text="Retención Ganancias:").grid(row=1, column=0, sticky="w")
        self.retencion_ganancias = tk.Entry(frame_ret_nacionales)
        self.retencion_ganancias.grid(row=1, column=1)

        tk.Label(frame_ret_nacionales, text="Retención SICOES:").grid(row=2, column=0, sticky="w")
        self.retencion_sicoss = tk.Entry(frame_ret_nacionales)
        self.retencion_sicoss.grid(row=2, column=1)

        # Sección Retenciones Provinciales
        frame_ret_provinciales = tk.LabelFrame(self.root, text="Retenciones Provinciales", padx=10, pady=10)
        frame_ret_provinciales.pack(fill="x", padx=10, pady=5)

        self.provincias = ["Buenos Aires", "CABA", "Córdoba", "Santa Fe", "Otras"]
        self.retenciones_iibb = []
        for i in range(4):
            tk.Label(frame_ret_provinciales, text=f"Retención IIBB {i+1} - Provincia:").grid(row=i, column=0, sticky="w")
            prov = ttk.Combobox(frame_ret_provinciales, values=self.provincias)
            prov.set("Buenos Aires")
            prov.grid(row=i, column=1)

            tk.Label(frame_ret_provinciales, text=f"Monto Retención {i+1}:").grid(row=i, column=2, sticky="w")
            monto = tk.Entry(frame_ret_provinciales)
            monto.grid(row=i, column=3)
            self.retenciones_iibb.append((prov, monto))

    def crear_botones(self):
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Agregar Registro", command=self.agregar_registro).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Consultar Registros", command=self.consultar_registros).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Editar Registro", command=self.editar_registro).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Imprimir Registros", command=self.imprimir_registros).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones, text="Calcular Total", command=self.calcular_total).grid(row=0, column=4, padx=5)

    def calcular_iva(self, neto, alicuota):
        alicuota_valor = {"10.5%": 0.105, "21%": 0.21, "27%": 0.27}
        return neto * alicuota_valor[alicuota]

    def calcular_iva_auto(self, event):
        try:
            neto = float(self.neto.get() or 0)
            alicuota = self.alicuota.get()
            iva = self.calcular_iva(neto, alicuota)
            self.iva.config(state="normal")
            self.iva.delete(0, tk.END)
            self.iva.insert(0, f"{iva:.2f}")
            self.iva.config(state="readonly")
        except ValueError:
            self.iva.config(state="normal")
            self.iva.delete(0, tk.END)
            self.iva.insert(0, "0.00")
            self.iva.config(state="readonly")

    def agregar_registro(self):
        try:
            registro = {
                "fecha_comprobante": self.fecha_comprobante.get(),
                "num_comprobante": self.num_comprobante.get(),
                "tipo_comprobante": self.tipo_comprobante.get(),
                "cliente": {
                    "denominacion": self.denominacion.get(),
                    "domicilio": self.domicilio.get(),
                    "cuit": self.cuit.get(),
                    "mail": self.mail.get(),
                    "telefono": self.telefono.get()
                },
                "factura": {
                    "neto": float(self.neto.get() or 0),
                    "alicuota": self.alicuota.get(),
                    "iva": float(self.iva.get() or 0)
                },
                "otros": {
                    "impuestos_internos": float(self.impuestos_internos.get() or 0),
                    "neto_no_gravado": float(self.neto_no_gravado.get() or 0),
                    "exento": float(self.exento.get() or 0)
                },
                "ret_nacionales": {
                    "retencion_iva": float(self.retencion_iva.get() or 0),
                    "retencion_ganancias": float(self.retencion_ganancias.get() or 0),
                    "retencion_sicoss": float(self.retencion_sicoss.get() or 0)
                },
                "ret_provinciales": [
                    {"provincia": prov.get(), "monto": float(monto.get() or 0)} for prov, monto in self.retenciones_iibb
                ]
            }
            self.registros.append(registro)
            self.guardar_datos()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Registro agregado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

    def limpiar_formulario(self):
        for entry in [self.fecha_comprobante, self.num_comprobante, self.denominacion, self.domicilio, self.cuit,
                      self.mail, self.telefono, self.neto, self.iva, self.impuestos_internos, self.neto_no_gravado,
                      self.exento, self.retencion_iva, self.retencion_ganancias, self.retencion_sicoss]:
            entry.delete(0, tk.END)
        for _, monto in self.retenciones_iibb:
            monto.delete(0, tk.END)
        self.iva.config(state="normal")
        self.iva.insert(0, "0.00")
        self.iva.config(state="readonly")

    def consultar_registros(self):
        self.resultado_texto.delete(1.0, tk.END)
        if not self.registros:
            self.resultado_texto.insert(tk.END, "No hay registros para mostrar.\n")
            return
        for i, reg in enumerate(self.registros):
            # Usar .get() para evitar KeyError si faltan claves
            fecha = reg.get('fecha_comprobante', 'N/A')
            num_comp = reg.get('num_comprobante', 'N/A')
            tipo_comp = reg.get('tipo_comprobante', 'N/A')
            cliente = reg.get('cliente', {}).get('denominacion', 'N/A')
            neto = reg.get('factura', {}).get('neto', 0)
            iva = reg.get('factura', {}).get('iva', 0)
            self.resultado_texto.insert(tk.END, f"Registro {i+1}: {fecha} | {num_comp} | {tipo_comp} | {cliente} | Neto: {neto:.2f} | IVA: {iva:.2f}\n")

    def editar_registro(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para editar")
            return

        # Usar simpledialog.askstring en lugar de messagebox.askstring
        index_str = simpledialog.askstring("Editar", f"Ingrese el número del registro a editar (1 a {len(self.registros)}):", parent=self.root)
        if index_str is None:  # Si el usuario cancela
            return
        try:
            index = int(index_str) - 1
            if index < 0 or index >= len(self.registros):
                messagebox.showerror("Error", "Número de registro inválido")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            return

        reg = self.registros[index]
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Registro")
        edit_window.geometry("800x800")

        # Reutilizar el diseño del formulario principal
        frame_comprobante = tk.LabelFrame(edit_window, text="Comprobante", padx=10, pady=10)
        frame_comprobante.pack(fill="x", padx=10, pady=5)
        fecha_comp = tk.Entry(frame_comprobante); fecha_comp.insert(0, reg.get("fecha_comprobante", "")); fecha_comp.grid(row=0, column=1)
        num_comp = tk.Entry(frame_comprobante); num_comp.insert(0, reg.get("num_comprobante", "")); num_comp.grid(row=1, column=1)
        tipo_comp = ttk.Combobox(frame_comprobante, values=["A", "B", "C", "E", "Ticket", "ND", "NC", "FC"]); tipo_comp.set(reg.get("tipo_comprobante", "A")); tipo_comp.grid(row=2, column=1)
        tk.Label(frame_comprobante, text="Fecha del Comprobante:").grid(row=0, column=0)
        tk.Label(frame_comprobante, text="Número de Comprobante:").grid(row=1, column=0)
        tk.Label(frame_comprobante, text="Tipo de Comprobante:").grid(row=2, column=0)

        frame_cliente = tk.LabelFrame(edit_window, text="Cliente", padx=10, pady=10)
        frame_cliente.pack(fill="x", padx=10, pady=5)
        cliente = reg.get("cliente", {})
        denominacion = tk.Entry(frame_cliente); denominacion.insert(0, cliente.get("denominacion", "")); denominacion.grid(row=0, column=1)
        domicilio = tk.Entry(frame_cliente); domicilio.insert(0, cliente.get("domicilio", "")); domicilio.grid(row=1, column=1)
        cuit = tk.Entry(frame_cliente); cuit.insert(0, cliente.get("cuit", "")); cuit.grid(row=2, column=1)
        mail = tk.Entry(frame_cliente); mail.insert(0, cliente.get("mail", "")); mail.grid(row=3, column=1)
        telefono = tk.Entry(frame_cliente); telefono.insert(0, cliente.get("telefono", "")); telefono.grid(row=4, column=1)
        tk.Label(frame_cliente, text="Denominación:").grid(row=0, column=0)
        tk.Label(frame_cliente, text="Domicilio:").grid(row=1, column=0)
        tk.Label(frame_cliente, text="CUIT:").grid(row=2, column=0)
        tk.Label(frame_cliente, text="Mail:").grid(row=3, column=0)
        tk.Label(frame_cliente, text="Teléfono:").grid(row=4, column=0)

        frame_factura = tk.LabelFrame(edit_window, text="Carga de Factura", padx=10, pady=10)
        frame_factura.pack(fill="x", padx=10, pady=5)
        factura = reg.get("factura", {})
        neto = tk.Entry(frame_factura); neto.insert(0, factura.get("neto", 0)); neto.grid(row=0, column=1)
        alicuota = ttk.Combobox(frame_factura, values=["10.5%", "21%", "27%"]); alicuota.set(factura.get("alicuota", "21%")); alicuota.grid(row=1, column=1)
        iva = tk.Entry(frame_factura, state="readonly"); iva.insert(0, factura.get("iva", 0)); iva.grid(row=2, column=1)
        tk.Label(frame_factura, text="Neto:").grid(row=0, column=0)
        tk.Label(frame_factura, text="Alícuota IVA:").grid(row=1, column=0)
        tk.Label(frame_factura, text="IVA (Calculado):").grid(row=2, column=0)

        frame_otros = tk.LabelFrame(edit_window, text="Otros Conceptos", padx=10, pady=10)
        frame_otros.pack(fill="x", padx=10, pady=5)
        otros = reg.get("otros", {})
        impuestos = tk.Entry(frame_otros); impuestos.insert(0, otros.get("impuestos_internos", 0)); impuestos.grid(row=0, column=1)
        no_gravado = tk.Entry(frame_otros); no_gravado.insert(0, otros.get("neto_no_gravado", 0)); no_gravado.grid(row=1, column=1)
        exento = tk.Entry(frame_otros); exento.insert(0, otros.get("exento", 0)); exento.grid(row=2, column=1)
        tk.Label(frame_otros, text="Impuestos Internos:").grid(row=0, column=0)
        tk.Label(frame_otros, text="Neto No Gravado:").grid(row=1, column=0)
        tk.Label(frame_otros, text="Exento:").grid(row=2, column=0)

        frame_ret_nac = tk.LabelFrame(edit_window, text="Retenciones Nacionales", padx=10, pady=10)
        frame_ret_nac.pack(fill="x", padx=10, pady=5)
        ret_nac = reg.get("ret_nacionales", {})
        ret_iva = tk.Entry(frame_ret_nac); ret_iva.insert(0, ret_nac.get("retencion_iva", 0)); ret_iva.grid(row=0, column=1)
        ret_gan = tk.Entry(frame_ret_nac); ret_gan.insert(0, ret_nac.get("retencion_ganancias", 0)); ret_gan.grid(row=1, column=1)
        ret_sicoss = tk.Entry(frame_ret_nac); ret_sicoss.insert(0, ret_nac.get("retencion_sicoss", 0)); ret_sicoss.grid(row=2, column=1)
        tk.Label(frame_ret_nac, text="Retención IVA:").grid(row=0, column=0)
        tk.Label(frame_ret_nac, text="Retención Ganancias:").grid(row=1, column=0)
        tk.Label(frame_ret_nac, text="Retención SICOES:").grid(row=2, column=0)

        frame_ret_prov = tk.LabelFrame(edit_window, text="Retenciones Provinciales", padx=10, pady=10)
        frame_ret_prov.pack(fill="x", padx=10, pady=5)
        ret_prov = reg.get("ret_provinciales", [{"provincia": "Buenos Aires", "monto": 0}] * 4)
        ret_iibb = []
        for i in range(4):
            prov = ttk.Combobox(frame_ret_prov, values=self.provincias); prov.set(ret_prov[i]["provincia"]); prov.grid(row=i, column=1)
            monto = tk.Entry(frame_ret_prov); monto.insert(0, ret_prov[i]["monto"]); monto.grid(row=i, column=3)
            tk.Label(frame_ret_prov, text=f"Retención IIBB {i+1} - Provincia:").grid(row=i, column=0)
            tk.Label(frame_ret_prov, text=f"Monto {i+1}:").grid(row=i, column=2)
            ret_iibb.append((prov, monto))

        def guardar_edicion():
            try:
                self.registros[index] = {
                    "fecha_comprobante": fecha_comp.get(),
                    "num_comprobante": num_comp.get(),
                    "tipo_comprobante": tipo_comp.get(),
                    "cliente": {
                        "denominacion": denominacion.get(),
                        "domicilio": domicilio.get(),
                        "cuit": cuit.get(),
                        "mail": mail.get(),
                        "telefono": telefono.get()
                    },
                    "factura": {
                        "neto": float(neto.get() or 0),
                        "alicuota": alicuota.get(),
                        "iva": self.calcular_iva(float(neto.get() or 0), alicuota.get())
                    },
                    "otros": {
                        "impuestos_internos": float(impuestos.get() or 0),
                        "neto_no_gravado": float(no_gravado.get() or 0),
                        "exento": float(exento.get() or 0)
                    },
                    "ret_nacionales": {
                        "retencion_iva": float(ret_iva.get() or 0),
                        "retencion_ganancias": float(ret_gan.get() or 0),
                        "retencion_sicoss": float(ret_sicoss.get() or 0)
                    },
                    "ret_provinciales": [
                        {"provincia": prov.get(), "monto": float(monto.get() or 0)} for prov, monto in ret_iibb
                    ]
                }
                self.guardar_datos()
                edit_window.destroy()
                messagebox.showinfo("Éxito", "Registro editado correctamente")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

        tk.Button(edit_window, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)

    def imprimir_registros(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para imprimir")
            return

        with open("registros_contables.txt", "w", encoding="utf-8") as f:
            f.write("Registros Contables:\n\n")
            for i, reg in enumerate(self.registros):
                f.write(f"Registro {i+1}:\n")
                f.write(f"Fecha: {reg.get('fecha_comprobante', 'N/A')} | N° Comprobante: {reg.get('num_comprobante', 'N/A')} | Tipo: {reg.get('tipo_comprobante', 'N/A')}\n")
                cliente = reg.get('cliente', {})
                f.write(f"Cliente: {cliente.get('denominacion', 'N/A')} | CUIT: {cliente.get('cuit', 'N/A')}\n")
                factura = reg.get('factura', {})
                f.write(f"Neto: {factura.get('neto', 0):.2f} | IVA ({factura.get('alicuota', 'N/A')}): {factura.get('iva', 0):.2f}\n")
                otros = reg.get('otros', {})
                f.write(f"Impuestos Internos: {otros.get('impuestos_internos', 0):.2f} | Neto No Gravado: {otros.get('neto_no_gravado', 0):.2f} | Exento: {otros.get('exento', 0):.2f}\n")
                ret_nac = reg.get('ret_nacionales', {})
                f.write(f"Retenciones Nacionales: IVA: {ret_nac.get('retencion_iva', 0):.2f} | Ganancias: {ret_nac.get('retencion_ganancias', 0):.2f} | SICOES: {ret_nac.get('retencion_sicoss', 0):.2f}\n")
                f.write("Retenciones Provinciales:\n")
                ret_prov = reg.get('ret_provinciales', [{"provincia": "N/A", "monto": 0}] * 4)
                for j, ret in enumerate(ret_prov):
                    f.write(f"  IIBB {j+1}: {ret['provincia']} - {ret['monto']:.2f}\n")
                monto_bruto = (factura.get('neto', 0) + factura.get('iva', 0) + otros.get('impuestos_internos', 0) +
                               otros.get('neto_no_gravado', 0) + otros.get('exento', 0) -
                               ret_nac.get('retencion_iva', 0) - ret_nac.get('retencion_ganancias', 0) -
                               ret_nac.get('retencion_sicoss', 0) - sum(r['monto'] for r in ret_prov))
                f.write(f"Monto Bruto: {monto_bruto:.2f}\n\n")
        messagebox.showinfo("Éxito", "Registros impresos en 'registros_contables.txt'")

    def calcular_total(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para calcular")
            return

        total_neto = total_iva = total_impuestos = total_no_gravado = total_exento = total_ret_nac = total_ret_prov = 0
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, "Resumen de Registros:\n\n")

        for reg in self.registros:
            factura = reg.get('factura', {})
            otros = reg.get('otros', {})
            ret_nac = reg.get('ret_nacionales', {})
            ret_prov = reg.get('ret_provinciales', [{"monto": 0}] * 4)
            total_neto += factura.get('neto', 0)
            total_iva += factura.get('iva', 0)
            total_impuestos += otros.get('impuestos_internos', 0)
            total_no_gravado += otros.get('neto_no_gravado', 0)
            total_exento += otros.get('exento', 0)
            total_ret_nac += (ret_nac.get('retencion_iva', 0) + ret_nac.get('retencion_ganancias', 0) +
                              ret_nac.get('retencion_sicoss', 0))
            total_ret_prov += sum(r['monto'] for r in ret_prov)

        total_bruto = total_neto + total_iva + total_impuestos + total_no_gravado + total_exento - total_ret_nac - total_ret_prov

        self.resultado_texto.insert(tk.END, f"Total Neto: {total_neto:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total IVA: {total_iva:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Impuestos Internos: {total_impuestos:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Neto No Gravado: {total_no_gravado:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Exento: {total_exento:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retenciones Nacionales: {total_ret_nac:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retenciones Provinciales: {total_ret_prov:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Bruto: {total_bruto:.2f}\n")

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
