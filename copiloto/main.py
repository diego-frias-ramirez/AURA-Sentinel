import customtkinter as ctk
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from typing import List, Dict
import threading
import time

# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

@dataclass
class FichaMedica:
    tipo_sangre: str
    alergias: List[str]
    medicamentos: List[str]
    condiciones: List[str]

@dataclass
class Usuario:
    nombre: str
    edad: int
    telefono: str
    ficha_medica: FichaMedica

@dataclass
class Ubicacion:
    latitud: float
    longitud: float
    direccion: str

@dataclass
class Emergencia:
    id: str
    usuario: Usuario
    ubicacion: Ubicacion
    tipo: str
    prioridad: str
    timestamp: str
    estado: str

class SistemaIA:
    """Motor de IA para clasificación y sugerencias"""
    
    def clasificar_emergencia(self, tipo: str) -> Dict:
        clasificaciones = {
            'medica': {
                'prioridad': 'CRÍTICA',
                'recursos': ['Ambulancia avanzada', 'Paramédicos', 'Equipo médico'],
                'protocolo': 'Soporte vital avanzado inmediato',
                'preguntas': [
                    '¿El paciente está consciente?',
                    '¿Respira con normalidad?',
                    '¿Presenta dolor de pecho?',
                    '¿Hay sangrado visible?'
                ],
                'tiempo': '3-5 min',
                'color': '#dc2626'
            },
            'incendio': {
                'prioridad': 'CRÍTICA',
                'recursos': ['Bomberos', 'Ambulancia', 'Policía de apoyo'],
                'protocolo': 'Evacuación y control de incendio',
                'preguntas': [
                    '¿Hay personas atrapadas?',
                    '¿Qué tipo de edificio es?',
                    '¿El fuego se está propagando?',
                    '¿Hay materiales peligrosos?'
                ],
                'tiempo': '2-4 min',
                'color': '#dc2626'
            },
            'seguridad': {
                'prioridad': 'ALTA',
                'recursos': ['Patrulla policial', 'Unidad táctica'],
                'protocolo': 'Respuesta de seguridad inmediata',
                'preguntas': [
                    '¿Hay armas involucradas?',
                    '¿Cuántas personas están involucradas?',
                    '¿Hay heridos?',
                    '¿El agresor sigue en el lugar?'
                ],
                'tiempo': '4-6 min',
                'color': '#ea580c'
            },
            'panico': {
                'prioridad': 'ALTA',
                'recursos': ['Patrulla policial', 'Apoyo psicológico'],
                'protocolo': 'Evaluación de amenaza y contención',
                'preguntas': [
                    '¿Se siente en peligro inmediato?',
                    '¿Está solo/a?',
                    '¿Puede describir la situación?',
                    '¿Necesita refugio seguro?'
                ],
                'tiempo': '5-8 min',
                'color': '#f59e0b'
            }
        }
        return clasificaciones.get(tipo, clasificaciones['panico'])

class Copiloto911(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Copiloto 911 con IA")
        self.geometry("1600x900")
        
        # Variables
        self.emergencias_pendientes = []
        self.emergencia_actual = None
        
        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear interfaz
        self.crear_panel_emergencias()
        self.crear_panel_principal()
        
        # Iniciar simulación
        self.simular_emergencia_entrante()
    
    def crear_panel_emergencias(self):
        """Panel izquierdo con lista de emergencias"""
        panel = ctk.CTkFrame(self, corner_radius=0)
        panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="#1e293b", corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        titulo = ctk.CTkLabel(
            header,
            text="EMERGENCIAS ACTIVAS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        titulo.pack(pady=15)
        
        # Scrollable frame para emergencias
        self.scroll_emergencias = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent"
        )
        self.scroll_emergencias.pack(fill="both", expand=True, padx=10, pady=10)
    
    def crear_panel_principal(self):
        """Panel principal con detalles de emergencia"""
        self.panel_principal = ctk.CTkFrame(self, corner_radius=0)
        self.panel_principal.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # Estado inicial
        self.mostrar_estado_inicial()
    
    def mostrar_estado_inicial(self):
        """Muestra mensaje de espera"""
        for widget in self.panel_principal.winfo_children():
            widget.destroy()
        
        contenedor = ctk.CTkFrame(self.panel_principal, fg_color="transparent")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")
        
        label = ctk.CTkLabel(
            contenedor,
            text="Esperando emergencias...",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#64748b"
        )
        label.pack()
        
        sublabel = ctk.CTkLabel(
            contenedor,
            text="El sistema está listo para recibir alertas de AURA",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8"
        )
        sublabel.pack(pady=10)
    
    def agregar_emergencia_lista(self, emergencia: Emergencia):
        """Agrega una emergencia a la lista lateral"""
        frame = ctk.CTkFrame(
            self.scroll_emergencias,
            fg_color="#1e293b",
            corner_radius=10
        )
        frame.pack(fill="x", pady=5)
        
        # Indicador de prioridad
        clasificacion = SistemaIA().clasificar_emergencia(emergencia.tipo)
        indicador = ctk.CTkFrame(
            frame,
            width=5,
            fg_color=clasificacion['color'],
            corner_radius=0
        )
        indicador.pack(side="left", fill="y")
        
        # Contenido
        contenido = ctk.CTkFrame(frame, fg_color="transparent")
        contenido.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        # Fila 1: Nombre y hora
        fila1 = ctk.CTkFrame(contenido, fg_color="transparent")
        fila1.pack(fill="x")
        
        nombre = ctk.CTkLabel(
            fila1,
            text=emergencia.usuario.nombre,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        nombre.pack(side="left")
        
        hora = ctk.CTkLabel(
            fila1,
            text=datetime.fromisoformat(emergencia.timestamp).strftime("%H:%M:%S"),
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        hora.pack(side="right")
        
        # Fila 2: Tipo y prioridad
        tipo = ctk.CTkLabel(
            contenido,
            text=f"{emergencia.tipo.upper()} • {emergencia.prioridad}",
            font=ctk.CTkFont(size=12),
            text_color="#60a5fa",
            anchor="w"
        )
        tipo.pack(fill="x", pady=(5, 0))
        
        # Botón para ver detalles
        btn = ctk.CTkButton(
            frame,
            text="VER",
            width=70,
            height=32,
            command=lambda e=emergencia: self.mostrar_emergencia(e),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        btn.pack(side="right", padx=10)
    
    def mostrar_emergencia(self, emergencia: Emergencia):
        """Muestra los detalles completos de la emergencia"""
        self.emergencia_actual = emergencia
        
        # Limpiar panel
        for widget in self.panel_principal.winfo_children():
            widget.destroy()
        
        # Crear scroll para todo el contenido
        scroll = ctk.CTkScrollableFrame(self.panel_principal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header con alerta
        self.crear_header_emergencia(scroll, emergencia)
        
        # Grid principal
        grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, pady=10)
        
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Columna izquierda
        self.crear_info_usuario(grid_frame, emergencia, 0, 0)
        self.crear_ficha_medica(grid_frame, emergencia, 0, 1)
        self.crear_ubicacion(grid_frame, emergencia, 0, 2)
        
        # Columna derecha
        self.crear_sugerencias_ia(grid_frame, emergencia, 1, 0)
        self.crear_protocolo(grid_frame, emergencia, 1, 1)
        self.crear_acciones(grid_frame, emergencia, 1, 2)
    
    def crear_header_emergencia(self, parent, emergencia):
        """Header con información crítica"""
        header = ctk.CTkFrame(parent, fg_color="#dc2626", corner_radius=10)
        header.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Título
        titulo = ctk.CTkLabel(
            content,
            text=f"EMERGENCIA ACTIVA - {emergencia.id}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        titulo.pack(anchor="w")
        
        # Detalles
        detalles = ctk.CTkFrame(content, fg_color="transparent")
        detalles.pack(fill="x", pady=(10, 0))
        
        clasificacion = SistemaIA().clasificar_emergencia(emergencia.tipo)
        
        info_items = [
            f"Tipo: {emergencia.tipo.upper()}",
            f"Prioridad: {emergencia.prioridad}",
            f"Tiempo de respuesta: {clasificacion['tiempo']}",
            f"Hora: {datetime.fromisoformat(emergencia.timestamp).strftime('%H:%M:%S')}"
        ]
        
        for item in info_items:
            lbl = ctk.CTkLabel(
                detalles,
                text=item,
                font=ctk.CTkFont(size=13),
                text_color="#fecaca"
            )
            lbl.pack(side="left", padx=(0, 30))
    
    def crear_info_usuario(self, parent, emergencia, col, row):
        """Tarjeta con información del usuario"""
        frame = self.crear_tarjeta(parent, "INFORMACIÓN DEL USUARIO", col, row)
        
        # Nombre y edad
        nombre = ctk.CTkLabel(
            frame,
            text=emergencia.usuario.nombre,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        nombre.pack(anchor="w", pady=(0, 5))
        
        edad = ctk.CTkLabel(
            frame,
            text=f"{emergencia.usuario.edad} años",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8"
        )
        edad.pack(anchor="w", pady=(0, 15))
        
        # Teléfono
        tel_frame = ctk.CTkFrame(frame, fg_color="#1e293b", corner_radius=8)
        tel_frame.pack(fill="x", pady=5)
        
        tel_label = ctk.CTkLabel(
            tel_frame,
            text=f"Teléfono: {emergencia.usuario.telefono}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#60a5fa"
        )
        tel_label.pack(pady=12, padx=15)
    
    def crear_ficha_medica(self, parent, emergencia, col, row):
        """Tarjeta con ficha médica"""
        frame = self.crear_tarjeta(parent, "FICHA MÉDICA CRÍTICA", col, row)
        
        ficha = emergencia.usuario.ficha_medica
        
        # Tipo de sangre (destacado)
        sangre_frame = ctk.CTkFrame(frame, fg_color="#dc2626", corner_radius=8)
        sangre_frame.pack(fill="x", pady=(0, 15))
        
        sangre_label = ctk.CTkLabel(
            sangre_frame,
            text=f"TIPO DE SANGRE: {ficha.tipo_sangre}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        sangre_label.pack(pady=12)
        
        # Alergias
        if ficha.alergias:
            alergia_titulo = ctk.CTkLabel(
                frame,
                text="ALERGIAS:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#ef4444",
                anchor="w"
            )
            alergia_titulo.pack(fill="x", pady=(0, 5))
            
            for alergia in ficha.alergias:
                alergia_frame = ctk.CTkFrame(frame, fg_color="#7f1d1d", corner_radius=6)
                alergia_frame.pack(fill="x", pady=2)
                
                alergia_label = ctk.CTkLabel(
                    alergia_frame,
                    text=f"• {alergia}",
                    font=ctk.CTkFont(size=12),
                    text_color="#fca5a5"
                )
                alergia_label.pack(anchor="w", pady=8, padx=12)
        
        # Condiciones médicas
        if ficha.condiciones:
            cond_titulo = ctk.CTkLabel(
                frame,
                text="CONDICIONES MÉDICAS:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#f59e0b",
                anchor="w"
            )
            cond_titulo.pack(fill="x", pady=(15, 5))
            
            for condicion in ficha.condiciones:
                cond_label = ctk.CTkLabel(
                    frame,
                    text=f"• {condicion}",
                    font=ctk.CTkFont(size=12),
                    text_color="#fbbf24",
                    anchor="w"
                )
                cond_label.pack(fill="x", pady=2)
        
        # Medicamentos
        if ficha.medicamentos:
            med_titulo = ctk.CTkLabel(
                frame,
                text="MEDICAMENTOS:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#60a5fa",
                anchor="w"
            )
            med_titulo.pack(fill="x", pady=(15, 5))
            
            for medicamento in ficha.medicamentos:
                med_label = ctk.CTkLabel(
                    frame,
                    text=f"• {medicamento}",
                    font=ctk.CTkFont(size=12),
                    text_color="#93c5fd",
                    anchor="w"
                )
                med_label.pack(fill="x", pady=2)
    
    def crear_ubicacion(self, parent, emergencia, col, row):
        """Tarjeta con ubicación GPS"""
        frame = self.crear_tarjeta(parent, "UBICACIÓN GPS EN TIEMPO REAL", col, row)
        
        # Coordenadas
        coords = ctk.CTkFrame(frame, fg_color="#1e293b", corner_radius=8)
        coords.pack(fill="x", pady=(0, 10))
        
        coord_text = ctk.CTkLabel(
            coords,
            text=f"📍 {emergencia.ubicacion.latitud}, {emergencia.ubicacion.longitud}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#22d3ee"
        )
        coord_text.pack(pady=12)
        
        # Dirección
        direccion = ctk.CTkLabel(
            frame,
            text=emergencia.ubicacion.direccion,
            font=ctk.CTkFont(size=13),
            text_color="#cbd5e1",
            wraplength=350,
            justify="left"
        )
        direccion.pack(fill="x", pady=5)
        
        # Botón de mapa
        btn_mapa = ctk.CTkButton(
            frame,
            text="ABRIR EN MAPA",
            command=lambda: self.abrir_mapa(emergencia.ubicacion),
            fg_color="#0891b2",
            hover_color="#0e7490",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        btn_mapa.pack(fill="x", pady=(15, 0))
    
    def crear_sugerencias_ia(self, parent, emergencia, col, row):
        """Tarjeta con sugerencias de IA"""
        frame = self.crear_tarjeta(parent, "SUGERENCIAS DE IA", col, row)
        
        clasificacion = SistemaIA().clasificar_emergencia(emergencia.tipo)
        
        # Recursos recomendados
        recursos_titulo = ctk.CTkLabel(
            frame,
            text="RECURSOS RECOMENDADOS:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#10b981",
            anchor="w"
        )
        recursos_titulo.pack(fill="x", pady=(0, 10))
        
        for recurso in clasificacion['recursos']:
            rec_frame = ctk.CTkFrame(frame, fg_color="#065f46", corner_radius=6)
            rec_frame.pack(fill="x", pady=3)
            
            rec_label = ctk.CTkLabel(
                rec_frame,
                text=f"✓ {recurso}",
                font=ctk.CTkFont(size=12),
                text_color="#6ee7b7"
            )
            rec_label.pack(anchor="w", pady=8, padx=12)
        
        # Preguntas clave
        preguntas_titulo = ctk.CTkLabel(
            frame,
            text="PREGUNTAS CLAVE A REALIZAR:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#60a5fa",
            anchor="w"
        )
        preguntas_titulo.pack(fill="x", pady=(20, 10))
        
        for i, pregunta in enumerate(clasificacion['preguntas'], 1):
            preg_label = ctk.CTkLabel(
                frame,
                text=f"{i}. {pregunta}",
                font=ctk.CTkFont(size=12),
                text_color="#cbd5e1",
                anchor="w",
                wraplength=400,
                justify="left"
            )
            preg_label.pack(fill="x", pady=5)
    
    def crear_protocolo(self, parent, emergencia, col, row):
        """Tarjeta con protocolo sugerido"""
        frame = self.crear_tarjeta(parent, "PROTOCOLO SUGERIDO", col, row)
        
        clasificacion = SistemaIA().clasificar_emergencia(emergencia.tipo)
        
        # Protocolo principal
        protocolo_frame = ctk.CTkFrame(frame, fg_color="#1e40af", corner_radius=8)
        protocolo_frame.pack(fill="x", pady=(0, 15))
        
        protocolo_label = ctk.CTkLabel(
            protocolo_frame,
            text=clasificacion['protocolo'],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff",
            wraplength=400
        )
        protocolo_label.pack(pady=15, padx=15)
        
        # Tiempo de respuesta
        tiempo_frame = ctk.CTkFrame(frame, fg_color="#7f1d1d", corner_radius=8)
        tiempo_frame.pack(fill="x")
        
        tiempo_label = ctk.CTkLabel(
            tiempo_frame,
            text=f"⏱ TIEMPO DE RESPUESTA OBJETIVO: {clasificacion['tiempo']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#fca5a5"
        )
        tiempo_label.pack(pady=12)
        
        # Nota de IA
        nota = ctk.CTkLabel(
            frame,
            text="La IA ha analizado el caso y sugiere seguir este protocolo. El operador tiene la decisión final.",
            font=ctk.CTkFont(size=11),
            text_color="#64748b",
            wraplength=400,
            justify="center"
        )
        nota.pack(pady=(15, 0))
    
    def crear_acciones(self, parent, emergencia, col, row):
        """Tarjeta con botones de acción"""
        frame = self.crear_tarjeta(parent, "ACCIONES", col, row)
        
        # Botón confirmar y despachar
        btn_despachar = ctk.CTkButton(
            frame,
            text="CONFIRMAR Y DESPACHAR RECURSOS",
            command=lambda: self.despachar_recursos(emergencia),
            fg_color="#16a34a",
            hover_color="#15803d",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        btn_despachar.pack(fill="x", pady=(0, 10))
        
        # Botón solicitar más info
        btn_info = ctk.CTkButton(
            frame,
            text="SOLICITAR MÁS INFORMACIÓN",
            command=lambda: self.solicitar_info(emergencia),
            fg_color="#0891b2",
            hover_color="#0e7490",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        btn_info.pack(fill="x", pady=(0, 10))
        
        # Botón falsa alarma
        btn_falsa = ctk.CTkButton(
            frame,
            text="MARCAR COMO FALSA ALARMA",
            command=lambda: self.falsa_alarma(emergencia),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        btn_falsa.pack(fill="x")
        
        # Notas del operador
        notas_titulo = ctk.CTkLabel(
            frame,
            text="NOTAS DEL OPERADOR:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        notas_titulo.pack(fill="x", pady=(20, 5))
        
        self.textbox_notas = ctk.CTkTextbox(
            frame,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.textbox_notas.pack(fill="x")
    
    def crear_tarjeta(self, parent, titulo, col, row):
        """Crea una tarjeta estándar"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        frame = ctk.CTkFrame(container, fg_color="#0f172a", corner_radius=10)
        frame.pack(fill="both", expand=True)
        
        # Título
        titulo_label = ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#60a5fa"
        )
        titulo_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Separador
        separador = ctk.CTkFrame(frame, height=2, fg_color="#1e293b")
        separador.pack(fill="x", padx=20, pady=(0, 15))
        
        # Contenido
        contenido = ctk.CTkFrame(frame, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return contenido
    
    def despachar_recursos(self, emergencia):
        """Despacha recursos de emergencia"""
        clasificacion = SistemaIA().clasificar_emergencia(emergencia.tipo)
        recursos = ", ".join(clasificacion['recursos'])
        
        mensaje = f"""RECURSOS DESPACHADOS:
        
{recursos}

Emergencia: {emergencia.id}
Usuario: {emergencia.usuario.nombre}
Ubicación: {emergencia.ubicacion.direccion}
Protocolo: {clasificacion['protocolo']}

Tiempo estimado de llegada: {clasificacion['tiempo']}"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmación de Despacho")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color="#16a34a")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame,
            text="✓ RECURSOS DESPACHADOS CON ÉXITO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        titulo.pack(pady=20)
        
        texto = ctk.CTkTextbox(
            frame,
            font=ctk.CTkFont(size=13),
            fg_color="#166534",
            text_color="#ffffff"
        )
        texto.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        texto.insert("1.0", mensaje)
        texto.configure(state="disabled")
        
        btn_cerrar = ctk.CTkButton(
            frame,
            text="CERRAR",
            command=dialog.destroy,
            fg_color="#15803d",
            hover_color="#14532d",
            height=40
        )
        btn_cerrar.pack(pady=(0, 20))
    
    def solicitar_info(self, emergencia):
        """Solicita más información"""
        dialog = ctk.CTkInputDialog(
            text="¿Qué información adicional necesita?",
            title="Solicitar Información"
        )
        respuesta = dialog.get_input()
        if respuesta:
            print(f"Información solicitada: {respuesta}")
    
    def falsa_alarma(self, emergencia):
        """Marca como falsa alarma"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar Falsa Alarma")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame,
            text="¿Confirmar como falsa alarma?",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=20)
        
        texto = ctk.CTkLabel(
            frame,
            text=f"Se marcará la emergencia {emergencia.id}\ncomo falsa alarma y se cerrará el caso.",
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8"
        )
        texto.pack(pady=10)
        
        botones = ctk.CTkFrame(frame, fg_color="transparent")
        botones.pack(pady=20)
        
        btn_confirmar = ctk.CTkButton(
            botones,
            text="CONFIRMAR",
            command=lambda: [dialog.destroy(), print(f"Emergencia {emergencia.id} marcada como falsa alarma")],
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=120
        )
        btn_confirmar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            botones,
            text="CANCELAR",
            command=dialog.destroy,
            fg_color="#475569",
            hover_color="#334155",
            width=120
        )
        btn_cancelar.pack(side="left", padx=5)
    
    def abrir_mapa(self, ubicacion):
        """Abre la ubicación en el mapa"""
        print(f"Abriendo mapa en: {ubicacion.latitud}, {ubicacion.longitud}")
    
    def simular_emergencia_entrante(self):
        """Simula emergencias entrantes para demostración"""
        def agregar_emergencia():
            time.sleep(2)
            emergencia_demo = Emergencia(
                id="EMG-2024-001",
                usuario=Usuario(
                    nombre="María González Hernández",
                    edad=45,
                    telefono="+52 618 234 5678",
                    ficha_medica=FichaMedica(
                        tipo_sangre="O+",
                        alergias=["Penicilina", "Mariscos", "Polen"],
                        medicamentos=[
                            "Metformina 850mg",
                            "Losartán 50mg",
                            "Aspirina 100mg"
                        ],
                        condiciones=[
                            "Diabetes tipo 2",
                            "Hipertensión arterial"
                        ]
                    )
                ),
                ubicacion=Ubicacion(
                    latitud=24.0277,
                    longitud=-104.6532,
                    direccion="Av. Francisco Villa 1234, Zona Centro, Victoria de Durango, Durango, México"
                ),
                tipo="medica",
                prioridad="CRÍTICA",
                timestamp=datetime.now().isoformat(),
                estado="activa"
            )
            
            self.after(0, lambda: self.agregar_emergencia_lista(emergencia_demo))
            self.after(100, lambda: self.mostrar_emergencia(emergencia_demo))
        
        thread = threading.Thread(target=agregar_emergencia, daemon=True)
        thread.start()

if __name__ == "__main__":
    app = Copiloto911()
    app.mainloop()