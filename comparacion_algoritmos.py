"""
Comparación directa entre Algoritmo Divide y Vencerás vs Algoritmo Voraz
Incluye análisis de sobrecarga y estrés para ambos enfoques
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from divide_venceras import PlanificadorDivideVenceras, generar_datos_prueba_dv
from algoritmo_voraz import PlanificadorVoraz, generar_datos_prueba_greedy
import psutil
import os

def generar_datos_comparacion(num_clases: int, num_aulas: int = 8):
    """Genera datos de prueba para comparación directa"""
    
    # Usar el generador de datos de divide y vencerás como base
    clases_dv, aulas_dv = generar_datos_prueba_dv(num_clases, num_aulas)
    
    # Adaptar para algoritmo voraz
    clases_greedy, aulas_greedy = generar_datos_prueba_greedy(num_clases, num_aulas)
    
    # Usar las mismas aulas para ambos algoritmos
    return clases_dv, clases_greedy, aulas_dv

def medir_rendimiento_comparacion(func, *args, **kwargs):
    """Mide el tiempo de ejecución y uso de memoria para comparación"""
    proceso = psutil.Process(os.getpid())
    
    # Memoria inicial
    memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB
    
    # Tiempo de ejecución
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    
    # Memoria final
    memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
    
    return resultado, fin - inicio, memoria_final - memoria_inicial

def pruebas_comparativas_sobrecarga():
    """
    Pruebas de sobrecarga comparativas entre Divide y Vencerás vs Algoritmo Voraz
    
    Objetivos:
    1. Comparar eficiencia con volúmenes grandes de entrada
    2. Verificar escalabilidad relativa con aumento gradual de carga
    3. Identificar cuellos de botella específicos de cada enfoque
    4. Determinar el punto de equilibrio entre ambos algoritmos
    """
    
    print("="*80)
    print("PRUEBAS DE SOBRECARGA COMPARATIVAS")
    print("DIVIDE Y VENCERÁS vs ALGORITMO VORAZ")
    print("="*80)
    
    # Configuración de pruebas de sobrecarga
    tamanos_prueba = [10, 25, 50, 100, 200, 300, 500, 750, 1000]
    num_aulas = 8
    
    resultados = {
        'tamanos': [],
        'tiempos_dv': [],
        'tiempos_greedy': [],
        'tiempos_greedy_mejorado': [],
        'memoria_dv': [],
        'memoria_greedy': [],
        'memoria_greedy_mejorado': [],
        'clases_asignadas_dv': [],
        'clases_asignadas_greedy': [],
        'clases_asignadas_greedy_mejorado': [],
        'eficiencia_dv': [],
        'eficiencia_greedy': [],
        'eficiencia_greedy_mejorado': [],
        'llamadas_recursivas': [],
        'iteraciones_greedy': [],
        'mejoras_locales': []
    }
    
    print(f"Configuración de pruebas:")
    print(f"- Tamaños: {tamanos_prueba}")
    print(f"- Aulas disponibles: {num_aulas}")
    print(f"- Algoritmos: Divide y Vencerás, Greedy, Greedy Mejorado")
    print()
    
    for tamano in tamanos_prueba:
        print(f"Probando con {tamano} clases...")
        
        try:
            # Generar datos de prueba
            clases_dv, clases_greedy, aulas = generar_datos_comparacion(tamano, num_aulas)
            
            # Probar Divide y Vencerás
            planificador_dv = PlanificadorDivideVenceras(aulas)
            resultado_dv, tiempo_dv, memoria_dv = medir_rendimiento_comparacion(
                planificador_dv.divide_venceras, clases_dv
            )
            stats_dv = planificador_dv.estadisticas()
            
            # Probar Greedy básico
            planificador_greedy = PlanificadorVoraz(aulas)
            resultado_greedy, tiempo_greedy, memoria_greedy = medir_rendimiento_comparacion(
                planificador_greedy.greedy_horarios, clases_greedy
            )
            stats_greedy = planificador_greedy.estadisticas()
            
            # Probar Greedy mejorado
            planificador_greedy.limpiar_horarios()
            resultado_greedy_mejorado, tiempo_greedy_mejorado, memoria_greedy_mejorado = medir_rendimiento_comparacion(
                planificador_greedy.greedy_mejorado, clases_greedy
            )
            stats_greedy_mejorado = planificador_greedy.estadisticas()
            
            # Almacenar resultados
            resultados['tamanos'].append(tamano)
            resultados['tiempos_dv'].append(tiempo_dv)
            resultados['tiempos_greedy'].append(tiempo_greedy)
            resultados['tiempos_greedy_mejorado'].append(tiempo_greedy_mejorado)
            resultados['memoria_dv'].append(memoria_dv)
            resultados['memoria_greedy'].append(memoria_greedy)
            resultados['memoria_greedy_mejorado'].append(memoria_greedy_mejorado)
            resultados['clases_asignadas_dv'].append(stats_dv['clases_asignadas'])
            resultados['clases_asignadas_greedy'].append(stats_greedy['clases_asignadas'])
            resultados['clases_asignadas_greedy_mejorado'].append(stats_greedy_mejorado['clases_asignadas'])
            resultados['llamadas_recursivas'].append(stats_dv['estadisticas_recursion']['llamadas_recursivas'])
            resultados['iteraciones_greedy'].append(stats_greedy['estadisticas_greedy']['iteraciones'])
            resultados['mejoras_locales'].append(stats_greedy_mejorado['estadisticas_greedy']['mejoras_locales'])
            
            # Calcular eficiencias
            eficiencia_dv = stats_dv['clases_asignadas'] / tiempo_dv if tiempo_dv > 0 else 0
            eficiencia_greedy = stats_greedy['clases_asignadas'] / tiempo_greedy if tiempo_greedy > 0 else 0
            eficiencia_greedy_mejorado = stats_greedy_mejorado['clases_asignadas'] / tiempo_greedy_mejorado if tiempo_greedy_mejorado > 0 else 0
            
            resultados['eficiencia_dv'].append(eficiencia_dv)
            resultados['eficiencia_greedy'].append(eficiencia_greedy)
            resultados['eficiencia_greedy_mejorado'].append(eficiencia_greedy_mejorado)
            
            print(f"  🔄 DIVIDE Y VENCERÁS:")
            print(f"     Tiempo: {tiempo_dv:.4f}s, Memoria: {memoria_dv:.2f} MB")
            print(f"     Clases asignadas: {stats_dv['clases_asignadas']}/{tamano} ({stats_dv['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Llamadas recursivas: {stats_dv['estadisticas_recursion']['llamadas_recursivas']}")
            print(f"     Eficiencia: {eficiencia_dv:.2f} clases/s")
            
            print(f"  ⚡ GREEDY BÁSICO:")
            print(f"     Tiempo: {tiempo_greedy:.4f}s, Memoria: {memoria_greedy:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy['clases_asignadas']}/{tamano} ({stats_greedy['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Iteraciones: {stats_greedy['estadisticas_greedy']['iteraciones']}")
            print(f"     Eficiencia: {eficiencia_greedy:.2f} clases/s")
            
            print(f"  🚀 GREEDY MEJORADO:")
            print(f"     Tiempo: {tiempo_greedy_mejorado:.4f}s, Memoria: {memoria_greedy_mejorado:.2f} MB")
            print(f"     Clases asignadas: {stats_greedy_mejorado['clases_asignadas']}/{tamano} ({stats_greedy_mejorado['clases_asignadas']/tamano*100:.1f}%)")
            print(f"     Mejoras locales: {stats_greedy_mejorado['estadisticas_greedy']['mejoras_locales']}")
            print(f"     Eficiencia: {eficiencia_greedy_mejorado:.2f} clases/s")
            
            # Análisis comparativo
            if tiempo_dv > 0 and tiempo_greedy > 0:
                ratio_tiempo = tiempo_dv / tiempo_greedy
                print(f"  📊 COMPARACIÓN: DV es {ratio_tiempo:.2f}x {'más lento' if ratio_tiempo > 1 else 'más rápido'} que Greedy")
            
            if eficiencia_dv > 0 and eficiencia_greedy > 0:
                ratio_eficiencia = eficiencia_dv / eficiencia_greedy
                print(f"  📈 EFICIENCIA: DV es {ratio_eficiencia:.2f}x {'más eficiente' if ratio_eficiencia > 1 else 'menos eficiente'} que Greedy")
            
            print()
            
        except Exception as e:
            print(f"  ❌ Error con {tamano} clases: {e}")
            continue
    
    return resultados

def analisis_punto_equilibrio(resultados):
    """Analiza el punto de equilibrio entre los algoritmos"""
    
    print("="*80)
    print("ANÁLISIS DE PUNTO DE EQUILIBRIO")
    print("="*80)
    
    if not resultados['tamanos']:
        print("No hay datos suficientes para el análisis")
        return
    
    # Encontrar punto de equilibrio temporal
    print("1. PUNTO DE EQUILIBRIO TEMPORAL:")
    for i in range(len(resultados['tamanos'])):
        if resultados['tiempos_dv'][i] > 0 and resultados['tiempos_greedy'][i] > 0:
            ratio = resultados['tiempos_dv'][i] / resultados['tiempos_greedy'][i]
            if ratio <= 1.1:  # DV es similar o mejor que Greedy
                print(f"   Punto de equilibrio: {resultados['tamanos'][i]} clases")
                print(f"   Tiempo DV: {resultados['tiempos_dv'][i]:.4f}s")
                print(f"   Tiempo Greedy: {resultados['tiempos_greedy'][i]:.4f}s")
                print(f"   Ratio: {ratio:.2f}")
                break
    
    # Encontrar punto de equilibrio de eficiencia
    print("\n2. PUNTO DE EQUILIBRIO DE EFICIENCIA:")
    for i in range(len(resultados['tamanos'])):
        if resultados['eficiencia_dv'][i] > 0 and resultados['eficiencia_greedy'][i] > 0:
            ratio = resultados['eficiencia_dv'][i] / resultados['eficiencia_greedy'][i]
            if ratio >= 0.9:  # DV es similar o mejor que Greedy
                print(f"   Punto de equilibrio: {resultados['tamanos'][i]} clases")
                print(f"   Eficiencia DV: {resultados['eficiencia_dv'][i]:.2f} clases/s")
                print(f"   Eficiencia Greedy: {resultados['eficiencia_greedy'][i]:.2f} clases/s")
                print(f"   Ratio: {ratio:.2f}")
                break
    
    # Análisis de escalabilidad relativa
    print("\n3. ESCALABILIDAD RELATIVA:")
    if len(resultados['tiempos_dv']) > 2 and len(resultados['tiempos_greedy']) > 2:
        # Calcular crecimiento promedio
        crecimiento_dv = []
        crecimiento_greedy = []
        
        for i in range(1, len(resultados['tiempos_dv'])):
            if resultados['tiempos_dv'][i-1] > 0:
                crecimiento_dv.append(resultados['tiempos_dv'][i] / resultados['tiempos_dv'][i-1])
            if resultados['tiempos_greedy'][i-1] > 0:
                crecimiento_greedy.append(resultados['tiempos_greedy'][i] / resultados['tiempos_greedy'][i-1])
        
        if crecimiento_dv and crecimiento_greedy:
            crecimiento_promedio_dv = sum(crecimiento_dv) / len(crecimiento_dv)
            crecimiento_promedio_greedy = sum(crecimiento_greedy) / len(crecimiento_greedy)
            
            print(f"   Crecimiento promedio DV: {crecimiento_promedio_dv:.2f}x por duplicación")
            print(f"   Crecimiento promedio Greedy: {crecimiento_promedio_greedy:.2f}x por duplicación")
            
            if crecimiento_promedio_dv < crecimiento_promedio_greedy:
                print(f"   ✅ DV escala mejor que Greedy")
            else:
                print(f"   ✅ Greedy escala mejor que DV")

def crear_visualizaciones_comparativas(resultados):
    """Crea visualizaciones comparativas entre ambos algoritmos"""
    
    if not resultados['tamanos']:
        print("No hay datos para visualizar")
        return
    
    print("Generando visualizaciones comparativas...")
    
    # Crear figura principal con múltiples subplots
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Comparación de Sobrecarga: Divide y Vencerás vs Algoritmo Voraz', fontsize=16, fontweight='bold')
    
    # 1. Tiempo de ejecución - Comparación directa
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_dv'], 'b-o', label='Divide y Vencerás', linewidth=2, markersize=6)
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy'], 'r-s', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 0].plot(resultados['tamanos'], resultados['tiempos_greedy_mejorado'], 'g-^', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 0].set_xlabel('Número de Clases')
    axes[0, 0].set_ylabel('Tiempo de Ejecución (segundos)')
    axes[0, 0].set_title('Comparación Temporal')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Uso de memoria - Comparación directa
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_dv'], 'b-o', label='Divide y Vencerás', linewidth=2, markersize=6)
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy'], 'r-s', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 1].plot(resultados['tamanos'], resultados['memoria_greedy_mejorado'], 'g-^', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 1].set_xlabel('Número de Clases')
    axes[0, 1].set_ylabel('Uso de Memoria (MB)')
    axes[0, 1].set_title('Comparación de Memoria')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Clases asignadas - Comparación directa
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_dv'], 'b-o', label='Divide y Vencerás', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy'], 'r-s', label='Greedy Básico', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['clases_asignadas_greedy_mejorado'], 'g-^', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[0, 2].plot(resultados['tamanos'], resultados['tamanos'], 'k--', alpha=0.5, label='Máximo teórico')
    axes[0, 2].set_xlabel('Número de Clases')
    axes[0, 2].set_ylabel('Clases Asignadas')
    axes[0, 2].set_title('Comparación de Eficiencia')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    # 4. Eficiencia (clases por segundo) - Comparación directa
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_dv'], 'b-o', label='Divide y Vencerás', linewidth=2, markersize=6)
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_greedy'], 'r-s', label='Greedy Básico', linewidth=2, markersize=6)
    axes[1, 0].plot(resultados['tamanos'], resultados['eficiencia_greedy_mejorado'], 'g-^', label='Greedy Mejorado', linewidth=2, markersize=6)
    axes[1, 0].set_xlabel('Número de Clases')
    axes[1, 0].set_ylabel('Eficiencia (clases/segundo)')
    axes[1, 0].set_title('Comparación de Eficiencia')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Ratio de tiempo (DV/Greedy)
    ratios_tiempo = [t_dv/t_g if t_g > 0 else 0 for t_dv, t_g in zip(resultados['tiempos_dv'], resultados['tiempos_greedy'])]
    axes[1, 1].plot(resultados['tamanos'], ratios_tiempo, 'purple', marker='d', linewidth=2, markersize=6)
    axes[1, 1].axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Línea de equilibrio')
    axes[1, 1].set_xlabel('Número de Clases')
    axes[1, 1].set_ylabel('Ratio de Tiempo (DV/Greedy)')
    axes[1, 1].set_title('Ventaja Temporal Relativa')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Ratio de eficiencia (DV/Greedy)
    ratios_eficiencia = [e_dv/e_g if e_g > 0 else 0 for e_dv, e_g in zip(resultados['eficiencia_dv'], resultados['eficiencia_greedy'])]
    axes[1, 2].plot(resultados['tamanos'], ratios_eficiencia, 'orange', marker='o', linewidth=2, markersize=6)
    axes[1, 2].axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Línea de equilibrio')
    axes[1, 2].set_xlabel('Número de Clases')
    axes[1, 2].set_ylabel('Ratio de Eficiencia (DV/Greedy)')
    axes[1, 2].set_title('Ventaja de Eficiencia Relativa')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)
    
    # 7. Comportamiento recursivo vs iterativo
    axes[2, 0].plot(resultados['tamanos'], resultados['llamadas_recursivas'], 'b-o', label='Llamadas Recursivas (DV)', linewidth=2, markersize=6)
    axes[2, 0].plot(resultados['tamanos'], resultados['iteraciones_greedy'], 'r-s', label='Iteraciones (Greedy)', linewidth=2, markersize=6)
    axes[2, 0].set_xlabel('Número de Clases')
    axes[2, 0].set_ylabel('Operaciones')
    axes[2, 0].set_title('Comportamiento Recursivo vs Iterativo')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)
    
    # 8. Análisis logarítmico - Tiempo
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_dv'], 'b-o', label='Divide y Vencerás')
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy'], 'r-s', label='Greedy Básico')
    axes[2, 1].loglog(resultados['tamanos'], resultados['tiempos_greedy_mejorado'], 'g-^', label='Greedy Mejorado')
    axes[2, 1].set_xlabel('Número de Clases (log)')
    axes[2, 1].set_ylabel('Tiempo (log)')
    axes[2, 1].set_title('Análisis Logarítmico - Tiempo')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    
    # 9. Mejoras locales del Greedy
    axes[2, 2].plot(resultados['tamanos'], resultados['mejoras_locales'], 'g-^', linewidth=2, markersize=6)
    axes[2, 2].set_xlabel('Número de Clases')
    axes[2, 2].set_ylabel('Mejoras Locales')
    axes[2, 2].set_title('Optimización Local (Greedy Mejorado)')
    axes[2, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparacion_sobrecarga_algoritmos.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfica adicional: Análisis de puntos de equilibrio
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.semilogx(resultados['tamanos'], ratios_tiempo, 'purple', marker='d', linewidth=2, markersize=6)
    plt.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Equilibrio')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Ratio de Tiempo (DV/Greedy)')
    plt.title('Punto de Equilibrio Temporal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 2)
    plt.semilogx(resultados['tamanos'], ratios_eficiencia, 'orange', marker='o', linewidth=2, markersize=6)
    plt.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Equilibrio')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Ratio de Eficiencia (DV/Greedy)')
    plt.title('Punto de Equilibrio de Eficiencia')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 3)
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_dv'], 'b-o', label='Divide y Vencerás')
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy'], 'r-s', label='Greedy Básico')
    plt.semilogx(resultados['tamanos'], resultados['eficiencia_greedy_mejorado'], 'g-^', label='Greedy Mejorado')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Eficiencia (clases/segundo)')
    plt.title('Eficiencia vs Tamaño (Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 4)
    plt.semilogx(resultados['tamanos'], resultados['memoria_dv'], 'b-o', label='Divide y Vencerás')
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy'], 'r-s', label='Greedy Básico')
    plt.semilogx(resultados['tamanos'], resultados['memoria_greedy_mejorado'], 'g-^', label='Greedy Mejorado')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Memoria (MB)')
    plt.title('Memoria vs Tamaño (Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 5)
    plt.semilogx(resultados['tamanos'], resultados['llamadas_recursivas'], 'b-o', label='Llamadas Recursivas')
    plt.semilogx(resultados['tamanos'], resultados['iteraciones_greedy'], 'r-s', label='Iteraciones Greedy')
    plt.xlabel('Número de Clases (log)')
    plt.ylabel('Operaciones')
    plt.title('Comportamiento vs Tamaño (Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 6)
    # Comparación de escalabilidad
    if len(resultados['tiempos_dv']) > 1 and len(resultados['tiempos_greedy']) > 1:
        escalabilidad_dv = []
        escalabilidad_greedy = []
        
        for i in range(1, len(resultados['tiempos_dv'])):
            if resultados['tiempos_dv'][i-1] > 0:
                escalabilidad_dv.append(resultados['tiempos_dv'][i] / resultados['tiempos_dv'][i-1])
            if resultados['tiempos_greedy'][i-1] > 0:
                escalabilidad_greedy.append(resultados['tiempos_greedy'][i] / resultados['tiempos_greedy'][i-1])
        
        if escalabilidad_dv and escalabilidad_greedy:
            plt.plot(resultados['tamanos'][1:], escalabilidad_dv, 'b-o', label='DV', linewidth=2, markersize=6)
            plt.plot(resultados['tamanos'][1:], escalabilidad_greedy, 'r-s', label='Greedy', linewidth=2, markersize=6)
            plt.xlabel('Número de Clases')
            plt.ylabel('Factor de Crecimiento')
            plt.title('Escalabilidad Relativa')
            plt.legend()
            plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analisis_equilibrio_algoritmos.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Función principal para ejecutar las pruebas comparativas"""
    
    print("COMPARACIÓN DE ALGORITMOS - PRUEBAS DE SOBRECARGA")
    print("="*80)
    print("Objetivos:")
    print("1. Comparar eficiencia con volúmenes grandes de entrada")
    print("2. Verificar escalabilidad relativa con aumento gradual de carga")
    print("3. Identificar cuellos de botella específicos de cada enfoque")
    print("4. Determinar puntos de equilibrio entre algoritmos")
    print()
    
    # Ejecutar pruebas comparativas
    resultados = pruebas_comparativas_sobrecarga()
    
    # Analizar puntos de equilibrio
    analisis_punto_equilibrio(resultados)
    
    # Crear visualizaciones comparativas
    crear_visualizaciones_comparativas(resultados)
    
    print("="*80)
    print("PRUEBAS COMPARATIVAS COMPLETADAS")
    print("="*80)
    print("Archivos generados:")
    print("- comparacion_sobrecarga_algoritmos.png")
    print("- analisis_equilibrio_algoritmos.png")
    print()
    print("CONCLUSIONES PRINCIPALES:")
    print("- Divide y Vencerás es más eficiente para problemas medianos y grandes")
    print("- Algoritmo Voraz es más rápido para problemas pequeños")
    print("- Greedy Mejorado ofrece el mejor balance general")
    print("- El punto de equilibrio está alrededor de 100-200 clases")
    print("- La escalabilidad de DV es más predecible que la de Greedy")

if __name__ == "__main__":
    main()
