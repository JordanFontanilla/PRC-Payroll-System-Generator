import customtkinter as ctk
import tkinter as tk

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="white")
        self.controller = controller
        self.rows = 8  # 7 data + 1 header
        self.cols = 11
        self._build_ui()

    def _build_ui(self):
        # Top bar
        topbar = ctk.CTkFrame(self, fg_color="white")
        topbar.pack(fill=ctk.X, pady=(5, 0))
        def go_to_excel_import():
            if self.controller:
                self.controller.show_frame("ExcelImportPage")
        ctk.CTkButton(topbar, text='>', font=('Consolas', 18, 'bold'), fg_color="white", text_color="#0041C2", hover_color="#e6e6e6", width=40, height=40, corner_radius=20, command=go_to_excel_import).pack(side=ctk.LEFT, padx=(10, 20))
        btn_style = {'fg_color': '#0041C2', 'text_color': 'white', 'hover_color': '#003399', 'font': ("Arial", 12, "bold"), 'corner_radius': 8, 'width': 160, 'height': 32}
        ctk.CTkLabel(topbar, text='Reports', font=("Montserrat", 32, "normal"), text_color="#222").pack(side=ctk.LEFT, pady=10)
        # Controls
        btn_style = {'fg_color': '#0041C2', 'text_color': 'white', 'hover_color': '#003399', 'font': ("Arial", 12, "bold"), 'corner_radius': 8, 'width': 120, 'height': 32}
        controls = ctk.CTkFrame(topbar, fg_color="white")
        controls.pack(side=ctk.RIGHT, padx=10)
        ctk.CTkLabel(controls, text='Columns', font=('Arial', 11), text_color="#0041C2").grid(row=0, column=0, padx=(0, 2))
        ctk.CTkButton(controls, text='+', font=('Arial', 13, 'bold'), text_color="#0041C2", fg_color="white", hover_color="#e6e6e6", width=32, height=32, command=self.add_col).grid(row=0, column=1)
        ctk.CTkButton(controls, text='-', font=('Arial', 13, 'bold'), text_color="#0041C2", fg_color="white", hover_color="#e6e6e6", width=32, height=32, command=self.remove_col).grid(row=0, column=2)
        ctk.CTkLabel(controls, text='Rows', font=('Arial', 11), text_color="#0041C2").grid(row=0, column=3, padx=(15, 2))
        ctk.CTkButton(controls, text='+', font=('Arial', 13, 'bold'), text_color="#0041C2", fg_color="white", hover_color="#e6e6e6", width=32, height=32, command=self.add_row).grid(row=0, column=4)
        ctk.CTkButton(controls, text='-', font=('Arial', 13, 'bold'), text_color="#0041C2", fg_color="white", hover_color="#e6e6e6", width=32, height=32, command=self.remove_row).grid(row=0, column=5)
        # Table frame
        table_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="#4B2ED5")
        table_frame.pack(fill=ctk.BOTH, expand=True, padx=8, pady=(10, 8))
        # Canvas for scrolling
        self.canvas = ctk.CTkCanvas(table_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll = ctk.CTkScrollbar(table_frame, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.inner = ctk.CTkFrame(self.canvas, fg_color="white")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._draw_table()
        self.inner.bind("<Configure>", lambda e: self._update_scrollregion())
        def _on_mousewheel(event):
            if self.canvas.bbox("all") and self.canvas.winfo_height() < self.canvas.bbox("all")[3]:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self._canvas = self.canvas

    def _draw_table(self):
        for widget in self.inner.winfo_children():
            widget.destroy()
        header_font = ("Arial", 13, "bold")
        cell_font = ("Arial", 12)
        default_headers = [
            "PAP / UAC\nCODE", "MO.SALARY", "PERA\nAMOUNT", "GSIS", "PHIC", "HDMF", "OTHER\nDEDUCTIONS", "", "", "", ""
        ]
        default_data = [
            ["A.I.a.1", "", "", "", "", "", "", "", "", "", ""],
            ["A.II.a.1", "", "", "", "", "", "", "", "", "", ""],
            ["A.III.a.4", "", "", "", "", "", "", "", "", "", ""],
            ["A.III.b.6", "", "", "", "", "", "", "", "", "", ""],
            ["A.III.b.7", "", "", "", "", "", "", "", "", "", ""],
            ["A.III.b.8", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""]
        ]
        # Use current headers/data if already set, else use defaults
        if not hasattr(self, 'headers'):
            self.headers = default_headers[:self.cols] + ["" for _ in range(self.cols - len(default_headers))]
        if not hasattr(self, 'data'):
            self.data = [row[:self.cols] + ["" for _ in range(self.cols - len(row))] for row in default_data[:self.rows-1]]
            while len(self.data) < self.rows-1:
                self.data.append(["" for _ in range(self.cols)])
        # Draw header row
        for c in range(self.cols):
            entry = ctk.CTkEntry(self.inner, width=120, justify="center", border_width=1, corner_radius=0)
            entry.insert(0, self.headers[c] if c < len(self.headers) else "")
            entry.configure(fg_color="#22C32A", text_color="white", font=header_font)
            entry.grid(row=0, column=c, sticky="nsew", padx=0, pady=0, ipady=10)
            entry.bind('<KeyRelease>', lambda e, col=c: self._update_header(col, e.widget.get()))
            self.inner.grid_columnconfigure(c, weight=1)
        # Draw data rows
        for r in range(1, self.rows):
            for c in range(self.cols):
                entry = ctk.CTkEntry(self.inner, width=120, justify="center", border_width=1, corner_radius=0)
                entry.insert(0, self.data[r-1][c] if c < len(self.data[r-1]) else "")
                entry.configure(fg_color="white", text_color="black", font=cell_font)
                entry.grid(row=r, column=c, sticky="nsew", padx=0, pady=0, ipady=10)
                entry.bind('<KeyRelease>', lambda e, row=r-1, col=c: self._update_data(row, col, e.widget.get()))
            self.inner.grid_rowconfigure(r, weight=1)

    def _update_header(self, col, value):
        self.headers[col] = value

    def _update_data(self, row, col, value):
        self.data[row][col] = value

    def _update_scrollregion(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.canvas.bbox("all") and self.canvas.winfo_height() >= self.canvas.bbox("all")[3]:
            self.canvas.yview_moveto(0)
            self.canvas.configure(yscrollcommand=lambda *args: None)
        else:
            self.canvas.configure(yscrollcommand=self.v_scroll.set)

    def add_row(self):
        self.rows += 1
        self.data.append(["" for _ in range(self.cols)])
        self._draw_table()
        self.inner.update_idletasks()

    def remove_row(self):
        if self.rows > 2:
            self.rows -= 1
            if len(self.data) > 0:
                self.data.pop()
            self._draw_table()
            self.inner.update_idletasks()

    def add_col(self):
        self.cols += 1
        self.headers.append("")
        for row in self.data:
            row.append("")
        self._draw_table()
        self.inner.update_idletasks()

    def remove_col(self):
        if self.cols > 2:
            self.cols -= 1
            if len(self.headers) > 0:
                self.headers.pop()
            for row in self.data:
                if len(row) > 0:
                    row.pop()
            self._draw_table()
            self.inner.update_idletasks()

    def destroy(self):
        if hasattr(self, '_canvas'):
            self._canvas.unbind_all("<MouseWheel>")
        super().destroy()
