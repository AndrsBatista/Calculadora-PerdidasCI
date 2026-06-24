Calculadora de Pérdidas        C+I

¿Qué es?
Herramienta web desarrollada en Django para el análisis automatizado de pérdidas energéticas en sistemas fotovoltaicos comerciales e industriales (C+I). Procesa archivos de datos exportados desde dataloggers y cuantifica los intervalos de tiempo en los que el sistema generó menos energía de la esperada, expresando las diferencias en kWh.

Desarrollada por Andrés Batista como herramienta interna de análisis operativo.

Funcionalidades actuales

- Carga de archivos CSV, con soporte para múltiples archivos (máximo 31)
- Detección automática de la fecha desde el contenido del archivo
- Detección automática de unidad de potencia (W o kW)
- Algoritmo de dos pasadas para identificar lapsos de pérdida basado en la eficiencia promedio del día
- Filtrado automático de ruido de arranque y cierre del día
- Resultados ordenados cronológicamente por fecha
- Resumen consolidado de pérdidas con botón de copia directa al portapapeles
- Cards colapsables por archivo para navegación limpia con múltiples días
- Contador de días con y sin pérdidas
- Exportación a Excel
- Modal de instructivo de uso integrado