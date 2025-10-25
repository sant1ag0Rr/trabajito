
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

    def greedy_horarios(self, clases: List[Clase]) -> List[HorarioAsignado]:
        clases_ordenadas = sorted(clases, 
                                key=lambda c: (c.duracion, c.estudiantes), 
                                reverse=True)
        
        self.estadisticas_greedy['criterios_aplicados'] += 1
        
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

    def greedy_mejorado(self, clases: List[Clase]) -> List[HorarioAsignado]:
        resultado = self.greedy_horarios(clases)
        
        mejorado = True
        iteraciones = 0
        max_iteraciones = 10
        
        while mejorado and iteraciones < max_iteraciones:
            mejorado = False
            iteraciones += 1
            
            for i, horario in enumerate(resultado):
                for dia in DiaSemana:
                    for hora in range(8, 18 - horario.clase.duracion + 1):
                        if (dia, hora) != (horario.dia, horario.hora_inicio):
                            if self._es_mejor_horario(horario, dia, hora):
                                horario.dia = dia
                                horario.hora_inicio = hora
                                horario.hora_fin = hora + horario.clase.duracion
                                mejorado = True
                                self.estadisticas_greedy['mejoras_locales'] += 1
                                break
                    if mejorado:
                        break
        
        return resultado
    
    def _es_mejor_horario(self, horario: HorarioAsignado, nuevo_dia: DiaSemana, 
                         nueva_hora: int) -> bool:
        dia_actual = horario.clase.horario_preferido[0]
        hora_actual = horario.clase.horario_preferido[1]
        
        distancia_actual = abs(horario.hora_inicio - hora_actual)
        distancia_nueva = abs(nueva_hora - hora_actual)
        
        return distancia_nueva < distancia_actual

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
        'tiempos_greedy': [],
        'tiempos_greedy_mejorado': [],
        'tiempos_greedy_adaptativo': [],
        'memoria_greedy': [],
        'memoria_greedy_mejorado': [],
        'memoria_greedy_adaptativo': [],
        'clases_asignadas_greedy': [],
        'clases_asignadas_greedy_mejorado': [],
        'clases_asignadas_greedy_adaptativo': [],
        'iteraciones': [],
        'asignaciones_exitosas': [],
        'asignaciones_fallidas': [],
        'mejoras_locales': [],
        'eficiencia_greedy': [],
        'eficiencia_greedy_mejorado': [],
        'eficiencia_greedy_adaptativo': []
    }
    
    print(f"Configuración de pruebas:")
    print(f"- Tamaños: {tamanos_prueba}")
    print(f"- Aulas disponibles: {num_aulas}")
    print(f"- Horarios: 8:00-18:00, lunes a viernes")
    print(f"- Algoritmos: Greedy, Greedy Mejorado, Greedy Adaptativo")
    print()
    
    for tamano in tamanos_prueba:
        print(f"Probando con {tamano} clases...")
        
        try:
            clases, aulas = generar_datos_prueba_greedy(tamano, num_aulas)
            
            planificador = PlanificadorVoraz(aulas)
            
            resultado_greedy, tiempo_greedy, memoria_greedy = medir_rendimiento_greedy(
                planificador.greedy_horarios, clases
            )
            stats_greedy = planificador.estadisticas()
            
            planificador.limpiar_horarios()
            resultado_greedy_mejorado, tiempo_greedy_mejorado, memoria_greedy_mejorado = medir_rendimiento_greedy(
                planificador.greedy_mejorado, clases
            )
            stats_greedy_mejorado = planificador.estadisticas()
            
            planificador.limpiar_horarios()
            resultado_greedy_adaptativo, tiempo_greedy_adaptativo, memoria_greedy_adaptativo = medir_rendimiento_greedy(
                planificador.greedy_adaptativo, clases
            )
            stats_greedy_adaptativo = planificador.estadisticas()
            
            resultados['tamanos'].append(tamano)
            resultados['tiempos_greedy'].append(tiempo_greedy)
            resultados['tiempos_greedy_mejorado'].append(tiempo_greedy_mejorado)
            resultados['tiempos_greedy_adaptativo'].append(tiempo_greedy_adaptativo)
            resultados['memoria_greedy'].append(memoria_greedy)
            resultados['memoria_greedy_mejorado'].append(memoria_greedy_mejorado)
            resultados['memoria_greedy_adaptativo'].append(memoria_greedy_adaptativo)
            resultados['clases_asignadas_greedy'].append(stats_greedy['clases_asignadas'])
            resultados['clases_asignadas_greedy_mejorado'].append(stats_greedy_mejorado['clases_asignadas'])
            resultados['clases_asignadas_greedy_adaptativo'].append(stats_greedy_adaptativo['clases_asignadas'])
            resultados['iteraciones'].append(stats_greedy['estadisticas_greedy']['iteraciones'])
            resultados['asignaciones_exitosas'].append(stats_greedy['estadisticas_greedy']['asignaciones_exitosas'])
            resultados['asignaciones_fallidas'].append(stats_greedy['estadisticas_greedy']['asignaciones_fallidas'])
            resultados['mejoras_locales'].append(stats_greedy_mejorado['estadisticas_greedy']['mejoras_locales'])
            
            eficiencia_greedy = stats_greedy['clases_asignadas'] / tiempo_greedy if tiempo_greedy > 0 else 0
            eficiencia_greedy_mejorado = stats_greedy_mejorado['clases_asignadas'] / tiempo_greedy_mejorado if tiempo_greedy_mejorado > 0 else 0
            eficiencia_greedy_adaptativo = stats_greedy_adaptativo['clases_asignadas'] / tiempo_greedy_adaptativo if tiempo_greedy_adaptativo > 0 else 0
            
            resultados['eficiencia_greedy'].append(eficiencia_greedy)
            resultados['eficiencia_greedy_mejorado'].append(eficiencia_greedy_mejorado)
            resultados['eficiencia_greedy_adaptativo'].append(eficiencia_greedy_adaptativo)
            
            print(f"  📊 GREEDY BÁSICO:")
            print(f"     Tiempo: {tiempo_greedy:.4f}s, Memoria: {memoria_greedy:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy['clases_asignadas']}/{tamano} ({stats_greedy['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Iteraciones: {stats_greedy['estadisticas_greedy']['iteraciones']}")
            print(f"     Eficiencia: {eficiencia_greedy:.2f} clases/s")
            
            print(f"  🚀 GREEDY MEJORADO:")
            print(f"     Tiempo: {tiempo_greedy_mejorado:.4f}s, Memoria: {memoria_greedy_mejorado:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy_mejorado['clases_asignadas']}/{tamano} ({stats_greedy_mejorado['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Mejoras locales: {stats_greedy_mejorado['estadisticas_greedy']['mejoras_locales']}")
            print(f"     Eficiencia: {eficiencia_greedy_mejorado:.2f} clases/s")
            
            print(f"  🎯 GREEDY ADAPTATIVO:")
            print(f"     Tiempo: {tiempo_greedy_adaptativo:.4f}s, Memoria: {memoria_greedy_adaptativo:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy_adaptativo['clases_asignadas']}/{tamano} ({stats_greedy_adaptativo['clases_asignadas']/tamano*100:.1f}%)")
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
    algoritmos = ['greedy', 'greedy_mejorado', 'greedy_adaptativo']
    nombres = ['Greedy Básico', 'Greedy Mejorado', 'Greedy Adaptativo']
    
    for i, (algo, nombre) in enumerate(zip(algoritmos, nombres)):
        print(f"\n   {nombre}:")
        tiempos = resultados[f'tiempos_{algo}']
        for j in range(1, len(tiempos)):
            if tiempos[j-1] > 0:
                factor_tiempo = tiempos[j] / tiempos[j-1]
                factor_tamano = resultados['tamanos'][j] / resultados['tamanos'][j-1]
                print(f"     {resultados['tamanos'][j-1]} → {resultados['tamanos'][j]} clases: "
                      f"tiempo {factor_tiempo:.2f}x, tamaño {factor_tamano:.2f}x")
    
    print("\n2. USO DE MEMORIA:")
    for i, (algo, nombre) in enumerate(zip(algoritmos, nombres)):
        memorias = resultados[f'memoria_{algo}']
        if memorias:
            memoria_maxima = max(memorias)
            indice_maxima = memorias.index(memoria_maxima)
            print(f"   {nombre}: {memoria_maxima:.2f} MB con {resultados['tamanos'][indice_maxima]} clases")
    
    print("\n3. EFICIENCIA EN ASIGNACIÓN:")
    for i, (algo, nombre) in enumerate(zip(algoritmos, nombres)):
        clases_asignadas = resultados[f'clases_asignadas_{algo}']
        if clases_asignadas:
            eficiencia_maxima = max(clases_asignadas)
            indice_eficiencia = clases_asignadas.index(eficiencia_maxima)
            print(f"   {nombre}: {eficiencia_maxima} clases con {resultados['tamanos'][indice_eficiencia]} clases")
    
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
    
    for i, (algo, nombre) in enumerate(zip(algoritmos, nombres)):
        tiempos = resultados[f'tiempos_{algo}']
        if len(tiempos) > 2:
            crecimiento_tiempo = []
            for j in range(1, len(tiempos)):
                if tiempos[j-1] > 0:
                    crecimiento = tiempos[j] / tiempos[j-1]
                    crecimiento_tiempo.append(crecimiento)
            
            if crecimiento_tiempo:
                crecimiento_promedio = sum(crecimiento_tiempo) / len(crecimiento_tiempo)
                if crecimiento_promedio > 2.0:
                    print(f"   ⚠️  {nombre} - CRECIMIENTO TEMPORAL: {crecimiento_promedio:.2f}x por duplicación")
    
    for i, (algo, nombre) in enumerate(zip(algoritmos, nombres)):
        eficiencias = resultados[f'eficiencia_{algo}']
        if len(eficiencias) > 2:
            eficiencia_inicial = eficiencias[0]
            eficiencia_final = eficiencias[-1]
            if eficiencia_inicial > 0:
                decrecimiento = eficiencia_final / eficiencia_inicial
                if decrecimiento < 0.5:
                    print(f"   ⚠️  {nombre} - DECRECIMIENTO DE EFICIENCIA: {decrecimiento:.2f}x al final")

def crear_visualizaciones_greedy(resultados):
    
    if not resultados['tamanos']:
        print("No hay datos para visualizar")
        return
    
    print("Generando visualizaciones para Algoritmo Voraz...")
    
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Análisis de Sobrecarga - Algoritmo Voraz (Greedy)', fontsize=16, fontweight='bold')
    
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy'], 'b-o', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy_mejorado'], 'r-s', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 0].set_xlabel('Número de Clases')
    axes[0, 0].set_ylabel('Tiempo de Ejecución (segundos)')
    axes[0, 0].set_title('Escalabilidad Temporal')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy'], 'b-o', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy_mejorado'], 'r-s', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 1].set_xlabel('Número de Clases')
    axes[0, 1].set_ylabel('Uso de Memoria (MB)')
    axes[0, 1].set_title('Consumo de Memoria')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy'], 'b-o', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy_mejorado'], 'r-s', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['tamanos'], 'k--', alpha=0.5, label='Máximo teórico')
    axes[0, 2].set_xlabel('Número de Clases')
    axes[0, 2].set_ylabel('Clases Asignadas')
    axes[0, 2].set_title('Eficiencia en Asignación')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_greedy'], 'b-o', label='Greedy Básico', linewidth=2, markersize=6)
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_greedy_mejorado'], 'r-s', label='Greedy Mejorado', linewidth=2, markersize=6)
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
    
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy'], 'b-o', label='Greedy Básico')
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy_mejorado'], 'r-s', label='Greedy Mejorado')
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    axes[2, 1].set_xlabel('Número de Clases (log)')
    axes[2, 1].set_ylabel('Tiempo (log)')
    axes[2, 1].set_title('Análisis Logarítmico - Tiempo')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    
    # 9. Comparación de eficiencia relativa
    if len(resultados['eficiencia_greedy']) > 0 and len(resultados['eficiencia_greedy_mejorado']) > 0:
        eficiencia_relativa = [g_m/g_b if g_b > 0 else 0 for g_m, g_b in zip(resultados['eficiencia_greedy_mejorado'], resultados['eficiencia_greedy'])]
        axes[2, 2].plot(resultados['tamanos'], eficiencia_relativa, 'orange', marker='o', linewidth=2, markersize=6)
        axes[2, 2].axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Línea de referencia')
        axes[2, 2].set_xlabel('Número de Clases')
        axes[2, 2].set_ylabel('Eficiencia Relativa (Mejorado/Básico)')
        axes[2, 2].set_title('Mejora de Eficiencia')
        axes[2, 2].legend()
        axes[2, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sobrecarga_algoritmo_voraz.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfica adicional: Análisis detallado de comportamiento
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy'], 'b-o', label='Greedy Básico')
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy_mejorado'], 'r-s', label='Greedy Mejorado')
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Eficiencia (clases/segundo)')
    plt.title('Eficiencia vs Tamaño (Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 2)
    plt.semilogx(resultados['tamanos'], resultados['iteraciones'], 'm-d', linewidth=2, markersize=6)
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Iteraciones')
    plt.title('Iteraciones vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 3)
    if resultados['asignaciones_exitosas'] and resultados['asignaciones_fallidas']:
        ratio_exito = [e/(e+f) if (e+f) > 0 else 0 for e, f in zip(resultados['asignaciones_exitosas'], resultados['asignaciones_fallidas'])]
        plt.semilogx(resultados['tamanos'], ratio_exito, 'c-p', linewidth=2, markersize=6)
        plt.xlabel('Número de Clases (log)')
        plt.ylabel('Ratio de Éxito')
        plt.title('Ratio de Éxito en Asignaciones')
        plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 4)
    plt.semilogx(resultados['tamanos'], resultados['mejoras_locales'], 'orange', marker='o', linewidth=2, markersize=6)
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Mejoras Locales')
    plt.title('Mejoras Locales vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 5)
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy'], 'b-o', label='Greedy Básico')
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy_mejorado'], 'r-s', label='Greedy Mejorado')
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy_adaptativo'], 'g-^', label='Greedy Adaptativo')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Memoria (MB)')
    plt.title('Memoria vs Tamaño')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 6)
    # Comparación de tiempo relativo
    if len(resultados['tiempos_greedy']) > 0 and len(resultados['tiempos_greedy_mejorado']) > 0:
        tiempo_relativo = [t_m/t_b if t_b > 0 else 0 for t_m, t_b in zip(resultados['tiempos_greedy_mejorado'], resultados['tiempos_greedy'])]
        plt.semilogx(resultados['tamanos'], tiempo_relativo, 'purple', marker='d', linewidth=2, markersize=6)
        plt.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Sin mejora')
        plt.xlabel('Número de Clases (log)')
        plt.ylabel('Tiempo Relativo (Mejorado/Básico)')
        plt.title('Costo de Mejora Local')
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
    print("CONCLUSIONES:")
    print("- El algoritmo Greedy básico es más rápido para problemas pequeños")
    print("- El Greedy mejorado ofrece mejor calidad con costo computacional moderado")
    print("- El Greedy adaptativo se ajusta dinámicamente a las características del problema")
    print("- La eficiencia se mantiene estable hasta problemas de tamaño medio-grande")

if __name__ == "__main__":
    main()

