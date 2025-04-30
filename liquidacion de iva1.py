import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import json
import os

class FormularioContable:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Contable")
        self.root.geometry("900x1100")

        # Lista para almacenar registros
        self.registros = self.cargar_datos()

        # Crear secciones del formulario
        self.crear_secciones()

        # Botones de acciones
        self.crear_botones()

        # Área de resultados
        self.resultado_texto = tk.Text(root, height=15, width=100)
        self.resultado_texto.pack(pady=10)

    def crear_secciones(self):
        # Sección Comprobante
        frame_comprobante = tk.LabelFrame(self.root, text="Comprobante", padx=10, pady=10)
        frame_comprobante.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_comprobante, text="Fecha del Comprobante:").grid(row=0, column=0, sticky="w")
        self.fecha_comprobante = tk.Entry(frame_comprobante)
        self.fecha_comprobante.grid(row=0, column=1)

        tk.Label(frame_comprobante, text="N° Comprobante (5 dígitos):").grid(row=1, column=0, sticky="w")
        self.num_comprobante_part1 = tk.Entry(frame_comprobante, width=10)
        self.num_comprobante_part1.grid(row=1, column=1, sticky="w")
        self.num_comprobante_part1.config(validate="key", validatecommand=(self.root.register(lambda x: len(x) <= 5 and x.isdigit()), "%P"))

        tk.Label(frame_comprobante, text="N° Comprobante (8 dígitos):").grid(row=1, column=2, sticky="w")
        self.num_comprobante_part2 = tk.Entry(frame_comprobante, width=15)
        self.num_comprobante_part2.grid(row=1, column=3, sticky="w")
        self.num_comprobante_part2.config(validate="key", validatecommand=(self.root.register(lambda x: len(x) <= 8 and x.isdigit()), "%P"))

        tk.Label(frame_comprobante, text="Tipo de Comprobante:").grid(row=2, column=0, sticky="w")
        self.tipo_comprobante = ttk.Combobox(frame_comprobante, values=["A", "B", "C", "E", "Ticket", "ND", "NC", "FC"])
        self.tipo_comprobante.set("A")
        self.tipo_comprobante.grid(row=2, column=1)

        tk.Label(frame_comprobante, text="Fecha de Contabilización:").grid(row=3, column=0, sticky="w")
        self.fecha_contabilizacion = tk.Entry(frame_comprobante)
        self.fecha_contabilizacion.grid(row=3, column=1)

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

        # Sección Otros Conceptos (horizontal con subtotal)
        frame_otros = tk.LabelFrame(self.root, text="Otros Conceptos", padx=10, pady=10)
        frame_otros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_otros, text="Impuestos Internos:").grid(row=0, column=0, sticky="w")
        self.impuestos_internos = tk.Entry(frame_otros, width=15)
        self.impuestos_internos.grid(row=0, column=1)

        tk.Label(frame_otros, text="Neto No Gravado:").grid(row=0, column=2, sticky="w")
        self.neto_no_gravado = tk.Entry(frame_otros, width=15)
        self.neto_no_gravado.grid(row=0, column=3)

        tk.Label(frame_otros, text="Exento:").grid(row=0, column=4, sticky="w")
        self.exento = tk.Entry(frame_otros, width=15)
        self.exento.grid(row=0, column=5)

        tk.Label(frame_otros, text="Subtotal Otros:").grid(row=0, column=6, sticky="w")
        self.subtotal_otros = tk.Entry(frame_otros, width=15, state="readonly")
        self.subtotal_otros.grid(row=0, column=7)
        for entry in [self.impuestos_internos, self.neto_no_gravado, self.exento]:
            entry.bind("<KeyRelease>", self.calcular_subtotal_otros)

        # Sección Retenciones Nacionales (horizontal con subtotal)
        frame_ret_nacionales = tk.LabelFrame(self.root, text="Retenciones Nacionales", padx=10, pady=10)
        frame_ret_nacionales.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ret_nacionales, text="Retención IVA:").grid(row=0, column=0, sticky="w")
        self.retencion_iva = tk.Entry(frame_ret_nacionales, width=15)
        self.retencion_iva.grid(row=0, column=1)

        tk.Label(frame_ret_nacionales, text="Retención Ganancias:").grid(row=0, column=2, sticky="w")
        self.retencion_ganancias = tk.Entry(frame_ret_nacionales, width=15)
        self.retencion_ganancias.grid(row=0, column=3)

        tk.Label(frame_ret_nacionales, text="Retención SICOES:").grid(row=0, column=4, sticky="w")
        self.retencion_sicoss = tk.Entry(frame_ret_nacionales, width=15)
        self.retencion_sicoss.grid(row=0, column=5)

        tk.Label(frame_ret_nacionales, text="Subtotal Ret. Nacionales:").grid(row=0, column=6, sticky="w")
        self.subtotal_ret_nacionales = tk.Entry(frame_ret_nacionales, width=15, state="readonly")
        self.subtotal_ret_nacionales.grid(row=0, column=7)
        for entry in [self.retencion_iva, self.retencion_ganancias, self.retencion_sicoss]:
            entry.bind("<KeyRelease>", self.calcular_subtotal_ret_nacionales)

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
            monto.bind("<KeyRelease>", self.calcular_monto_bruto)

        # Sección Total Bruto
        frame_total = tk.LabelFrame(self.root, text="Total", padx=10, pady=10)
        frame_total.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_total, text="Monto Bruto:").grid(row=0, column=0, sticky="w")
        self.monto_bruto = tk.Entry(frame_total, state="readonly")
        self.monto_bruto.grid(row=0, column=1)

        # Vincular cálculo automático al modificar campos
        for entry in [self.neto, self.impuestos_internos, self.neto_no_gravado, self.exento,
                      self.retencion_iva, self.retencion_ganancias, self.retencion_sicoss]:
            entry.bind("<KeyRelease>", self.calcular_monto_bruto)

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

    def calcular_subtotal_otros(self, event):
        try:
            impuestos = float(self.impuestos_internos.get() or 0)
            no_gravado = float(self.neto_no_gravado.get() or 0)
            exento = float(self.exento.get() or 0)
            subtotal = impuestos + no_gravado + exento
            self.subtotal_otros.config(state="normal")
            self.subtotal_otros.delete(0, tk.END)
            self.subtotal_otros.insert(0, f"{subtotal:.2f}")
            self.subtotal_otros.config(state="readonly")
        except ValueError:
            self.subtotal_otros.config(state="normal")
            self.subtotal_otros.delete(0, tk.END)
            self.subtotal_otros.insert(0, "0.00")
            self.subtotal_otros.config(state="readonly")

    def calcular_subtotal_ret_nacionales(self, event):
        try:
            ret_iva = float(self.retencion_iva.get() or 0)
            ret_gan = float(self.retencion_ganancias.get() or 0)
            ret_sicoss = float(self.retencion_sicoss.get() or 0)
            subtotal = ret_iva + ret_gan + ret_sicoss
            self.subtotal_ret_nacionales.config(state="normal")
            self.subtotal_ret_nacionales.delete(0, tk.END)
            self.subtotal_ret_nacionales.insert(0, f"{subtotal:.2f}")
            self.subtotal_ret_nacionales.config(state="readonly")
        except ValueError:
            self.subtotal_ret_nacionales.config(state="normal")
            self.subtotal_ret_nacionales.delete(0, tk.END)
            self.subtotal_ret_nacionales.insert(0, "0.00")
            self.subtotal_ret_nacionales.config(state="readonly")

    def calcular_monto_bruto(self, event):
        try:
            neto = float(self.neto.get() or 0)
            iva = float(self.iva.get() or 0)
            impuestos = float(self.impuestos_internos.get() or 0)
            no_gravado = float(self.neto_no_gravado.get() or 0)
            exento = float(self.exento.get() or 0)
            ret_iva = float(self.retencion_iva.get() or 0)
            ret_gan = float(self.retencion_ganancias.get() or 0)
            ret_sicoss = float(self.retencion_sicoss.get() or 0)
            ret_iibb_total = sum(float(monto.get() or 0) for _, monto in self.retenciones_iibb)
            monto_bruto = neto + iva + impuestos + no_gravado + exento - ret_iva - ret_gan - ret_sicoss - ret_iibb_total
            self.monto_bruto.config(state="normal")
            self.monto_bruto.delete(0, tk.END)
            self.monto_bruto.insert(0, f"{monto_bruto:.2f}")
            self.monto_bruto.config(state="readonly")
            self.calcular_subtotal_otros(None)  # Actualizar subtotal otros
            self.calcular_subtotal_ret_nacionales(None)  # Actualizar subtotal retenciones nacionales
        except ValueError:
            self.monto_bruto.config(state="normal")
            self.monto_bruto.delete(0, tk.END)
            self.monto_bruto.insert(0, "0.00")
            self.monto_bruto.config(state="readonly")

    def agregar_registro(self):
        try:
            registro = {
                "fecha_comprobante": self.fecha_comprobante.get(),
                "num_comprobante_part1": self.num_comprobante_part1.get(),
                "num_comprobante_part2": self.num_comprobante_part2.get(),
                "tipo_comprobante": self.tipo_comprobante.get(),
                "fecha_contabilizacion": self.fecha_contabilizacion.get(),
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
                    "exento": float(self.exento.get() or 0),
                    "subtotal": float(self.subtotal_otros.get() or 0)
                },
                "ret_nacionales": {
                    "retencion_iva": float(self.retencion_iva.get() or 0),
                    "retencion_ganancias": float(self.retencion_ganancias.get() or 0),
                    "retencion_sicoss": float(self.retencion_sicoss.get() or 0),
                    "subtotal": float(self.subtotal_ret_nacionales.get() or 0)
                },
                "ret_provinciales": [
                    {"provincia": prov.get(), "monto": float(monto.get() or 0)} for prov, monto in self.retenciones_iibb
                ],
                "monto_bruto": float(self.monto_bruto.get() or 0)
            }
            self.registros.append(registro)
            self.guardar_datos()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Registro agregado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

    def limpiar_formulario(self):
        for entry in [self.fecha_comprobante, self.num_comprobante_part1, self.num_comprobante_part2,
                      self.fecha_contabilizacion, self.denominacion, self.domicilio, self.cuit, self.mail,
                      self.telefono, self.neto, self.impuestos_internos, self.neto_no_gravado, self.exento,
                      self.retencion_iva, self.retencion_ganancias, self.retencion_sicoss]:
            entry.delete(0, tk.END)
        for _, monto in self.retenciones_iibb:
            monto.delete(0, tk.END)
        for entry in [self.iva, self.subtotal_otros, self.subtotal_ret_nacionales, self.monto_bruto]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, "0.00")
            entry.config(state="readonly")

    def consultar_registros(self):
        self.resultado_texto.delete(1.0, tk.END)
        if not self.registros:
            self.resultado_texto.insert(tk.END, "No hay registros para mostrar.\n")
            return
        for i, reg in enumerate(self.registros):
            self.resultado_texto.insert(tk.END, f"Registro {i+1}: {reg['fecha_comprobante']} | {reg['num_comprobante_part1']}-{reg['num_comprobante_part2']} | {reg['tipo_comprobante']} | {reg['fecha_contabilizacion']} | {reg['cliente']['denominacion']} | Neto: {reg['factura']['neto']:.2f} | IVA: {reg['factura']['iva']:.2f} | Monto Bruto: {reg['monto_bruto']:.2f}\n")

    def editar_registro(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para editar")
            return

        index_str = simpledialog.askstring("Editar", f"Ingrese el número del registro a editar (1 a {len(self.registros)}):", parent=self.root)
        if index_str is None:
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
        edit_window.geometry("900x1000")

        # Sección Comprobante
        frame_comprobante = tk.LabelFrame(edit_window, text="Comprobante", padx=10, pady=10)
        frame_comprobante.pack(fill="x", padx=10, pady=5)
        fecha_comp = tk.Entry(frame_comprobante); fecha_comp.insert(0, reg["fecha_comprobante"]); fecha_comp.grid(row=0, column=1)
        num_comp1 = tk.Entry(frame_comprobante); num_comp1.insert(0, reg["num_comprobante_part1"]); num_comp1.grid(row=1, column=1)
        num_comp2 = tk.Entry(frame_comprobante); num_comp2.insert(0, reg["num_comprobante_part2"]); num_comp2.grid(row=1, column=3)
        tipo_comp = ttk.Combobox(frame_comprobante, values=["A", "B", "C", "E", "Ticket", "ND", "NC", "FC"]); tipo_comp.set(reg["tipo_comprobante"]); tipo_comp.grid(row=2, column=1)
        fecha_contab = tk.Entry(frame_comprobante); fecha_contab.insert(0, reg["fecha_contabilizacion"]); fecha_contab.grid(row=3, column=1)
        tk.Label(frame_comprobante, text="Fecha del Comprobante:").grid(row=0, column=0)
        tk.Label(frame_comprobante, text="N° Comprobante (5):").grid(row=1, column=0)
        tk.Label(frame_comprobante, text="N° Comprobante (8):").grid(row=1, column=2)
        tk.Label(frame_comprobante, text="Tipo de Comprobante:").grid(row=2, column=0)
        tk.Label(frame_comprobante, text="Fecha de Contabilización:").grid(row=3, column=0)

        # Sección Cliente
        frame_cliente = tk.LabelFrame(edit_window, text="Cliente", padx=10, pady=10)
        frame_cliente.pack(fill="x", padx=10, pady=5)
        cliente = reg["cliente"]
        denominacion = tk.Entry(frame_cliente); denominacion.insert(0, cliente["denominacion"]); denominacion.grid(row=0, column=1)
        domicilio = tk.Entry(frame_cliente); domicilio.insert(0, cliente["domicilio"]); domicilio.grid(row=1, column=1)
        cuit = tk.Entry(frame_cliente); cuit.insert(0, cliente["cuit"]); cuit.grid(row=2, column=1)
        mail = tk.Entry(frame_cliente); mail.insert(0, cliente["mail"]); mail.grid(row=3, column=1)
        telefono = tk.Entry(frame_cliente); telefono.insert(0, cliente["telefono"]); telefono.grid(row=4, column=1)
        tk.Label(frame_cliente, text="Denominación:").grid(row=0, column=0)
        tk.Label(frame_cliente, text="Domicilio:").grid(row=1, column=0)
        tk.Label(frame_cliente, text="CUIT:").grid(row=2, column=0)
        tk.Label(frame_cliente, text="Mail:").grid(row=3, column=0)
        tk.Label(frame_cliente, text="Teléfono:").grid(row=4, column=0)

        # Sección Carga de Factura
        frame_factura = tk.LabelFrame(edit_window, text="Carga de Factura", padx=10, pady=10)
        frame_factura.pack(fill="x", padx=10, pady=5)
        factura = reg["factura"]
        neto = tk.Entry(frame_factura); neto.insert(0, factura["neto"]); neto.grid(row=0, column=1)
        alicuota = ttk.Combobox(frame_factura, values=["10.5%", "21%", "27%"]); alicuota.set(factura["alicuota"]); alicuota.grid(row=1, column=1)
        iva = tk.Entry(frame_factura, state="readonly"); iva.insert(0, factura["iva"]); iva.grid(row=2, column=1)
        tk.Label(frame_factura, text="Neto:").grid(row=0, column=0)
        tk.Label(frame_factura, text="Alícuota IVA:").grid(row=1, column=0)
        tk.Label(frame_factura, text="IVA (Calculado):").grid(row=2, column=0)

        # Sección Otros Conceptos
        frame_otros = tk.LabelFrame(edit_window, text="Otros Conceptos", padx=10, pady=10)
        frame_otros.pack(fill="x", padx=10, pady=5)
        otros = reg["otros"]
        impuestos = tk.Entry(frame_otros, width=15); impuestos.insert(0, otros["impuestos_internos"]); impuestos.grid(row=0, column=1)
        no_gravado = tk.Entry(frame_otros, width=15); no_gravado.insert(0, otros["neto_no_gravado"]); no_gravado.grid(row=0, column=3)
        exento = tk.Entry(frame_otros, width=15); exento.insert(0, otros["exento"]); exento.grid(row=0, column=5)
        subtotal_otros = tk.Entry(frame_otros, width=15, state="readonly"); subtotal_otros.insert(0, otros["subtotal"]); subtotal_otros.grid(row=0, column=7)
        tk.Label(frame_otros, text="Impuestos Internos:").grid(row=0, column=0)
        tk.Label(frame_otros, text="Neto No Gravado:").grid(row=0, column=2)
        tk.Label(frame_otros, text="Exento:").grid(row=0, column=4)
        tk.Label(frame_otros, text="Subtotal Otros:").grid(row=0, column=6)

        # Sección Retenciones Nacionales
        frame_ret_nac = tk.LabelFrame(edit_window, text="Retenciones Nacionales", padx=10, pady=10)
        frame_ret_nac.pack(fill="x", padx=10, pady=5)
        ret_nac = reg["ret_nacionales"]
        ret_iva = tk.Entry(frame_ret_nac, width=15); ret_iva.insert(0, ret_nac["retencion_iva"]); ret_iva.grid(row=0, column=1)
        ret_gan = tk.Entry(frame_ret_nac, width=15); ret_gan.insert(0, ret_nac["retencion_ganancias"]); ret_gan.grid(row=0, column=3)
        ret_sicoss = tk.Entry(frame_ret_nac, width=15); ret_sicoss.insert(0, ret_nac["retencion_sicoss"]); ret_sicoss.grid(row=0, column=5)
        subtotal_ret_nac = tk.Entry(frame_ret_nac, width=15, state="readonly"); subtotal_ret_nac.insert(0, ret_nac["subtotal"]); subtotal_ret_nac.grid(row=0, column=7)
        tk.Label(frame_ret_nac, text="Retención IVA:").grid(row=0, column=0)
        tk.Label(frame_ret_nac, text="Retención Ganancias:").grid(row=0, column=2)
        tk.Label(frame_ret_nac, text="Retención SICOES:").grid(row=0, column=4)
        tk.Label(frame_ret_nac, text="Subtotal Ret. Nacionales:").grid(row=0, column=6)

        # Sección Retenciones Provinciales
        frame_ret_prov = tk.LabelFrame(edit_window, text="Retenciones Provinciales", padx=10, pady=10)
        frame_ret_prov.pack(fill="x", padx=10, pady=5)
        ret_prov = reg["ret_provinciales"]
        ret_iibb = []
        for i in range(4):
            prov = ttk.Combobox(frame_ret_prov, values=self.provincias); prov.set(ret_prov[i]["provincia"]); prov.grid(row=i, column=1)
            monto = tk.Entry(frame_ret_prov); monto.insert(0, ret_prov[i]["monto"]); monto.grid(row=i, column=3)
            tk.Label(frame_ret_prov, text=f"Retención IIBB {i+1} - Provincia:").grid(row=i, column=0)
            tk.Label(frame_ret_prov, text=f"Monto {i+1}:").grid(row=i, column=2)
            ret_iibb.append((prov, monto))

        # Sección Total
        frame_total = tk.LabelFrame(edit_window, text="Total", padx=10, pady=10)
        frame_total.pack(fill="x", padx=10, pady=5)
        monto_bruto = tk.Entry(frame_total, state="readonly"); monto_bruto.insert(0, reg["monto_bruto"]); monto_bruto.grid(row=0, column=1)
        tk.Label(frame_total, text="Monto Bruto:").grid(row=0, column=0)

        def guardar_edicion():
            try:
                self.registros[index] = {
                    "fecha_comprobante": fecha_comp.get(),
                    "num_comprobante_part1": num_comp1.get(),
                    "num_comprobante_part2": num_comp2.get(),
                    "tipo_comprobante": tipo_comp.get(),
                    "fecha_contabilizacion": fecha_contab.get(),
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
                        "exento": float(exento.get() or 0),
                        "subtotal": float(impuestos.get() or 0) + float(no_gravado.get() or 0) + float(exento.get() or 0)
                    },
                    "ret_nacionales": {
                        "retencion_iva": float(ret_iva.get() or 0),
                        "retencion_ganancias": float(ret_gan.get() or 0),
                        "retencion_sicoss": float(ret_sicoss.get() or 0),
                        "subtotal": float(ret_iva.get() or 0) + float(ret_gan.get() or 0) + float(ret_sicoss.get() or 0)
                    },
                    "ret_provinciales": [
                        {"provincia": prov.get(), "monto": float(monto.get() or 0)} for prov, monto in ret_iibb
                    ],
                    "monto_bruto": float(neto.get() or 0) + self.calcular_iva(float(neto.get() or 0), alicuota.get()) +
                                   float(impuestos.get() or 0) + float(no_gravado.get() or 0) + float(exento.get() or 0) -
                                   float(ret_iva.get() or 0) - float(ret_gan.get() or 0) - float(ret_sicoss.get() or 0) -
                                   sum(float(monto.get() or 0) for _, monto in ret_iibb)
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
                f.write(f"Fecha: {reg['fecha_comprobante']} | N° Comprobante: {reg['num_comprobante_part1']}-{reg['num_comprobante_part2']} | Tipo: {reg['tipo_comprobante']} | Fecha Contab.: {reg['fecha_contabilizacion']}\n")
                f.write(f"Cliente: {reg['cliente']['denominacion']} | CUIT: {reg['cliente']['cuit']}\n")
                f.write(f"Neto: {reg['factura']['neto']:.2f} | IVA ({reg['factura']['alicuota']}): {reg['factura']['iva']:.2f}\n")
                f.write(f"Otros Conceptos: Imp. Internos: {reg['otros']['impuestos_internos']:.2f} | Neto No Gravado: {reg['otros']['neto_no_gravado']:.2f} | Exento: {reg['otros']['exento']:.2f} | Subtotal: {reg['otros']['subtotal']:.2f}\n")
                f.write(f"Retenciones Nacionales: IVA: {reg['ret_nacionales']['retencion_iva']:.2f} | Ganancias: {reg['ret_nacionales']['retencion_ganancias']:.2f} | SICOES: {reg['ret_nacionales']['retencion_sicoss']:.2f} | Subtotal: {reg['ret_nacionales']['subtotal']:.2f}\n")
                f.write("Retenciones Provinciales:\n")
                for j, ret in enumerate(reg["ret_provinciales"]):
                    f.write(f"  IIBB {j+1}: {ret['provincia']} - {ret['monto']:.2f}\n")
                f.write(f"Monto Bruto: {reg['monto_bruto']:.2f}\n\n")
        messagebox.showinfo("Éxito", "Registros impresos en 'registros_contables.txt'")

    def calcular_total(self):
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para calcular")
            return

        total_neto = total_iva = total_impuestos = total_no_gravado = total_exento = total_subtotal_otros = total_ret_iva = total_ret_gan = total_ret_sicoss = total_subtotal_ret_nac = total_ret_prov = total_bruto = 0
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, "Resumen de Registros:\n\n")

        for reg in self.registros:
            total_neto += reg['factura']['neto']
            total_iva += reg['factura']['iva']
            total_impuestos += reg['otros']['impuestos_internos']
            total_no_gravado += reg['otros']['neto_no_gravado']
            total_exento += reg['otros']['exento']
            total_subtotal_otros += reg['otros']['subtotal']
            total_ret_iva += reg['ret_nacionales']['retencion_iva']
            total_ret_gan += reg['ret_nacionales']['retencion_ganancias']
            total_ret_sicoss += reg['ret_nacionales']['retencion_sicoss']
            total_subtotal_ret_nac += reg['ret_nacionales']['subtotal']
            total_ret_prov += sum(r['monto'] for r in reg['ret_provinciales'])
            total_bruto += reg['monto_bruto']

        self.resultado_texto.insert(tk.END, f"Total Neto: {total_neto:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total IVA: {total_iva:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Impuestos Internos: {total_impuestos:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Neto No Gravado: {total_no_gravado:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Exento: {total_exento:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Subtotal Otros: {total_subtotal_otros:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retención IVA: {total_ret_iva:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retención Ganancias: {total_ret_gan:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retención SICOES: {total_ret_sicoss:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Subtotal Ret. Nacionales: {total_subtotal_ret_nac:.2f}\n")
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
