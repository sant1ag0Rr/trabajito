"""
Script principal para ejecutar todas las pruebas de sobrecarga
Divide y Vencerás vs Algoritmo Voraz
"""

import sys
import os
import time

def mostrar_menu():
    """Muestra el menú principal de pruebas de sobrecarga"""
    print("\n" + "="*80)
    print("PRUEBAS DE SOBRECARGA Y ESTRÉS")
    print("Planificación de Horarios: Divide y Vencerás vs Algoritmo Voraz")
    print("="*80)
    print("\nOpciones disponibles:")
    print("1. Ejecutar pruebas de Divide y Vencerás")
    print("2. Ejecutar pruebas de Algoritmo Voraz")
    print("3. Ejecutar comparación directa entre algoritmos")
    print("4. Ejecutar todas las pruebas (completo)")
    print("5. Mostrar información sobre las pruebas")
    print("6. Salir")
    print("\n" + "="*80)

def mostrar_informacion():
    """Muestra información detallada sobre las pruebas"""
    print("\n" + "="*80)
    print("INFORMACIÓN SOBRE LAS PRUEBAS DE SOBRECARGA")
    print("="*80)
    
    print("""
    🎯 OBJETIVOS DE LAS PRUEBAS DE SOBRECARGA:
    
    1. Medir la eficiencia del algoritmo con volúmenes grandes de entrada
       - Evaluar rendimiento con 10, 25, 50, 100, 200, 300, 500, 750, 1000+ clases
       - Analizar comportamiento con diferentes configuraciones de aulas
    
    2. Verificar cómo escala el rendimiento con el aumento gradual de la carga
       - Identificar patrones de crecimiento temporal y espacial
       - Determinar puntos de inflexión en el rendimiento
    
    3. Identificar cuellos de botella en el procesamiento
       - Analizar uso de memoria y CPU
       - Detectar limitaciones específicas de cada algoritmo
       - Evaluar eficiencia de estructuras de datos utilizadas
    
    📊 MÉTRICAS EVALUADAS:
    
    Métricas Generales:
    - Tiempo de ejecución (segundos)
    - Uso de memoria (MB)
    - Clases asignadas (eficiencia)
    - Eficiencia (clases por segundo)
    
    Métricas Específicas de Divide y Vencerás:
    - Llamadas recursivas
    - Niveles máximos de recursión
    - Divisiones realizadas
    - Comportamiento recursivo
    
    Métricas Específicas de Algoritmo Voraz:
    - Iteraciones del algoritmo
    - Asignaciones exitosas/fallidas
    - Mejoras locales
    - Criterios aplicados
    
    📈 VISUALIZACIONES GENERADAS:
    
    Para Divide y Vencerás:
    - sobrecarga_divide_venceras.png
    - analisis_logaritmico_dv.png
    
    Para Algoritmo Voraz:
    - sobrecarga_algoritmo_voraz.png
    - analisis_detallado_greedy.png
    
    Para Comparación:
    - comparacion_sobrecarga_algoritmos.png
    - analisis_equilibrio_algoritmos.png
    
    ⏱️  TIEMPO ESTIMADO DE EJECUCIÓN:
    - Pruebas individuales: 5-10 minutos
    - Comparación completa: 10-15 minutos
    - Todas las pruebas: 20-30 minutos
    
    💾 RECURSOS NECESARIOS:
    - Memoria: 200-500 MB durante las pruebas
    - Espacio en disco: 50-100 MB para gráficas
    - CPU: Uso intensivo durante las pruebas
    """)

def ejecutar_divide_venceras():
    """Ejecuta las pruebas de Divide y Vencerás"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DE DIVIDE Y VENCERÁS")
    print("="*60)
    print("Esto puede tomar 5-10 minutos...")
    print()
    
    try:
        from divide_venceras import main as dv_main
        dv_main()
        print("\n✅ Pruebas de Divide y Vencerás completadas exitosamente!")
        
    except ImportError as e:
        print(f"❌ Error al importar módulo de Divide y Vencerás: {e}")
        print("Asegúrate de que el archivo divide_venceras.py esté presente")
    except Exception as e:
        print(f"❌ Error durante las pruebas de Divide y Vencerás: {e}")

def ejecutar_algoritmo_voraz():
    """Ejecuta las pruebas de Algoritmo Voraz"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DE ALGORITMO VORAZ")
    print("="*60)
    print("Esto puede tomar 5-10 minutos...")
    print()
    
    try:
        from algoritmo_voraz import main as greedy_main
        greedy_main()
        print("\n✅ Pruebas de Algoritmo Voraz completadas exitosamente!")
        
    except ImportError as e:
        print(f"❌ Error al importar módulo de Algoritmo Voraz: {e}")
        print("Asegúrate de que el archivo algoritmo_voraz.py esté presente")
    except Exception as e:
        print(f"❌ Error durante las pruebas de Algoritmo Voraz: {e}")

def ejecutar_comparacion():
    """Ejecuta la comparación directa entre algoritmos"""
    print("\n" + "="*60)
    print("EJECUTANDO COMPARACIÓN DIRECTA ENTRE ALGORITMOS")
    print("="*60)
    print("Esto puede tomar 10-15 minutos...")
    print()
    
    try:
        from comparacion_algoritmos import main as comp_main
        comp_main()
        print("\n✅ Comparación entre algoritmos completada exitosamente!")
        
    except ImportError as e:
        print(f"❌ Error al importar módulo de comparación: {e}")
        print("Asegúrate de que el archivo comparacion_algoritmos.py esté presente")
    except Exception as e:
        print(f"❌ Error durante la comparación: {e}")

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas de sobrecarga"""
    print("\n" + "="*60)
    print("EJECUTANDO TODAS LAS PRUEBAS DE SOBRECARGA")
    print("="*60)
    print("Esto puede tomar 20-30 minutos...")
    print("Se ejecutarán en el siguiente orden:")
    print("1. Pruebas de Divide y Vencerás")
    print("2. Pruebas de Algoritmo Voraz")
    print("3. Comparación directa entre algoritmos")
    print()
    
    inicio_total = time.time()
    
    # Ejecutar Divide y Vencerás
    print("🔄 FASE 1: Pruebas de Divide y Vencerás")
    ejecutar_divide_venceras()
    
    # Ejecutar Algoritmo Voraz
    print("\n🔄 FASE 2: Pruebas de Algoritmo Voraz")
    ejecutar_algoritmo_voraz()
    
    # Ejecutar Comparación
    print("\n🔄 FASE 3: Comparación directa entre algoritmos")
    ejecutar_comparacion()
    
    fin_total = time.time()
    tiempo_total = fin_total - inicio_total
    
    print("\n" + "="*60)
    print("TODAS LAS PRUEBAS COMPLETADAS")
    print("="*60)
    print(f"⏱️  Tiempo total de ejecución: {tiempo_total/60:.1f} minutos")
    print("\n📊 Archivos generados:")
    print("- sobrecarga_divide_venceras.png")
    print("- analisis_logaritmico_dv.png")
    print("- sobrecarga_algoritmo_voraz.png")
    print("- analisis_detallado_greedy.png")
    print("- comparacion_sobrecarga_algoritmos.png")
    print("- analisis_equilibrio_algoritmos.png")
    print("\n✅ Todas las pruebas de sobrecarga han sido ejecutadas exitosamente!")

def verificar_dependencias():
    """Verifica que todas las dependencias estén disponibles"""
    print("Verificando dependencias...")
    
    dependencias = [
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
        ('psutil', 'psutil')
    ]
    
    faltantes = []
    for nombre, modulo in dependencias:
        try:
            __import__(modulo)
            print(f"✅ {nombre} - OK")
        except ImportError:
            print(f"❌ {nombre} - FALTANTE")
            faltantes.append(nombre)
    
    if faltantes:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(faltantes)}")
        print("Instala las dependencias faltantes con:")
        print("pip install " + " ".join(faltantes))
        return False
    
    print("\n✅ Todas las dependencias están disponibles")
    return True

def main():
    """Función principal"""
    
    print("PRUEBAS DE SOBRECARGA Y ESTRÉS")
    print("Planificación de Horarios: Divide y Vencerás vs Algoritmo Voraz")
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ No se pueden ejecutar las pruebas sin las dependencias necesarias")
        return
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                ejecutar_divide_venceras()
                
            elif opcion == "2":
                ejecutar_algoritmo_voraz()
                
            elif opcion == "3":
                ejecutar_comparacion()
                
            elif opcion == "4":
                ejecutar_todas_las_pruebas()
                
            elif opcion == "5":
                mostrar_informacion()
                
            elif opcion == "6":
                print("\n¡Gracias por usar el sistema de pruebas de sobrecarga!")
                print("Trabajo completado exitosamente.")
                break
                
            else:
                print("❌ Opción inválida. Por favor, selecciona una opción del 1 al 6.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("Por favor, intenta nuevamente.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)

