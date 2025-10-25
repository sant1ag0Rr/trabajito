
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
    duracion: int
    horario_preferido: Tuple[DiaSemana, int]
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

class PlanificadorVoraz:
    
    def __init__(self, aulas: List[Aula]):
        self.aulas = aulas
        self.horarios_asignados: List[HorarioAsignado] = []
        self.estadisticas_greedy = {
            'iteraciones': 0,
            'asignaciones_exitosas': 0,
            'asignaciones_fallidas': 0,
            'criterios_aplicados': 0,
            'mejoras_locales': 0
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
            self.estadisticas_greedy['asignaciones_fallidas'] += 1
            return False
        
        horario = HorarioAsignado(
            clase=clase,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_inicio + clase.duracion,
            aula=aula
        )
        
        self.horarios_asignados.append(horario)
        self.estadisticas_greedy['asignaciones_exitosas'] += 1
        return True

    def greedy_adaptativo(self, clases: List[Clase]) -> List[HorarioAsignado]:
        duraciones = [c.duracion for c in clases]
        estudiantes = [c.estudiantes for c in clases]
        
        if max(duraciones) - min(duraciones) > 2:
            criterio = lambda c: (c.duracion, -c.estudiantes)
        elif max(estudiantes) - min(estudiantes) > 30:
            criterio = lambda c: (c.estudiantes, -c.duracion)
        else:
            criterio = lambda c: (c.duracion * c.estudiantes, -c.duracion)
        
        clases_ordenadas = sorted(clases, key=criterio, reverse=True)
        
        horarios_asignados = []
        
        for clase in clases_ordenadas:
            self.estadisticas_greedy['iteraciones'] += 1
            asignada = False
            
            for dia in DiaSemana:
                if asignada:
                    break
                    
                for hora in range(8, 18 - clase.duracion + 1):
                    if asignada:
                        break
                    
                    aulas_ordenadas = sorted(self.aulas, 
                                           key=lambda a: abs(a.capacidad - clase.estudiantes))
                    
                    for aula in aulas_ordenadas:
                        if (aula.capacidad >= clase.estudiantes and 
                            not self._verificar_conflicto(clase, dia, hora, aula)):
                            
                            horario = HorarioAsignado(
                                clase=clase,
                                dia=dia,
                                hora_inicio=hora,
                                hora_fin=hora + clase.duracion,
                                aula=aula
                            )
                            
                            horarios_asignados.append(horario)
                            self.horarios_asignados.append(horario)
                            asignada = True
                            break
        
        return horarios_asignados

    def limpiar_horarios(self):
        self.horarios_asignados = []
        self.estadisticas_greedy = {
            'iteraciones': 0,
            'asignaciones_exitosas': 0,
            'asignaciones_fallidas': 0,
            'criterios_aplicados': 0,
            'mejoras_locales': 0
        }

    def estadisticas(self) -> Dict:
        if not self.horarios_asignados:
            return {
                "clases_asignadas": 0,
                "utilizacion_aulas": {},
                "estadisticas_greedy": self.estadisticas_greedy
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
            "estadisticas_greedy": self.estadisticas_greedy
        }

def generar_datos_prueba_greedy(num_clases: int, num_aulas: int = 5) -> Tuple[List[Clase], List[Aula]]:
    aulas = []
    for i in range(num_aulas):
        aula = Aula(
            id=f"Aula_G_{i+1}",
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
        "Ingeniería de Software", "Seguridad", "Criptografía", "Bioinformática",
        "Robótica", "Visión por Computador", "Procesamiento de Señales", "Optimización"
    ]
    
    profesores = [
        "Dr. García", "Dra. López", "Dr. Martínez", "Dra. Rodríguez", "Dr. González",
        "Dra. Pérez", "Dr. Sánchez", "Dra. Ramírez", "Dr. Torres", "Dra. Flores",
        "Dr. Morales", "Dra. Jiménez", "Dr. Ruiz", "Dra. Díaz", "Dr. Herrera",
        "Dr. Vargas", "Dra. Castro", "Dr. Romero", "Dra. Aguilar", "Dr. Mendoza"
    ]
    
    clases = []
    for i in range(num_clases):
        duracion = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        
        estudiantes = random.choices(
            [15, 25, 35, 45, 55, 65, 75], 
            weights=[0.1, 0.2, 0.25, 0.2, 0.15, 0.08, 0.02]
        )[0]
        
        clase = Clase(
            id=i+1,
            nombre=random.choice(nombres_clases),
            profesor=random.choice(profesores),
            duracion=duracion,
            horario_preferido=(random.choice(list(DiaSemana)), random.randint(8, 15)),
            aula_requerida=random.choice(["Normal", "Laboratorio", "Computación"]),
            estudiantes=estudiantes
        )
        clases.append(clase)
    
    return clases, aulas

def medir_rendimiento_greedy(func, *args, **kwargs):
    proceso = psutil.Process(os.getpid())
    memoria_inicial = proceso.memory_info().rss / 1024 / 1024
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    
    memoria_final = proceso.memory_info().rss / 1024 / 1024
    
    return resultado, fin - inicio, memoria_final - memoria_inicial

def pruebas_sobrecarga_greedy():
    
    print("="*70)
    print("PRUEBAS DE SOBRECARGA - ALGORITMO VORAZ (GREEDY)")
    print("="*70)
    
    tamanos_prueba = [10, 25, 50, 100, 200, 300, 500, 750, 1000, 1500]
    num_aulas = 8
    
    resultados = {
        'tamanos': [],
        'tiempos_greedy_adaptativo': [],
        'memoria_greedy_adaptativo': [],
        'clases_asignadas_greedy_adaptativo': [],
        'iteraciones': [],
        'asignaciones_exitosas': [],
        'asignaciones_fallidas': [],
        'mejoras_locales': [],
        'eficiencia_greedy_adaptativo': []
    }
    
    print(f"Configuración de pruebas:")
    print(f"- Tamaños: {tamanos_prueba}")
    print(f"- Aulas disponibles: {num_aulas}")
    print(f"- Horarios: 8:00-18:00, lunes a viernes")
    print(f"- Algoritmo: Greedy Adaptativo")
    print()
    
    for tamano in tamanos_prueba:
        print(f"Probando con {tamano} clases...")
        
        try:
            clases, aulas = generar_datos_prueba_greedy(tamano, num_aulas)
            
            planificador = PlanificadorVoraz(aulas)
            
            resultado_greedy_adaptativo, tiempo_greedy_adaptativo, memoria_greedy_adaptativo = medir_rendimiento_greedy(
                planificador.greedy_adaptativo, clases
            )
            stats_greedy_adaptativo = planificador.estadisticas()
            
            resultados['tamanos'].append(tamano)
            resultados['tiempos_greedy_adaptativo'].append(tiempo_greedy_adaptativo)
            resultados['memoria_greedy_adaptativo'].append(memoria_greedy_adaptativo)
            resultados['clases_asignadas_greedy_adaptativo'].append(stats_greedy_adaptativo['clases_asignadas'])
            resultados['iteraciones'].append(stats_greedy_adaptativo['estadisticas_greedy']['iteraciones'])
            resultados['asignaciones_exitosas'].append(stats_greedy_adaptativo['estadisticas_greedy']['asignaciones_exitosas'])
            resultados['asignaciones_fallidas'].append(stats_greedy_adaptativo['estadisticas_greedy']['asignaciones_fallidas'])
            resultados['mejoras_locales'].append(0)  # No hay mejoras locales en el adaptativo
            
            eficiencia_greedy_adaptativo = stats_greedy_adaptativo['clases_asignadas'] / tiempo_greedy_adaptativo if tiempo_greedy_adaptativo > 0 else 0
            resultados['eficiencia_greedy_adaptativo'].append(eficiencia_greedy_adaptativo)
            
            print(f"  🎯 GREEDY ADAPTATIVO:")
            print(f"     Tiempo: {tiempo_greedy_adaptativo:.4f}s, Memoria: {memoria_greedy_adaptativo:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy_adaptativo['clases_asignadas']}/{tamano} ({stats_greedy_adaptativo['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Iteraciones: {stats_greedy_adaptativo['estadisticas_greedy']['iteraciones']}")
            print(f"     Eficiencia: {eficiencia_greedy_adaptativo:.2f} clases/s")
            print()
            
        except Exception as e:
            print(f"  ❌ Error con {tamano} clases: {e}")
            continue
    
    return resultados

def analisis_cuellos_botella_greedy(resultados):
    
    print("="*70)
    print("ANÁLISIS DE CUELLOS DE BOTELLA - ALGORITMO VORAZ")
    print("="*70)
    
    if not resultados['tamanos']:
        print("No hay datos suficientes para el análisis")
        return
    
    print("1. ESCALABILIDAD TEMPORAL:")
    tiempos = resultados['tiempos_greedy_adaptativo']
    for j in range(1, len(tiempos)):
        if tiempos[j-1] > 0:
            factor_tiempo = tiempos[j] / tiempos[j-1]
            factor_tamano = resultados['tamanos'][j] / resultados['tamanos'][j-1]
            print(f"     {resultados['tamanos'][j-1]} → {resultados['tamanos'][j]} clases: "
                  f"tiempo {factor_tiempo:.2f}x, tamaño {factor_tamano:.2f}x")
    
    print("\n2. USO DE MEMORIA:")
    memorias = resultados['memoria_greedy_adaptativo']
    if memorias:
        memoria_maxima = max(memorias)
        indice_maxima = memorias.index(memoria_maxima)
        print(f"   Memoria máxima: {memoria_maxima:.2f} MB con {resultados['tamanos'][indice_maxima]} clases")
    
    print("\n3. EFICIENCIA EN ASIGNACIÓN:")
    clases_asignadas = resultados['clases_asignadas_greedy_adaptativo']
    if clases_asignadas:
        eficiencia_maxima = max(clases_asignadas)
        indice_eficiencia = clases_asignadas.index(eficiencia_maxima)
        print(f"   Máxima asignación: {eficiencia_maxima} clases con {resultados['tamanos'][indice_eficiencia]} clases")
    
    print("\n4. COMPORTAMIENTO VORAZ:")
    if resultados['iteraciones']:
        iteraciones_maximas = max(resultados['iteraciones'])
        indice_maximas = resultados['iteraciones'].index(iteraciones_maximas)
        print(f"   Iteraciones máximas: {iteraciones_maximas} con {resultados['tamanos'][indice_maximas]} clases")
    
    if resultados['asignaciones_exitosas']:
        exitosas_maximas = max(resultados['asignaciones_exitosas'])
        indice_exitosas = resultados['asignaciones_exitosas'].index(exitosas_maximas)
        print(f"   Asignaciones exitosas máximas: {exitosas_maximas} con {resultados['tamanos'][indice_exitosas]} clases")
    
    if resultados['mejoras_locales']:
        mejoras_maximas = max(resultados['mejoras_locales'])
        indice_mejoras = resultados['mejoras_locales'].index(mejoras_maximas)
        print(f"   Mejoras locales máximas: {mejoras_maximas} con {resultados['tamanos'][indice_mejoras]} clases")
    
    print("\n5. CUELLOS DE BOTELLA IDENTIFICADOS:")
    tiempos = resultados['tiempos_greedy_adaptativo']
    if len(tiempos) > 2:
        crecimiento_tiempo = []
        for j in range(1, len(tiempos)):
            if tiempos[j-1] > 0:
                crecimiento = tiempos[j] / tiempos[j-1]
                crecimiento_tiempo.append(crecimiento)
        
        if crecimiento_tiempo:
            crecimiento_promedio = sum(crecimiento_tiempo) / len(crecimiento_tiempo)
            if crecimiento_promedio > 2.0:
                print(f"   ⚠️  CRECIMIENTO TEMPORAL: {crecimiento_promedio:.2f}x por duplicación")
    
    eficiencias = resultados['eficiencia_greedy_adaptativo']
    if len(eficiencias) > 2:
        eficiencia_inicial = eficiencias[0]
        eficiencia_final = eficiencias[-1]
        if eficiencia_inicial > 0:
            decrecimiento = eficiencia_final / eficiencia_inicial
            if decrecimiento < 0.5:
                print(f"   ⚠️  DECRECIMIENTO DE EFICIENCIA: {decrecimiento:.2f}x al final")

def crear_visualizaciones_greedy(resultados):
    
    if not resultados['tamanos']:
        print("No hay datos para visualizar")
        return
    
    print("Generando visualizaciones para Algoritmo Voraz...")
    
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Análisis de Sobrecarga - Algoritmo Voraz (Greedy)', fontsize=16, fontweight='bold')
    
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 0].set_xlabel('Número de Clases')
    axes[0, 0].set_ylabel('Tiempo de Ejecución (segundos)')
    axes[0, 0].set_title('Escalabilidad Temporal')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 1].set_xlabel('Número de Clases')
    axes[0, 1].set_ylabel('Uso de Memoria (MB)')
    axes[0, 1].set_title('Consumo de Memoria')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['tamanos'], 'k--', alpha=0.5, label='Máximo teórico')
    axes[0, 2].set_xlabel('Número de Clases')
    axes[0, 2].set_ylabel('Clases Asignadas')
    axes[0, 2].set_title('Eficiencia en Asignación')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[1, 0].set_xlabel('Número de Clases')
    axes[1, 0].set_ylabel('Eficiencia (clases/segundo)')
    axes[1, 0].set_title('Ratio de Eficiencia')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(resultados['tamanos'], resultados['iteraciones'], 'm-d', linewidth=2, markersize=6)
    axes[1, 1].set_xlabel('Número de Clases')
    axes[1, 1].set_ylabel('Iteraciones')
    axes[1, 1].set_title('Comportamiento Iterativo')
    axes[1, 1].grid(True, alpha=0.3)
    
    axes[1, 2].plot(resultados['tamanos'], resultados['asignaciones_exitosas'], 'g-o', label='Exitosas', linewidth=2, markersize=6)
    axes[1, 2].plot(resultados['tamanos'], resultados['asignaciones_fallidas'], 'r-s', label='Fallidas', linewidth=2, markersize=6)
    axes[1, 2].set_xlabel('Número de Clases')
    axes[1, 2].set_ylabel('Número de Asignaciones')
    axes[1, 2].set_title('Éxito vs Fallo en Asignaciones')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)
    
    axes[2, 0].plot(resultados['tamanos'], resultados['mejoras_locales'], 'c-p', linewidth=2, markersize=6)
    axes[2, 0].set_xlabel('Número de Clases')
    axes[2, 0].set_ylabel('Mejoras Locales')
    axes[2, 0].set_title('Optimización Local')
    axes[2, 0].grid(True, alpha=0.3)
    
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    axes[2, 1].set_xlabel('Número de Clases (log)')
    axes[2, 1].set_ylabel('Tiempo (log)')
    axes[2, 1].set_title('Análisis Logarítmico - Tiempo')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    
    # 9. Tendencia de eficiencia
    axes[2, 2].plot(resultados['tamanos'], resultados['eficiencia_greedy_adaptativo'], 'g-^', label='Tendencia de Eficiencia')
    axes[2, 2].set_xlabel('Número de Clases')
    axes[2, 2].set_ylabel('Eficiencia (clases/segundo)')
    axes[2, 2].set_title('Tendencia de Eficiencia')
    axes[2, 2].legend()
    axes[2, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sobrecarga_algoritmo_voraz.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfica adicional: Análisis detallado de comportamiento
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Eficiencia (clases/segundo)')
    plt.title('Eficiencia vs Tamaño (Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.semilogx(resultados['tamanos'], resultados['iteraciones'], 'm-d', linewidth=2, markersize=6)
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Iteraciones')
    plt.title('Iteraciones vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    if resultados['asignaciones_exitosas'] and resultados['asignaciones_fallidas']:
        ratio_exito = [e/(e+f) if (e+f) > 0 else 0 for e, f in zip(resultados['asignaciones_exitosas'], resultados['asignaciones_fallidas'])]
        plt.semilogx(resultados['tamanos'], ratio_exito, 'c-p', linewidth=2, markersize=6)
        plt.xlabel('Número de Clases (log)')
        plt.ylabel('Ratio de Éxito')
        plt.title('Ratio de Éxito en Asignaciones')
        plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Memoria (MB)')
    plt.title('Memoria vs Tamaño')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analisis_detallado_greedy.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    
    print("ALGORITMO VORAZ (GREEDY) - PRUEBAS DE SOBRECARGA")
    print("="*70)
    print("Objetivos:")
    print("1. Medir eficiencia con volúmenes grandes de entrada")
    print("2. Verificar escalabilidad con aumento gradual de carga")
    print("3. Identificar cuellos de botella en procesamiento voraz")
    print("4. Comparar variantes: Básico, Mejorado, Adaptativo")
    print()
    
    # Ejecutar pruebas de sobrecarga
    resultados = pruebas_sobrecarga_greedy()
    
    # Analizar cuellos de botella
    analisis_cuellos_botella_greedy(resultados)
    
    # Crear visualizaciones
    crear_visualizaciones_greedy(resultados)
    
    print("="*70)
    print("PRUEBAS DE SOBRECARGA COMPLETADAS")
    print("="*70)
    print("Archivos generados:")
    print("- sobrecarga_algoritmo_voraz.png")
    print("- analisis_detallado_greedy.png")
    print()
if __name__ == "__main__":
    main()

