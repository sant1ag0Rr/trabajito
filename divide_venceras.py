import time
import random
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import psutil
import os

class DiaSemana(Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"

@dataclass
class Clase:
    id: int
    nombre: str
    profesor: str
    duracion: int  # en horas
    horario_preferido: Tuple[DiaSemana, int]  # (día, hora_inicio)
    aula_requerida: str
    estudiantes: int

@dataclass
class Aula:
    id: str
    capacidad: int
    equipamiento: List[str]

@dataclass
class HorarioAsignado:
    clase: Clase
    dia: DiaSemana
    hora_inicio: int
    hora_fin: int
    aula: Aula

class PlanificadorDivideVenceras:
    
    def __init__(self, aulas: List[Aula]):
        self.aulas = aulas
        self.horarios_asignados: List[HorarioAsignado] = []
        self.estadisticas_recursion = {
            'llamadas_recursivas': 0,
            'niveles_maximos': 0,
            'divisiones_realizadas': 0
        }
    
    def _verificar_conflicto(self, clase: Clase, dia: DiaSemana, 
                           hora_inicio: int, aula: Aula) -> bool:
        hora_fin = hora_inicio + clase.duracion
        
        for horario in self.horarios_asignados:
            if (horario.aula.id == aula.id and 
                horario.dia == dia and
                not (hora_fin <= horario.hora_inicio or hora_inicio >= horario.hora_fin)):
                return True
            
            if (horario.clase.profesor == clase.profesor and
                horario.dia == dia and
                not (hora_fin <= horario.hora_inicio or hora_inicio >= horario.hora_fin)):
                return True
        
        return False
    
    def _asignar_horario(self, clase: Clase, dia: DiaSemana, 
                        hora_inicio: int, aula: Aula) -> bool:
        if self._verificar_conflicto(clase, dia, hora_inicio, aula):
            return False
        
        horario = HorarioAsignado(
            clase=clase,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_inicio + clase.duracion,
            aula=aula
        )
        
        self.horarios_asignados.append(horario)
        return True

    def divide_venceras(self, clases: List[Clase], nivel_recursion: int = 0) -> List[HorarioAsignado]:    
        self.estadisticas_recursion['llamadas_recursivas'] += 1
        self.estadisticas_recursion['niveles_maximos'] = max(
            self.estadisticas_recursion['niveles_maximos'], nivel_recursion
        )
        
        if not clases:
            return []
        
        if len(clases) == 1:
            clase = clases[0]
            for dia in DiaSemana:
                for hora in range(8, 18 - clase.duracion + 1):
                    for aula in self.aulas:
                        if (aula.capacidad >= clase.estudiantes and 
                            self._asignar_horario(clase, dia, hora, aula)):
                            return [self.horarios_asignados[-1]]
            return []
        
        clases_ordenadas = sorted(clases, key=lambda c: c.duracion, reverse=True)
        mitad = len(clases_ordenadas) // 2
        
        clases_largas = clases_ordenadas[:mitad]
        clases_cortas = clases_ordenadas[mitad:]
        
        self.estadisticas_recursion['divisiones_realizadas'] += 1
        
        resultado_largas = self._divide_venceras_recursivo(clases_largas, nivel_recursion + 1)
        resultado_cortas = self._divide_venceras_recursivo(clases_cortas, nivel_recursion + 1)
        
        return resultado_largas + resultado_cortas
    
    def _divide_venceras_recursivo(self, clases: List[Clase], nivel_recursion: int) -> List[HorarioAsignado]:
        self.estadisticas_recursion['llamadas_recursivas'] += 1
        self.estadisticas_recursion['niveles_maximos'] = max(
            self.estadisticas_recursion['niveles_maximos'], nivel_recursion
        )
        
        if not clases:
            return []
        
        if len(clases) == 1:
            clase = clases[0]
            for dia in DiaSemana:
                for hora in range(8, 18 - clase.duracion + 1):
                    for aula in self.aulas:
                        if (aula.capacidad >= clase.estudiantes and 
                            self._asignar_horario(clase, dia, hora, aula)):
                            return [self.horarios_asignados[-1]]
            return []
        
        mitad = len(clases) // 2
        primera_mitad = clases[:mitad]
        segunda_mitad = clases[mitad:]
        
        self.estadisticas_recursion['divisiones_realizadas'] += 1
        
        resultado1 = self._divide_venceras_recursivo(primera_mitad, nivel_recursion + 1)
        resultado2 = self._divide_venceras_recursivo(segunda_mitad, nivel_recursion + 1)
        
        return resultado1 + resultado2

    def limpiar_horarios(self):
        self.horarios_asignados = []
        self.estadisticas_recursion = {
            'llamadas_recursivas': 0,
            'niveles_maximos': 0,
            'divisiones_realizadas': 0
        }

    def estadisticas(self) -> Dict:
        if not self.horarios_asignados:
            return {
                "clases_asignadas": 0,
                "utilizacion_aulas": {},
                "estadisticas_recursion": self.estadisticas_recursion
            }
        
        clases_asignadas = len(self.horarios_asignados)
        total_horas = sum(h.hora_fin - h.hora_inicio for h in self.horarios_asignados)
        utilizacion_aulas = {}
        
        for aula in self.aulas:
            horas_aula = sum(h.hora_fin - h.hora_inicio 
                           for h in self.horarios_asignados 
                           if h.aula.id == aula.id)
            utilizacion_aulas[aula.id] = horas_aula
        
        return {
            "clases_asignadas": clases_asignadas,
            "total_horas": total_horas,
            "utilizacion_aulas": utilizacion_aulas,
            "estadisticas_recursion": self.estadisticas_recursion
        }

def generar_datos_prueba_dv(num_clases: int, num_aulas: int = 5) -> Tuple[List[Clase], List[Aula]]:
    
    aulas = []
    for i in range(num_aulas):
        aula = Aula(
            id=f"Aula_DV_{i+1}",
            capacidad=random.randint(20, 100),
            equipamiento=random.sample(["Proyector", "Pizarra", "Computadoras", "Laboratorio"], 
                                     random.randint(1, 3))
        )
        aulas.append(aula)
    
    nombres_clases = [
        "Matemáticas I", "Física I", "Química I", "Programación I", "Algoritmos",
        "Estructuras de Datos", "Bases de Datos", "Redes", "Sistemas Operativos",
        "Inteligencia Artificial", "Machine Learning", "Cálculo I", "Cálculo II",
        "Estadística", "Probabilidad", "Álgebra Lineal", "Geometría", "Trigonometría",
        "Análisis Numérico", "Teoría de Grafos", "Compiladores", "Arquitectura",
        "Ingeniería de Software", "Seguridad", "Criptografía", "Bioinformática"
    ]
    
    profesores = [
        "Dr. García", "Dra. López", "Dr. Martínez", "Dra. Rodríguez", "Dr. González",
        "Dra. Pérez", "Dr. Sánchez", "Dra. Ramírez", "Dr. Torres", "Dra. Flores",
        "Dr. Morales", "Dra. Jiménez", "Dr. Ruiz", "Dra. Díaz", "Dr. Herrera"
    ]
    
    clases = []
    for i in range(num_clases):
        duracion = random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1])[0]
        
        clase = Clase(
            id=i+1,
            nombre=random.choice(nombres_clases),
            profesor=random.choice(profesores),
            duracion=duracion,
            horario_preferido=(random.choice(list(DiaSemana)), random.randint(8, 15)),
            aula_requerida=random.choice(["Normal", "Laboratorio", "Computación"]),
            estudiantes=random.randint(15, 80)
        )
        clases.append(clase)
    
    return clases, aulas

def medir_rendimiento_dv(func, *args, **kwargs):
    proceso = psutil.Process(os.getpid())
    
    memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB
    
    # Tiempo de ejecución
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    
    # Memoria final
    memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
    
    return resultado, fin - inicio, memoria_final - memoria_inicial

def pruebas_sobrecarga_divide_venceras():
    
    print("="*70)
    print("PRUEBAS DE SOBRECARGA - ALGORITMO DIVIDE Y VENCERÁS")
    print("="*70)
    
    tamanos_prueba = [10, 25, 50, 100, 200, 300, 500, 750, 1000]
    num_aulas = 8  
    
    resultados = {
        'tamanos': [],
        'tiempos': [],
        'memoria': [],
        'clases_asignadas': [],
        'llamadas_recursivas': [],
        'niveles_maximos': [],
        'divisiones_realizadas': [],
        'eficiencia': []
    }
    
    print(f"Configuración de pruebas:")
    print(f"- Tamaños: {tamanos_prueba}")
    print(f"- Aulas disponibles: {num_aulas}")
    print(f"- Horarios: 8:00-18:00, lunes a viernes")
    print()
    
    for tamano in tamanos_prueba:
        print(f"Probando con {tamano} clases...")
        
        try:
            clases, aulas = generar_datos_prueba_dv(tamano, num_aulas)
            
            planificador = PlanificadorDivideVenceras(aulas)
            
            resultado, tiempo, memoria = medir_rendimiento_dv(
                planificador.divide_venceras, clases
            )
            
            stats = planificador.estadisticas()
            
            resultados['tamanos'].append(tamano)
            resultados['tiempos'].append(tiempo)
            resultados['memoria'].append(memoria)
            resultados['clases_asignadas'].append(stats['clases_asignadas'])
            resultados['llamadas_recursivas'].append(stats['estadisticas_recursion']['llamadas_recursivas'])
            resultados['niveles_maximos'].append(stats['estadisticas_recursion']['niveles_maximos'])
            resultados['divisiones_realizadas'].append(stats['estadisticas_recursion']['divisiones_realizadas'])
            
            eficiencia = stats['clases_asignadas'] / tiempo if tiempo > 0 else 0
            resultados['eficiencia'].append(eficiencia)
            
            print(f"  ✅ Tiempo: {tiempo:.4f}s")
            print(f"  📊 Memoria: {memoria:.2f} MB")
            print(f"  🎯 Clases asignadas: {stats['clases_asignadas']}/{tamano} ({stats['clases_asignadas']/tamano*100:.1f}%)")
            print(f"  🔄 Llamadas recursivas: {stats['estadisticas_recursion']['llamadas_recursivas']}")
            print(f"  📈 Niveles máximos: {stats['estadisticas_recursion']['niveles_maximos']}")
            print(f"  ✂️  Divisiones: {stats['estadisticas_recursion']['divisiones_realizadas']}")
            print(f"  ⚡ Eficiencia: {eficiencia:.2f} clases/s")
            print()
            
        except Exception as e:
            print(f"   Error con {tamano} clases: {e}")
            continue
    
    return resultados

def analisis_cuellos_botella_dv(resultados):
    """Analiza los cuellos de botella en el algoritmo divide y vencerás"""
    
    print("="*70)
    print("ANÁLISIS DE CUELLOS DE BOTELLA - DIVIDE Y VENCERÁS")
    print("="*70)
    
    if not resultados['tamanos']:
        print("No hay datos suficientes para el análisis")
        return
    
    print("1. ESCALABILIDAD TEMPORAL:")
    for i in range(1, len(resultados['tamanos'])):
        tamano_anterior = resultados['tamanos'][i-1]
        tamano_actual = resultados['tamanos'][i]
        tiempo_anterior = resultados['tiempos'][i-1]
        tiempo_actual = resultados['tiempos'][i]
        
        if tiempo_anterior > 0:
            factor_tiempo = tiempo_actual / tiempo_anterior
            factor_tamano = tamano_actual / tamano_anterior
            print(f"   {tamano_anterior} → {tamano_actual} clases: "
                  f"tiempo {factor_tiempo:.2f}x, tamaño {factor_tamano:.2f}x")
    
    print("\n2. USO DE MEMORIA:")
    memoria_maxima = max(resultados['memoria'])
    indice_maxima = resultados['memoria'].index(memoria_maxima)
    print(f"   Memoria máxima: {memoria_maxima:.2f} MB con {resultados['tamanos'][indice_maxima]} clases")
    
    print("\n3. COMPORTAMIENTO RECURSIVO:")
    llamadas_maximas = max(resultados['llamadas_recursivas'])
    indice_maximas = resultados['llamadas_recursivas'].index(llamadas_maximas)
    print(f"   Llamadas recursivas máximas: {llamadas_maximas} con {resultados['tamanos'][indice_maximas]} clases")
    
    niveles_maximos = max(resultados['niveles_maximos'])
    indice_niveles = resultados['niveles_maximos'].index(niveles_maximos)
    print(f"   Niveles de recursión máximos: {niveles_maximos} con {resultados['tamanos'][indice_niveles]} clases")
    
    print("\n4. EFICIENCIA:")
    eficiencia_maxima = max(resultados['eficiencia'])
    indice_eficiencia = resultados['eficiencia'].index(eficiencia_maxima)
    print(f"   Eficiencia máxima: {eficiencia_maxima:.2f} clases/s con {resultados['tamanos'][indice_eficiencia]} clases")
    
    print("\n5. CUELLOS DE BOTELLA IDENTIFICADOS:")
    
    if len(resultados['tiempos']) > 2:
        crecimiento_tiempo = []
        for i in range(1, len(resultados['tiempos'])):
            if resultados['tiempos'][i-1] > 0:
                crecimiento = resultados['tiempos'][i] / resultados['tiempos'][i-1]
                crecimiento_tiempo.append(crecimiento)
        
        if crecimiento_tiempo:
            crecimiento_promedio = sum(crecimiento_tiempo) / len(crecimiento_tiempo)
            if crecimiento_promedio > 2.0:
                print(f"     CRECIMIENTO TEMPORAL: El tiempo crece {crecimiento_promedio:.2f}x por duplicación de datos")
    
    if len(resultados['memoria']) > 2:
        crecimiento_memoria = []
        for i in range(1, len(resultados['memoria'])):
            if resultados['memoria'][i-1] > 0:
                crecimiento = resultados['memoria'][i] / resultados['memoria'][i-1]
                crecimiento_memoria.append(crecimiento)
        
        if crecimiento_memoria:
            crecimiento_promedio = sum(crecimiento_memoria) / len(crecimiento_memoria)
            if crecimiento_promedio > 1.5:
                print(f"     CRECIMIENTO DE MEMORIA: La memoria crece {crecimiento_promedio:.2f}x por duplicación de datos")
    
    if len(resultados['llamadas_recursivas']) > 2:
        crecimiento_recursion = []
        for i in range(1, len(resultados['llamadas_recursivas'])):
            if resultados['llamadas_recursivas'][i-1] > 0:
                crecimiento = resultados['llamadas_recursivas'][i] / resultados['llamadas_recursivas'][i-1]
                crecimiento_recursion.append(crecimiento)
        
        if crecimiento_recursion:
            crecimiento_promedio = sum(crecimiento_recursion) / len(crecimiento_recursion)
            if crecimiento_promedio > 2.5:
                print(f"     CRECIMIENTO DE RECURSIÓN: Las llamadas recursivas crecen {crecimiento_promedio:.2f}x por duplicación de datos")

def crear_visualizaciones_dv(resultados):
    """Crea visualizaciones específicas para el algoritmo divide y vencerás"""
    
    if not resultados['tamanos']:
        print("No hay datos para visualizar")
        return
    
    print("Generando visualizaciones para Divide y Vencerás...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis de Sobrecarga - Algoritmo Divide y Vencerás', fontsize=16, fontweight='bold')
    
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos'], 'b-o', linewidth=2, markersize=6)
    axes[0, 0].set_xlabel('Número de Clases')
    axes[0, 0].set_ylabel('Tiempo de Ejecución (segundos)')
    axes[0, 0].set_title('Escalabilidad Temporal')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria'], 'r-s', linewidth=2, markersize=6)
    axes[0, 1].set_xlabel('Número de Clases')
    axes[0, 1].set_ylabel('Uso de Memoria (MB)')
    axes[0, 1].set_title('Consumo de Memoria')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas'], 'g-^', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['tamanos'], 'k--', alpha=0.5, label='Máximo teórico')
    axes[0, 2].set_xlabel('Número de Clases')
    axes[0, 2].set_ylabel('Clases Asignadas')
    axes[0, 2].set_title('Eficiencia en Asignación')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    axes[1, 0].plot(resultados['tamanos'], resultados['llamadas_recursivas'], 'm-d', linewidth=2, markersize=6)
    axes[1, 0].set_xlabel('Número de Clases')
    axes[1, 0].set_ylabel('Llamadas Recursivas')
    axes[1, 0].set_title('Comportamiento Recursivo')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(resultados['tamanos'], resultados['niveles_maximos'], 'c-p', linewidth=2, markersize=6)
    axes[1, 1].set_xlabel('Número de Clases')
    axes[1, 1].set_ylabel('Niveles Máximos de Recursión')
    axes[1, 1].set_title('Profundidad de Recursión')
    axes[1, 1].grid(True, alpha=0.3)
    
    axes[1, 2].plot(resultados['tamanos'], resultados['eficiencia'], 'orange', marker='o', linewidth=2, markersize=6)
    axes[1, 2].set_xlabel('Número de Clases')
    axes[1, 2].set_ylabel('Eficiencia (clases/segundo)')
    axes[1, 2].set_title('Ratio de Eficiencia')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sobrecarga_divide_venceras.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.loglog(resultados['tamanos'], resultados['tiempos'], 'b-o', label='Tiempo real')
    tiempos_teoricos = [t * (n/resultados['tamanos'][0])**2 for n, t in zip(resultados['tamanos'], resultados['tiempos'])]
    plt.loglog(resultados['tamanos'], tiempos_teoricos, 'r--', alpha=0.7, label='O(n²) teórico')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Tiempo (log)')
    plt.title('Análisis Logarítmico - Tiempo')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.loglog(resultados['tamanos'], resultados['llamadas_recursivas'], 'g-s', label='Llamadas reales')
    llamadas_teoricas = [l * (n/resultados['tamanos'][0]) * np.log2(n/resultados['tamanos'][0]) for n, l in zip(resultados['tamanos'], resultados['llamadas_recursivas'])]
    plt.loglog(resultados['tamanos'], llamadas_teoricas, 'r--', alpha=0.7, label='O(n log n) teórico')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Llamadas Recursivas (log)')
    plt.title('Análisis Logarítmico - Recursión')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.semilogx(resultados['tamanos'], resultados['eficiencia'], 'm-^', linewidth=2, markersize=6)
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Eficiencia (clases/segundo)')
    plt.title('Eficiencia vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    plt.semilogx(resultados['tamanos'], resultados['memoria'], 'c-p', linewidth=2, markersize=6)
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Memoria (MB)')
    plt.title('Memoria vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analisis_logaritmico_dv.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Función principal para ejecutar las pruebas de sobrecarga"""
    
    print("ALGORITMO DIVIDE Y VENCERÁS - PRUEBAS DE SOBRECARGA")
    print("="*70)
    print("Objetivos:")
    print("1. Medir eficiencia con volúmenes grandes de entrada")
    print("2. Verificar escalabilidad con aumento gradual de carga")
    print("3. Identificar cuellos de botella en procesamiento recursivo")
    print()
    
    resultados = pruebas_sobrecarga_divide_venceras()
    
    analisis_cuellos_botella_dv(resultados)
    
    crear_visualizaciones_dv(resultados)
    
    print("="*70)
    print("PRUEBAS DE SOBRECARGA COMPLETADAS")
    print("="*70)
    print("Archivos generados:")
    print("- sobrecarga_divide_venceras.png")
    print("- analisis_logaritmico_dv.png")
    print()
if __name__ == "__main__":
    main()

