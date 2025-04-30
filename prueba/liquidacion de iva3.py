import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import json
import os
import sqlite3
import pandas as pd

class FormularioContable:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Contable")
        self.root.geometry("900x1100")

        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect("registros_contables.db")
        self.crear_tabla()

        # Lista para almacenar registros en memoria (para compatibilidad)
        self.registros = self.cargar_datos()

        # Crear secciones del formulario
        self.crear_secciones()

        # Botones de acciones
        self.crear_botones()

        # Área de resultados
        self.resultado_texto = tk.Text(root, height=15, width=100)
        self.resultado_texto.pack(pady=10)

    def crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_comprobante TEXT,
            num_comprobante_part1 TEXT,
            num_comprobante_part2 TEXT,
            tipo_comprobante TEXT,
            fecha_contabilizacion TEXT,
            denominacion TEXT,
            domicilio TEXT,
            cuit TEXT,
            mail TEXT,
            telefono TEXT,
            neto REAL,
            alicuota TEXT,
            iva REAL,
            subtotal_factura REAL,
            impuestos_internos REAL,
            neto_no_gravado REAL,
            exento REAL,
            subtotal_otros REAL,
            retencion_iva REAL,
            retencion_ganancias REAL,
            retencion_sicoss REAL,
            subtotal_ret_nacionales REAL,
            ret_iibb_1_prov TEXT, ret_iibb_1_monto REAL,
            ret_iibb_2_prov TEXT, ret_iibb_2_monto REAL,
            ret_iibb_3_prov TEXT, ret_iibb_3_monto REAL,
            ret_iibb_4_prov TEXT, ret_iibb_4_monto REAL,
            subtotal_ret_provinciales REAL,
            total_bruto REAL
        )''')
        self.conn.commit()

    def crear_secciones(self):
        # Sección Comprobante
        frame_comprobante = tk.LabelFrame(self.root, text="Comprobante", padx=10, pady=10)
        frame_comprob aplikante.pack(fill="x", padx=10, pady=5)

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

        tk.Label(frame_factura, text="Subtotal Factura:").grid(row=3, column=0, sticky="w")
        self.subtotal_factura = tk.Entry(frame_factura, state="readonly")
        self.subtotal_factura.grid(row=3, column=1)
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

        tk.Label(frame_otros, text="Subtotal Otros:").grid(row=3, column=0, sticky="w")
        self.subtotal_otros = tk.Entry(frame_otros, state="readonly")
        self.subtotal_otros.grid(row=3, column=1)
        for entry in [self.impuestos_internos, self.neto_no_gravado, self.exento]:
            entry.bind("<KeyRelease>", self.calcular_subtotal_otros)

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

        tk.Label(frame_ret_nacionales, text="Subtotal Ret. Nacionales:").grid(row=3, column=0, sticky="w")
        self.subtotal_ret_nacionales = tk.Entry(frame_ret_nacionales, state="readonly")
        self.subtotal_ret_nacionales.grid(row=3, column=1)
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
            monto.bind("<KeyRelease>", self.calcular_subtotal_ret_provinciales)
            self.retenciones_iibb.append((prov, monto))

        tk.Label(frame_ret_provinciales, text="Subtotal Ret. Provinciales:").grid(row=4, column=0, sticky="w")
        self.subtotal_ret_provinciales = tk.Entry(frame_ret_provinciales, state="readonly")
        self.subtotal_ret_provinciales.grid(row=4, column=1)

        # Sección Total
        frame_total = tk.LabelFrame(self.root, text="Total", padx=10, pady=10)
        frame_total.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_total, text="Total Bruto:").grid(row=0, column=0, sticky="w")
        self.total_bruto = tk.Entry(frame_total, state="readonly")
        self.total_bruto.grid(row=0, column=1)
        for entry in [self.neto, self.impuestos_internos, self.neto_no_gravado, self.exento,
                      self.retencion_iva, self.retencion_ganancias, self.retencion_sicoss] + [m for _, m in self.retenciones_iibb]:
            entry.bind("<KeyRelease>", self.calcular_total_bruto)

    def crear_botones(self):
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Agregar Registro", command=self.agregar_registro).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Consultar Registros", command=self.consultar_registros).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Editar Registro", command=self.editar_registro).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Imprimir Registros", command=self.imprimir_registros).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones, text="Calcular Total", command=self.calcular_total).grid(row=0, column=4, padx=5)
        tk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_a_excel).grid(row=0, column=5, padx=5)

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
            self.subtotal_factura.config(state="normal")
            self.subtotal_factura.delete(0, tk.END)
            self.subtotal_factura.insert(0, f"{neto + iva:.2f}")
            self.subtotal_factura.config(state="readonly")
        except ValueError:
            self.iva.config(state="normal")
            self.iva.delete(0, tk.END)
            self.iva.insert(0, "0.00")
            self.iva.config(state="readonly")
            self.subtotal_factura.config(state="normal")
            self.subtotal_factura.delete(0, tk.END)
            self.subtotal_factura.insert(0, "0.00")
            self.subtotal_factura.config(state="readonly")

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

    def calcular_subtotal_ret_provinciales(self, event):
        try:
            subtotal = sum(float(monto.get() or 0) for _, monto in self.retenciones_iibb)
            self.subtotal_ret_provinciales.config(state="normal")
            self.subtotal_ret_provinciales.delete(0, tk.END)
            self.subtotal_ret_provinciales.insert(0, f"{subtotal:.2f}")
            self.subtotal_ret_provinciales.config(state="readonly")
        except ValueError:
            self.subtotal_ret_provinciales.config(state="normal")
            self.subtotal_ret_provinciales.delete(0, tk.END)
            self.subtotal_ret_provinciales.insert(0, "0.00")
            self.subtotal_ret_provinciales.config(state="readonly")

    def calcular_total_bruto(self, event):
        try:
            neto = float(self.neto.get() or 0)
            iva = float(self.iva.get() or 0)
            impuestos = float(self.impuestos_internos.get() or 0)
            no_gravado = float(self.neto_no_gravado.get() or 0)
            exento = float(self.exento.get() or 0)
            ret_iva = float(self.retencion_iva.get() or 0)
            ret_gan = float(self.retencion_ganancias.get() or 0)
            ret_sicoss = float(self.retencion_sicoss.get() or 0)
            ret_prov = float(self.subtotal_ret_provinciales.get() or 0)
            total = neto + iva + impuestos + no_gravado + exento - ret_iva - ret_gan - ret_sicoss - ret_prov
            self.total_bruto.config(state="normal")
            self.total_bruto.delete(0, tk.END)
            self.total_bruto.insert(0, f"{total:.2f}")
            self.total_bruto.config(state="readonly")
        except ValueError:
            self.total_bruto.config(state="normal")
            self.total_bruto.delete(0, tk.END)
            self.total_bruto.insert(0, "0.00")
            self.total_bruto.config(state="readonly")

    def agregar_registro(self):
        try:
            registro = (
                self.fecha_comprobante.get(),
                self.num_comprobante_part1.get(),
                self.num_comprobante_part2.get(),
                self.tipo_comprobante.get(),
                self.fecha_contabilizacion.get(),
                self.denominacion.get(),
                self.domicilio.get(),
                self.cuit.get(),
                self.mail.get(),
                self.telefono.get(),
                float(self.neto.get() or 0),
                self.alicuota.get(),
                float(self.iva.get() or 0),
                float(self.subtotal_factura.get() or 0),
                float(self.impuestos_internos.get() or 0),
                float(self.neto_no_gravado.get() or 0),
                float(self.exento.get() or 0),
                float(self.subtotal_otros.get() or 0),
                float(self.retencion_iva.get() or 0),
                float(self.retencion_ganancias.get() or 0),
                float(self.retencion_sicoss.get() or 0),
                float(self.subtotal_ret_nacionales.get() or 0),
                self.retenciones_iibb[0][0].get(), float(self.retenciones_iibb[0][1].get() or 0),
                self.retenciones_iibb[1][0].get(), float(self.retenciones_iibb[1][1].get() or 0),
                self.retenciones_iibb[2][0].get(), float(self.retenciones_iibb[2][1].get() or 0),
                self.retenciones_iibb[3][0].get(), float(self.retenciones_iibb[3][1].get() or 0),
                float(self.subtotal_ret_provinciales.get() or 0),
                float(self.total_bruto.get() or 0)
            )
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO registros (
                fecha_comprobante, num_comprobante_part1, num_comprobante_part2, tipo_comprobante, fecha_contabilizacion,
                denominacion, domicilio, cuit, mail, telefono, neto, alicuota, iva, subtotal_factura,
                impuestos_internos, neto_no_gravado, exento, subtotal_otros, retencion_iva, retencion_ganancias,
                retencion_sicoss, subtotal_ret_nacionales, ret_iibb_1_prov, ret_iibb_1_monto, ret_iibb_2_prov,
                ret_iibb_2_monto, ret_iibb_3_prov, ret_iibb_3_monto, ret_iibb_4_prov, ret_iibb_4_monto,
                subtotal_ret_provinciales, total_bruto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', registro)
            self.conn.commit()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Registro agregado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

    def limpiar_formulario(self):
        for entry in [self.fecha_comprobante, self.num_comprobante_part1, self.num_comprobante_part2, self.fecha_contabilizacion,
                      self.denominacion, self.domicilio, self.cuit, self.mail, self.telefono, self.neto,
                      self.impuestos_internos, self.neto_no_gravado, self.exento, self.retencion_iva,
                      self.retencion_ganancias, self.retencion_sicoss] + [m for _, m in self.retenciones_iibb]:
            entry.delete(0, tk.END)
        for entry in [self.iva, self.subtotal_factura, self.subtotal_otros, self.subtotal_ret_nacionales,
                      self.subtotal_ret_provinciales, self.total_bruto]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, "0.00")
            entry.config(state="readonly")

    def consultar_registros(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        self.registros = cursor.fetchall()
        self.resultado_texto.delete(1.0, tk.END)
        if not self.registros:
            self.resultado_texto.insert(tk.END, "No hay registros para mostrar.\n")
            return
        for i, reg in enumerate(self.registros):
            self.resultado_texto.insert(tk.END, f"Registro {reg[0]}: {reg[1]} | {reg[2]}-{reg[3]} | {reg[4]} | {reg[6]} | Neto: {reg[11]:.2f} | IVA: {reg[13]:.2f} | Total: {reg[31]:.2f}\n")

    def editar_registro(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        self.registros = cursor.fetchall()
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay registros para editar")
            return

        index_str = simpledialog.askstring("Editar", f"Ingrese el ID del registro a editar (1 a {len(self.registros)}):", parent=self.root)
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

        # Reutilizar diseño (simplificado para este ejemplo)
        entries = {}
        fields = [
            ("Fecha del Comprobante", reg[1]), ("N° Comprobante (5)", reg[2]), ("N° Comprobante (8)", reg[3]),
            ("Tipo de Comprobante", reg[4], ttk.Combobox, ["A", "B", "C", "E", "Ticket", "ND", "NC", "FC"]),
            ("Fecha de Contabilización", reg[5]), ("Denominación", reg[6]), ("Domicilio", reg[7]), ("CUIT", reg[8]),
            ("Mail", reg[9]), ("Teléfono", reg[10]), ("Neto", reg[11]), ("Alícuota IVA", reg[12], ttk.Combobox, ["10.5%", "21%", "27%"]),
            ("IVA", reg[13], tk.Entry, None, "readonly"), ("Subtotal Factura", reg[14], tk.Entry, None, "readonly"),
            ("Impuestos Internos", reg[15]), ("Neto No Gravado", reg[16]), ("Exento", reg[17]), ("Subtotal Otros", reg[18], tk.Entry, None, "readonly"),
            ("Retención IVA", reg[19]), ("Retención Ganancias", reg[20]), ("Retención SICOES", reg[21]),
            ("Subtotal Ret. Nacionales", reg[22], tk.Entry, None, "readonly"),
            ("Ret IIBB 1 Prov", reg[23], ttk.Combobox, self.provincias), ("Ret IIBB 1 Monto", reg[24]),
            ("Ret IIBB 2 Prov", reg[25], ttk.Combobox, self.provincias), ("Ret IIBB 2 Monto", reg[26]),
            ("Ret IIBB 3 Prov", reg[27], ttk.Combobox, self.provincias), ("Ret IIBB 3 Monto", reg[28]),
            ("Ret IIBB 4 Prov", reg[29], ttk.Combobox, self.provincias), ("Ret IIBB 4 Monto", reg[30]),
            ("Subtotal Ret. Provinciales", reg[31], tk.Entry, None, "readonly"), ("Total Bruto", reg[32], tk.Entry, None, "readonly")
        ]
        for i, (label, value, *widget_info) in enumerate(fields):
            tk.Label(edit_window, text=f"{label}:").grid(row=i, column=0, sticky="w")
            widget_type = widget_info[0] if widget_info else tk.Entry
            options = widget_info[1] if len(widget_info) > 1 else None
            state = widget_info[2] if len(widget_info) > 2 else None
            if widget_type == ttk.Combobox:
                entry = widget_type(edit_window, values=options)
                entry.set(value)
            else:
                entry = widget_type(edit_window)
                entry.insert(0, value)
                if state:
                    entry.config(state=state)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def guardar_edicion():
            try:
                cursor.execute('''UPDATE registros SET
                    fecha_comprobante=?, num_comprobante_part1=?, num_comprobante_part2=?, tipo_comprobante=?, fecha_contabilizacion=?,
                    denominacion=?, domicilio=?, cuit=?, mail=?, telefono=?, neto=?, alicuota=?, iva=?, subtotal_factura=?,
                    impuestos_internos=?, neto_no_gravado=?, exento=?, subtotal_otros=?, retencion_iva=?, retencion_ganancias=?,
                    retencion_sicoss=?, subtotal_ret_nacionales=?, ret_iibb_1_prov=?, ret_iibb_1_monto=?, ret_iibb_2_prov=?,
                    ret_iibb_2_monto=?, ret_iibb_3_prov=?, ret_iibb_3_monto=?, ret_iibb_4_prov=?, ret_iibb_4_monto=?,
                    subtotal_ret_provinciales=?, total_bruto=?
                    WHERE id=?''', (
                    entries["Fecha del Comprobante"].get(), entries["N° Comprobante (5)"].get(), entries["N° Comprobante (8)"].get(),
                    entries["Tipo de Comprobante"].get(), entries["Fecha de Contabilización"].get(), entries["Denominación"].get(),
                    entries["Domicilio"].get(), entries["CUIT"].get(), entries["Mail"].get(), entries["Teléfono"].get(),
                    float(entries["Neto"].get() or 0), entries["Alícuota IVA"].get(), float(entries["IVA"].get() or 0),
                    float(entries["Subtotal Factura"].get() or 0), float(entries["Impuestos Internos"].get() or 0),
                    float(entries["Neto No Gravado"].get() or 0), float(entries["Exento"].get() or 0),
                    float(entries["Subtotal Otros"].get() or 0), float(entries["Retención IVA"].get() or 0),
                    float(entries["Retención Ganancias"].get() or 0), float(entries["Retención SICOES"].get() or 0),
                    float(entries["Subtotal Ret. Nacionales"].get() or 0), entries["Ret IIBB 1 Prov"].get(),
                    float(entries["Ret IIBB 1 Monto"].get() or 0), entries["Ret IIBB 2 Prov"].get(),
                    float(entries["Ret IIBB 2 Monto"].get() or 0), entries["Ret IIBB 3 Prov"].get(),
                    float(entries["Ret IIBB 3 Monto"].get() or 0), entries["Ret IIBB 4 Prov"].get(),
                    float(entries["Ret IIBB 4 Monto"].get() or 0), float(entries["Subtotal Ret. Provinciales"].get() or 0),
                    float(entries["Total Bruto"].get() or 0), reg[0]
                ))
                self.conn.commit()
                edit_window.destroy()
                messagebox.showinfo("Éxito", "Registro editado correctamente")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

        tk.Button(edit_window, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)

    def imprimir_registros(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()
        if not registros:
            messagebox.showwarning("Advertencia", "No hay registros para imprimir")
            return

        with open("registros_contables.txt", "w", encoding="utf-8") as f:
            f.write("Registros Contables:\n\n")
            for reg in registros:
                f.write(f"Registro {reg[0]}:\n")
                f.write(f"Fecha: {reg[1]} | N° Comprobante: {reg[2]}-{reg[3]} | Tipo: {reg[4]} | Fecha Contab.: {reg[5]}\n")
                f.write(f"Cliente: {reg[6]} | CUIT: {reg[8]}\n")
                f.write(f"Neto: {reg[11]:.2f} | IVA ({reg[12]}): {reg[13]:.2f} | Subtotal Factura: {reg[14]:.2f}\n")
                f.write(f"Impuestos Internos: {reg[15]:.2f} | Neto No Gravado: {reg[16]:.2f} | Exento: {reg[17]:.2f} | Subtotal Otros: {reg[18]:.2f}\n")
                f.write(f"Retenciones Nacionales: IVA: {reg[19]:.2f} | Ganancias: {reg[20]:.2f} | SICOES: {reg[21]:.2f} | Subtotal: {reg[22]:.2f}\n")
                f.write(f"Retenciones Provinciales: IIBB 1: {reg[23]} - {reg[24]:.2f} | IIBB 2: {reg[25]} - {reg[26]:.2f} | IIBB 3: {reg[27]} - {reg[28]:.2f} | IIBB 4: {reg[29]} - {reg[30]:.2f} | Subtotal: {reg[31]:.2f}\n")
                f.write(f"Total Bruto: {reg[32]:.2f}\n\n")
        messagebox.showinfo("Éxito", "Registros impresos en 'registros_contables.txt'")

    def calcular_total(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()
        if not registros:
            messagebox.showwarning("Advertencia", "No hay registros para calcular")
            return

        total_neto = total_iva = total_impuestos = total_no_gravado = total_exento = total_ret_nac = total_ret_prov = total_bruto = 0
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, "Resumen de Registros:\n\n")

        for reg in registros:
            total_neto += reg[11]
            total_iva += reg[13]
            total_impuestos += reg[15]
            total_no_gravado += reg[16]
            total_exento += reg[17]
            total_ret_nac += reg[22]
            total_ret_prov += reg[31]
            total_bruto += reg[32]

        self.resultado_texto.insert(tk.END, f"Total Neto: {total_neto:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total IVA: {total_iva:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Impuestos Internos: {total_impuestos:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Neto No Gravado: {total_no_gravado:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Exento: {total_exento:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retenciones Nacionales: {total_ret_nac:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Retenciones Provinciales: {total_ret_prov:.2f}\n")
        self.resultado_texto.insert(tk.END, f"Total Bruto: {total_bruto:.2f}\n")

    def exportar_a_excel(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()
        if not registros:
            messagebox.showwarning("Advertencia", "No hay registros para exportar")
            return

        columnas = ["ID", "Fecha Comprobante", "N° Comprobante (5)", "N° Comprobante (8)", "Tipo Comprobante", "Fecha Contabilización",
                   "Denominación", "Domicilio", "CUIT", "Mail", "Teléfono", "Neto", "Alícuota", "IVA", "Subtotal Factura",
                   "Impuestos Internos", "Neto No Gravado", "Exento", "Subtotal Otros", "Retención IVA", "Retención Ganancias",
                   "Retención SICOES", "Subtotal Ret. Nacionales", "Ret IIBB 1 Prov", "Ret IIBB 1 Monto", "Ret IIBB 2 Prov",
                   "Ret IIBB 2 Monto", "Ret IIBB 3 Prov", "Ret IIBB 3 Monto", "Ret IIBB 4 Prov", "Ret IIBB 4 Monto",
                   "Subtotal Ret. Provinciales", "Total Bruto"]
        df = pd.DataFrame(registros, columns=columnas)
        df.to_excel("registros_contables.xlsx", index=False)
        messagebox.showinfo("Éxito", "Registros exportados a 'registros_contables.xlsx'")

    def cargar_datos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registros")
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioContable(root)
    root.mainloop()
