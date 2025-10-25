# Pruebas de Sobrecarga y Estrés - Planificación de Horarios

## 📋 Descripción

Este proyecto implementa **pruebas de sobrecarga y estrés** específicas para dos algoritmos de planificación de horarios:

1. **Algoritmo Divide y Vencerás**
2. **Algoritmo Voraz (Greedy)**

Cada algoritmo se encuentra en archivos separados con sus propias pruebas de sobrecarga, permitiendo un análisis detallado y específico de cada enfoque.

## 🎯 Objetivos de las Pruebas de Sobrecarga

### Definición
Las **pruebas de sobrecarga** están orientadas a determinar cómo se comporta un algoritmo cuando se le somete a una carga cercana a su límite máximo de rendimiento sin que el sistema colapse.

### Objetivos Específicos:

1. **Medir la eficiencia del algoritmo con volúmenes grandes de entrada**
   - Evaluar el rendimiento con 10, 25, 50, 100, 200, 300, 500, 750, 1000+ clases
   - Analizar el comportamiento con diferentes configuraciones de aulas

2. **Verificar cómo escala el rendimiento con el aumento gradual de la carga**
   - Identificar patrones de crecimiento temporal y espacial
   - Determinar puntos de inflexión en el rendimiento

3. **Identificar cuellos de botella en el procesamiento**
   - Analizar el uso de memoria y CPU
   - Detectar limitaciones específicas de cada algoritmo
   - Evaluar la eficiencia de las estructuras de datos utilizadas

## 📁 Estructura del Proyecto

```
trabajito/
├── divide_venceras.py           # Algoritmo Divide y Vencerás + Pruebas de Sobrecarga
├── algoritmo_voraz.py           # Algoritmo Voraz + Pruebas de Sobrecarga
├── comparacion_algoritmos.py    # Comparación directa entre ambos algoritmos
├── README_SOBRECARGA.md         # Este archivo
└── requirements.txt             # Dependencias
```

## 🚀 Cómo Ejecutar las Pruebas

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución Individual

#### 1. Pruebas de Divide y Vencerás
```bash
python divide_venceras.py
```

**Características específicas:**
- Análisis de recursión (llamadas recursivas, niveles máximos)
- Medición de divisiones realizadas
- Análisis de complejidad espacial por recursión
- Visualizaciones específicas del comportamiento recursivo

#### 2. Pruebas de Algoritmo Voraz
```bash
python algoritmo_voraz.py
```

**Características específicas:**
- Análisis de iteraciones y asignaciones
- Comparación entre Greedy básico, mejorado y adaptativo
- Medición de mejoras locales
- Análisis de criterios de selección

#### 3. Comparación Directa
```bash
python comparacion_algoritmos.py
```

**Características específicas:**
- Comparación lado a lado de ambos algoritmos
- Análisis de puntos de equilibrio
- Identificación de ventajas específicas de cada enfoque
- Visualizaciones comparativas

## 📊 Métricas Evaluadas

### Métricas Generales
- **Tiempo de ejecución** (segundos)
- **Uso de memoria** (MB)
- **Clases asignadas** (eficiencia)
- **Eficiencia** (clases por segundo)

### Métricas Específicas de Divide y Vencerás
- **Llamadas recursivas**: Número total de llamadas recursivas
- **Niveles máximos**: Profundidad máxima de recursión
- **Divisiones realizadas**: Número de divisiones del problema
- **Comportamiento recursivo**: Análisis de la estructura de recursión

### Métricas Específicas de Algoritmo Voraz
- **Iteraciones**: Número de iteraciones del algoritmo
- **Asignaciones exitosas/fallidas**: Éxito en la asignación de horarios
- **Mejoras locales**: Optimizaciones realizadas por búsqueda local
- **Criterios aplicados**: Número de criterios de selección utilizados

## 📈 Visualizaciones Generadas

### Para Divide y Vencerás
- `sobrecarga_divide_venceras.png`: Análisis completo de sobrecarga
- `analisis_logaritmico_dv.png`: Análisis logarítmico de complejidad

### Para Algoritmo Voraz
- `sobrecarga_algoritmo_voraz.png`: Análisis completo de sobrecarga
- `analisis_detallado_greedy.png`: Análisis detallado de comportamiento

### Para Comparación
- `comparacion_sobrecarga_algoritmos.png`: Comparación directa
- `analisis_equilibrio_algoritmos.png`: Análisis de puntos de equilibrio

## 🔍 Análisis de Cuellos de Botella

### Identificación Automática
Los scripts identifican automáticamente:

1. **Cuellos de botella temporales**
   - Crecimiento exponencial del tiempo de ejecución
   - Puntos de inflexión en la escalabilidad

2. **Cuellos de botella de memoria**
   - Uso excesivo de memoria
   - Crecimiento no lineal del consumo

3. **Cuellos de botella específicos del algoritmo**
   - **DV**: Recursión excesiva, divisiones ineficientes
   - **Greedy**: Iteraciones excesivas, criterios ineficientes

### Alertas Generadas
- ⚠️ **CRECIMIENTO TEMPORAL**: Cuando el tiempo crece más de 2x por duplicación
- ⚠️ **CRECIMIENTO DE MEMORIA**: Cuando la memoria crece más de 1.5x por duplicación
- ⚠️ **CRECIMIENTO DE RECURSIÓN**: Cuando las llamadas recursivas crecen más de 2.5x por duplicación

## 📊 Resultados Esperados

### Comportamiento de Divide y Vencerás
- **Complejidad temporal**: O(n² × m × h) en el peor caso
- **Complejidad espacial**: O(n) por recursión
- **Ventaja**: Solución más robusta y completa
- **Desventaja**: Mayor uso de memoria por recursión

### Comportamiento de Algoritmo Voraz
- **Complejidad temporal**: O(n² × m × h) en el peor caso
- **Complejidad espacial**: O(n) lineal
- **Ventaja**: Más rápido para problemas pequeños
- **Desventaja**: Puede quedar atrapado en óptimos locales

### Puntos de Equilibrio
- **Problemas pequeños** (n < 50): Greedy es más rápido
- **Problemas medianos** (50 ≤ n ≤ 200): DV es más eficiente
- **Problemas grandes** (n > 200): Greedy Mejorado ofrece el mejor balance

## 🛠️ Configuración de Pruebas

### Tamaños de Prueba
```python
tamanos_prueba = [10, 25, 50, 100, 200, 300, 500, 750, 1000, 1500]
```

### Configuración de Aulas
- **Número de aulas**: 8 (configurable)
- **Capacidades**: 20-100 estudiantes (aleatorio)
- **Equipamiento**: Variable (Proyector, Pizarra, Computadoras, Laboratorio)

### Configuración de Clases
- **Duración**: 1-4 horas (distribución específica por algoritmo)
- **Estudiantes**: 15-80 (distribución específica por algoritmo)
- **Profesores**: 15-20 profesores diferentes
- **Horarios**: 8:00-18:00, lunes a viernes

## 📋 Interpretación de Resultados

### Análisis de Escalabilidad
1. **Crecimiento lineal**: O(n) - Ideal
2. **Crecimiento logarítmico**: O(n log n) - Muy bueno
3. **Crecimiento cuadrático**: O(n²) - Aceptable para problemas pequeños
4. **Crecimiento exponencial**: O(2ⁿ) - Problemático

### Análisis de Eficiencia
- **Eficiencia alta**: > 100 clases/segundo
- **Eficiencia media**: 10-100 clases/segundo
- **Eficiencia baja**: < 10 clases/segundo

### Análisis de Memoria
- **Uso bajo**: < 50 MB
- **Uso medio**: 50-200 MB
- **Uso alto**: > 200 MB

## 🔧 Personalización de Pruebas

### Modificar Tamaños de Prueba
```python
# En cada archivo, modificar la variable tamanos_prueba
tamanos_prueba = [10, 50, 100, 500, 1000, 2000]  # Personalizar según necesidades
```

### Modificar Configuración de Aulas
```python
# Modificar el número de aulas y sus características
num_aulas = 10  # Aumentar para problemas más complejos
```

### Modificar Criterios de Alerta
```python
# En las funciones de análisis, modificar los umbrales
if crecimiento_promedio > 2.0:  # Cambiar umbral según necesidades
    print("⚠️ CRECIMIENTO TEMPORAL EXCESIVO")
```

## 📚 Conceptos Teóricos Aplicados

### Análisis de Complejidad
- **Big O**: Cota superior asintótica
- **Theta (Θ)**: Cota ajustada
- **Omega (Ω)**: Cota inferior asintótica

### Pruebas de Sobrecarga
- **Escalabilidad**: Comportamiento con aumento de datos
- **Robustez**: Comportamiento en condiciones límite
- **Eficiencia**: Relación entre recursos utilizados y resultados obtenidos

### Análisis Empírico
- **Medición de rendimiento**: Tiempo y espacio reales
- **Análisis de tendencias**: Patrones de crecimiento
- **Identificación de cuellos de botella**: Limitaciones específicas

## 🎯 Conclusiones Esperadas

### Para Divide y Vencerás
- Comportamiento O(n²) en la práctica
- Recursión crece logarítmicamente
- Uso de memoria lineal con el número de clases
- Eficiencia estable hasta problemas de tamaño medio

### Para Algoritmo Voraz
- Más rápido para problemas pequeños
- Greedy mejorado ofrece mejor calidad con costo moderado
- Greedy adaptativo se ajusta dinámicamente
- Eficiencia se mantiene estable hasta problemas medianos-grandes

### Comparación General
- DV es más eficiente para problemas medianos y grandes
- Greedy es más rápido para problemas pequeños
- Greedy Mejorado ofrece el mejor balance general
- El punto de equilibrio está alrededor de 100-200 clases

---

**Estas pruebas de sobrecarga proporcionan una evaluación exhaustiva del rendimiento de ambos algoritmos bajo condiciones de estrés, permitiendo tomar decisiones informadas sobre cuál algoritmo usar en diferentes contextos.**

