import base64
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .services.perdidas_engine import procesar_archivos, generar_excel


def _sort_key(fecha_str):
    try:
        return datetime.strptime(fecha_str, '%d/%m/%Y')
    except (ValueError, TypeError):
        return datetime.min


def upload_view(request):
    if request.method == 'POST':
        archivos = request.FILES.getlist('archivos_csv')
        nombre_planta = request.POST.get('nombre_planta', '').strip()

        if not nombre_planta:
            return render(request, 'calculadora/upload.html', {
                'error': 'Por favor, ingresa el nombre de la planta.'
            })

        if not archivos:
            return render(request, 'calculadora/upload.html', {
                'error': 'No se recibió ningún archivo.'
            })
        
        if len(archivos) > 31:
            return render(request, 'calculadora/upload.html', {
                'error': 'Se han subido más de 31 archivos. Por favor, suba un máximo de 31.'
            })

        resultado = procesar_archivos(archivos)

        # Ordenar resultados por fecha extraída del nombre de archivo
        resultados_ordenados = sorted(resultado['resultados'], key=lambda r: _sort_key(r['fecha']))

        # Regenerar Excel con registros en el mismo orden
        registros_ordenados = sorted(resultado['registros_excel'], key=lambda r: _sort_key(r['fecha']))
        excel_bytes_ordenado = generar_excel(registros_ordenados, nombre_planta) if registros_ordenados else None

        if excel_bytes_ordenado:
            request.session['excel_b64'] = base64.b64encode(excel_bytes_ordenado).decode('utf-8')
            request.session['nombre_planta'] = nombre_planta
        else:
            request.session.pop('excel_b64', None)
            request.session.pop('nombre_planta', None)

        dias_con_perdidas = sum(1 for r in resultados_ordenados if not r['sin_perdidas'])
        dias_sin_perdidas = sum(1 for r in resultados_ordenados if r['sin_perdidas'])
        
        return render(request, 'calculadora/resultados.html', {
            'resultados':         resultados_ordenados,
            'perdida_global':     resultado['perdida_global'],
            'archivos_omitidos':  resultado['archivos_omitidos'],
            'archivos_con_error': resultado['archivos_con_error'],
            'hay_excel':          excel_bytes_ordenado is not None,
            'dias_con_perdidas':  dias_con_perdidas,
            'dias_sin_perdidas':  dias_sin_perdidas,
            'nombre_planta':      nombre_planta
        })
        
    return render(request, 'calculadora/upload.html')


def descargar_excel(request):
    excel_b64     = request.session.get('excel_b64')
    nombre_planta = request.session.get('nombre_planta', 'Reporte')

    if not excel_b64:
        return HttpResponse('No hay Excel disponible. Procesa los archivos primero.', status=404)

    excel_bytes = base64.b64decode(excel_b64)
    response = HttpResponse(
        excel_bytes,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    nombre_archivo = f"Reporte_Perdidas_{nombre_planta.replace(' ', '_')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response