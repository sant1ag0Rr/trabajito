# Pruebas de Sobrecarga y Estrés - Planificación de Horarios

## 📋 Descripción

Este proyecto implementa **pruebas de sobrecarga y estrés** específicas para dos algoritmos de planificación de horarios:

1. **Algoritmo Divide y Vencerás**
## Pruebas de Sobrecarga y Estrés - Planificación de Horarios

### Descripción (actualizada)

Este repositorio contiene implementaciones y pruebas de sobrecarga para dos enfoques de planificación de horarios:

- `divide_venceras.py` — Implementación basada en dividir y vencerás (versión recursiva).
- `algoritmo_voraz.py` — Implementación voraz; actualmente se mantiene únicamente la variante **Greedy adaptativo** (las variantes "básico" y "mejorado" fueron removidas para simplificar las comparaciones).

El objetivo es comparar comportamiento práctico, consumo de recursos y calidad de soluciones entre el enfoque voraz adaptativo y la versión de divide y vencerás.

### Objetivos de las pruebas

- Medir rendimiento (tiempo y memoria) con distintos tamaños de entrada.
- Identificar cuellos de botella y puntos de inflexión en escalabilidad.
- Comparar la calidad de asignaciones (número de clases asignadas) entre los algoritmos.

### Estructura del proyecto

```
trabajito/
├── divide_venceras.py
├── algoritmo_voraz.py
├── comparacion_algoritmos.py    # (opcional)
├── README_SOBRECARGA.md
└── requirements.txt
```

### Cómo ejecutar

Instala dependencias:

```powershell
pip install -r requirements.txt
```

Ejecuta cada script por separado:

```powershell
python divide_venceras.py
python algoritmo_voraz.py
python comparacion_algoritmos.py  # si existe
```

`algoritmo_voraz.py` ejecuta ahora solo la variante Greedy adaptativo para facilitar comparaciones reproducibles.

### Métricas evaluadas

- Tiempo de ejecución (s)
- Uso de memoria (MB)
- Clases asignadas (calidad)
- Eficiencia (clases/s)

Adicional (DV): llamadas recursivas, niveles máximos y divisiones.

### Visualizaciones

- Divide y Vencerás: `sobrecarga_divide_venceras.png`, `analisis_logaritmico_dv.png`
- Greedy adaptativo: `sobrecarga_algoritmo_voraz.png`, `analisis_detallado_greedy.png`
- Comparación (si se genera): `comparacion_sobrecarga_algoritmos.png`

### Resumen comparativo

- Greedy adaptativo (recomendado para uso práctico): adapta criterios según la entrada, buen balance entre velocidad y calidad, bajo overhead.
- Divide y Vencerás (útil como alternativa): puede mostrar comportamientos interesantes, pero la implementación actual tiene mayor overhead recursivo.

Recomendación: usar Greedy adaptativo para comparaciones prácticas con `divide_venceras.py`.

### Personalización

- Cambia `tamanos_prueba` y `num_aulas` en los scripts para ajustar la carga.
- Para comparaciones reproducibles, fija `random.seed(...)` en los generadores de datos.

---

Si quieres que añada un script reproducible que ejecute ambos algoritmos sobre el mismo dataset y guarde métricas + gráficos, lo puedo crear y añadir al repositorio.
## 📊 Métricas Evaluadas

