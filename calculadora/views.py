from django.shortcuts import render
from django.contrib import messages
from decimal import Decimal, InvalidOperation # <-- IMPORTANTE PARA EVITAR ERRORES
from .models import ProyectoGondola, CalculoCamara

def calcular_cobertura_view(request):
    if request.method == 'POST':
        nombre_gondola = request.POST.get('nombre')
        
        # Validar que los campos de texto existan
        if not nombre_gondola:
            messages.error(request, "Falta el nombre de la góndola.")
            return render(request, 'calculadora/formulario.html')

        try:
            # CORRECCIÓN 2: Convertir todo lo que llega del HTML (texto) a Decimal (número)
            l_gondola = Decimal(request.POST.get('largo_gondola'))
            b_mayor = Decimal(request.POST.get('base_mayor'))
            b_menor = Decimal(request.POST.get('base_menor'))
            h_gondola = Decimal(request.POST.get('altura_gondola'))
            solape_val = Decimal(request.POST.get('solape'))
            
            # Si el usuario deja la cabecera vacía, usamos 0.5 por defecto
            d_cab_raw = request.POST.get('distancia_cabecera')
            d_cabecera = Decimal(d_cab_raw) if d_cab_raw else Decimal('0.5')

            # Ahora sí, guardamos en la base de datos con los tipos correctos
            gondola = ProyectoGondola.objects.create(
                nombre=nombre_gondola,
                largo_gondola=l_gondola
            )
            
            calculo = CalculoCamara.objects.create(
                gondola=gondola,
                base_mayor=b_mayor,
                base_menor=b_menor,
                altura_gondola=h_gondola,
                solape=solape_val,
                distancia_cabecera=d_cabecera
            )
            
            return render(request, 'calculadora/resultado.html', {
                'gondola': gondola,
                'calculo': calculo
            })

        except InvalidOperation:
            # Esto atrapa el error si el usuario escribe letras en lugar de números
            messages.error(request, "Por favor, ingresa solo números válidos (usa punto en vez de coma para los decimales).")
            return render(request, 'calculadora/formulario.html')
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado: {e}")
            return render(request, 'calculadora/formulario.html')

    return render(request, 'calculadora/formulario.html')