import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import sqlite3


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

        tk.Label(frame_factura, text="Subtotal Factura:").grid(row=3, column=0, sticky="w")
        self.subtotal_factura = tk.Entry(frame_factura, state="readonly")
        self.subtotal_factura
