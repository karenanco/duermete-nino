from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SerFolclorico, Pais, Arquetipo


def home_view(request):
    """Renderiza la interfaz principal: el planeta Tierra interactivo con fondo oscuro."""
    context = {
        'titulo': 'Duérmete Niño - Mapa interactivo del folclore infantil mundial'
    }
    return render(request, 'duermete_nino/home.html', context)


def arquetipos_lista_view(request):
    """Muestra un desglose educativo e histórico de los grandes arquetipos."""
    arquetipos = Arquetipo.objects.all()
    return render(request, 'duermete_nino/arquetipos.html', {'arquetipos': arquetipos})


def acerca_de_view(request):
    """Página informativa sobre el proyecto, metodología y objetivos académicos."""
    return render(request, 'duermete_nino/acerca_de.html')


# API endpoints (JSON)

def api_lista_seres(request):
    """Devuelve la lista simplificada de todos los seres para posicionamiento o búsqueda inicial."""
    seres = SerFolclorico.objects.select_related('pais', 'arquetipo').all()
    data = [{
        'id': s.id,
        'nombre': s.nombre,
        'pais': s.pais.nombre,
        'codigo_iso': s.pais.codigo_iso,
        'continente': s.pais.get_continente_display(),
        'arquetipo': s.arquetipo.nombre if s.arquetipo else "Desconocido",
        'descripcion_breve': s.descripcion_breve
    } for s in seres]
    return JsonResponse({'seres': data})


def api_seres_por_pais(request, codigo_iso):
    """Devuelve los seres mitológicos de un país al hacer clic en el mapa."""
    pais = get_object_or_404(Pais, codigo_iso__iexact=codigo_iso)
    seres = SerFolclorico.objects.filter(pais=pais).select_related('arquetipo')

    data = {
        'pais': pais.nombre,
        'continente': pais.get_continente_display(),
        'seres': [{
            'id': s.id,
            'nombre': s.nombre,
            'arquetipo': s.arquetipo.nombre if s.arquetipo else "N/A",
            'descripcion_breve': s.descripcion_breve,
            'descripcion_detallada': s.descripcion_detallada
        } for s in seres]
    }
    return JsonResponse(data)


def api_detalle_ser(request, ser_id):
    """Devuelve la ficha completa y detallada de un ser folclórico específico."""
    ser = get_object_or_404(SerFolclorico, id=ser_id)
    data = {
        'id': ser.id,
        'nombre': ser.nombre,
        'pais': ser.pais.nombre,
        'arquetipo': ser.arquetipo.nombre if ser.arquetipo else None,
        'descripcion_breve': ser.descripcion_breve,
        'descripcion_detallada': ser.descripcion_detallada,
    }
    return JsonResponse(data)
