import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import threading
import socket
import ipaddress
import json
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import subprocess
import platform

# =========================================
# CONFIGURACIÓN
# =========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    8080: 'HTTP-Alt',
    8443: 'HTTPS-Alt'
}

# =========================================
# APP
# =========================================

class NeosToolkit(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Neos Toolkit")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_frame()

    # =========================================
    # SIDEBAR
    # =========================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        title = ctk.CTkLabel(
            self.sidebar,
            text="Neos TOOLKIT",
            font=("Consolas", 24, "bold")
        )
        title.pack(pady=(30, 40))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Calculadora", self.show_calculator),
            ("Escaneo Red", self.show_network_scanner),
            ("Port Scanner", self.show_port_scanner),
            ("Limpiar Logs", self.clear_logs)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                font=("Consolas", 15),
                command=command
            )
            btn.pack(fill="x", padx=20, pady=10)

    # =========================================
    # MAIN FRAME
    # =========================================

    def create_main_frame(self):

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Dashboard",
            font=("Consolas", 28, "bold")
        )
        self.header.grid(row=0, column=0, pady=15)

        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.show_dashboard()

    # =========================================
    # UTILIDADES
    # =========================================

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def log(self, text):
        self.logs.insert("end", f"{text}\n")
        self.logs.see("end")

    def clear_logs(self):
        try:
            self.logs.delete("1.0", "end")
        except:
            pass

    # =========================================
    # DASHBOARD
    # =========================================

    def show_dashboard(self):

        self.clear_content()
        self.header.configure(text="Dashboard")

        title = ctk.CTkLabel(
            self.content_frame,
            text="Neos Toolkit",
            font=("Consolas", 30, "bold")
        )
        title.pack(pady=40)

        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Herramientas de red y utilidades",
            font=("Consolas", 18)
        )
        subtitle.pack(pady=10)

    # =========================================
    # CALCULADORA
    # =========================================

    def show_calculator(self):

        self.clear_content()
        self.header.configure(text="Calculadora")

        frame = ctk.CTkFrame(self.content_frame)
        frame.pack(pady=40)

        self.num1 = ctk.CTkEntry(frame, placeholder_text="Número 1", width=250)
        self.num1.pack(pady=10)

        self.num2 = ctk.CTkEntry(frame, placeholder_text="Número 2", width=250)
        self.num2.pack(pady=10)

        self.result_label = ctk.CTkLabel(
            frame,
            text="Resultado: ",
            font=("Consolas", 20, "bold")
        )
        self.result_label.pack(pady=20)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)

        operations = [
            ("+", self.add),
            ("-", self.subtract),
            ("×", self.multiply),
            ("÷", self.divide)
        ]

        for text, cmd in operations:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                width=60,
                command=cmd
            )
            btn.pack(side="left", padx=10)

    def get_numbers(self):

        try:
            n1 = float(self.num1.get())
            n2 = float(self.num2.get())
            return n1, n2
        except:
            messagebox.showerror("Error", "Ingresa números válidos")
            return None, None

    def add(self):
        n1, n2 = self.get_numbers()
        if n1 is not None:
            self.result_label.configure(text=f"Resultado: {n1 + n2}")

    def subtract(self):
        n1, n2 = self.get_numbers()
        if n1 is not None:
            self.result_label.configure(text=f"Resultado: {n1 - n2}")

    def multiply(self):
        n1, n2 = self.get_numbers()
        if n1 is not None:
            self.result_label.configure(text=f"Resultado: {n1 * n2}")

    def divide(self):
        n1, n2 = self.get_numbers()
        if n1 is not None:
            if n2 == 0:
                messagebox.showerror("Error", "No se puede dividir entre 0")
                return
            self.result_label.configure(text=f"Resultado: {n1 / n2}")

    # =========================================
    # ESCANEO RED
    # =========================================

    def show_network_scanner(self):

        self.clear_content()
        self.header.configure(text="Escaneo Red")

        top = ctk.CTkFrame(self.content_frame)
        top.pack(fill="x", pady=10)

        self.network_entry = ctk.CTkEntry(
            top,
            placeholder_text="Red o CIDR (ej. 192.168.1.0/24)",
            width=350
        )
        self.network_entry.pack(side="left", padx=10)

        scan_btn = ctk.CTkButton(
            top,
            text="Escanear",
            command=self.start_network_scan
        )
        scan_btn.pack(side="left", padx=10)

        self.network_text = ctk.CTkTextbox(
            self.content_frame,
            width=800,
            height=380
        )
        self.network_text.pack(fill="both", expand=True, pady=20)

        self.network_results = []

    def start_network_scan(self):
        threading.Thread(target=self.network_scan, daemon=True).start()

    def network_scan(self):
        self.network_text.delete("0.0", "end")
        target = self.network_entry.get().strip()

        if not target:
            messagebox.showerror("Error", "Ingresa una red o CIDR válido")
            return

        all_hosts = []
        if "/" in target:
            try:
                net = ipaddress.ip_network(target, strict=False)
                all_hosts = [str(ip) for ip in net.hosts()]
            except Exception:
                messagebox.showerror("Error", "CIDR inválido")
                return
        else:
            if target.endswith("."):
                prefix = target
            else:
                prefix = target + "."
            all_hosts = [f"{prefix}{i}" for i in range(1, 255)]

        self.network_results = []
        self.network_text.insert("end", f"Escaneando {len(all_hosts)} hosts...\n")

        def ping_host(ip):
            sistema = platform.system().lower()
            if sistema == "windows":
                comando = ["ping", "-n", "1", "-w", "200", ip]
            else:
                comando = ["ping", "-c", "1", "-W", "1", ip]

            resultado = subprocess.run(
                comando,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if resultado.returncode == 0:
                self.network_results.append(ip)
                self.network_text.insert("end", f"[ACTIVO] {ip}\n")
                self.network_text.see("end")

        with ThreadPoolExecutor(max_workers=50) as executor:
            for ip in all_hosts:
                executor.submit(ping_host, ip)

        self.network_text.insert("end", "\nEscaneo terminado.\n")
        if self.network_results:
            self.network_text.insert("end", f"{len(self.network_results)} hosts activos encontrados.\n")
        else:
            self.network_text.insert("end", "No se encontraron hosts activos.\n")
        self.network_text.see("end")

    # =========================================
    # PORT SCANNER
    # =========================================

    def show_port_scanner(self):

        self.clear_content()
        self.header.configure(text="Port Scanner")

        top = ctk.CTkFrame(self.content_frame)
        top.pack(fill="x", pady=10)

        self.ip_entry = ctk.CTkEntry(
            top,
            placeholder_text="IP o CIDR",
            width=250
        )
        self.ip_entry.pack(side="left", padx=10)

        self.ports_entry = ctk.CTkEntry(
            top,
            placeholder_text="Puertos (22,80,443)",
            width=250
        )
        self.ports_entry.pack(side="left", padx=10)

        scan_btn = ctk.CTkButton(
            top,
            text="Escanear",
            command=self.start_port_scan
        )
        scan_btn.pack(side="left", padx=10)

        export_btn = ctk.CTkButton(
            top,
            text="Exportar JSON",
            command=self.export_json
        )
        export_btn.pack(side="left", padx=10)

        columns = ("IP", "Puerto", "Servicio", "Estado")

        self.tree = ttk.Treeview(
            self.content_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True, pady=20)

        self.scan_results = []

    def start_port_scan(self):
        threading.Thread(target=self.port_scan, daemon=True).start()

    def port_scan(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        target = self.ip_entry.get().strip()

        ports_input = self.ports_entry.get().strip()

        if ports_input:
            ports = [int(p.strip()) for p in ports_input.split(",")]
        else:
            ports = list(COMMON_PORTS.keys())

        self.scan_results = []

        def scan(ip, port):

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)

                result = sock.connect_ex((ip, port))

                if result == 0:

                    service = COMMON_PORTS.get(port, "Unknown")

                    self.tree.insert(
                        "",
                        "end",
                        values=(ip, port, service, "OPEN")
                    )

                    self.scan_results.append({
                        "ip": ip,
                        "port": port,
                        "service": service,
                        "state": "open",
                        "timestamp": datetime.now().isoformat()
                    })

                sock.close()

            except:
                pass

        if "/" in target:

            try:
                net = ipaddress.ip_network(target, strict=False)

                threads = []

                for ip in net.hosts():
                    ip = str(ip)

                    for port in ports:
                        t = threading.Thread(target=scan, args=(ip, port))
                        threads.append(t)
                        t.start()

                for t in threads:
                    t.join()

            except:
                messagebox.showerror("Error", "CIDR inválido")

        else:

            threads = []

            for port in ports:
                t = threading.Thread(target=scan, args=(target, port))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

    def export_json(self):

        if not self.scan_results:
            messagebox.showwarning("Vacío", "No hay resultados")
            return

        file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )

        if not file:
            return

        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.scan_results, f, indent=2)

        messagebox.showinfo("Exportado", "Resultados guardados")

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app = NeosToolkit()
    app.mainloop()