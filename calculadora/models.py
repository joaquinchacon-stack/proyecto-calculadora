from django.db import models
from decimal import Decimal # <-- NUEVO IMPORT
import math

class ProyectoGondola(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Pasillo/Góndola")
    largo_gondola = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Largo de góndola (m)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class CalculoCamara(models.Model):
    gondola = models.OneToOneField(ProyectoGondola, on_delete=models.CASCADE, related_name="calculo")
    
    base_mayor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Base Mayor (m)")
    base_menor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Base Menor / Cobertura útil (m)")
    altura_gondola = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Altura enfocada (m)")
    solape = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Solape requerido (m)")
    distancia_cabecera = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Distancia a cabecera (m)", default=0.5)

    area_perdida = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    distancia_entre_camaras = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cantidad_camaras = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # CORRECCIÓN 1: Faltaba dividir la fórmula del área geométrica por 2
        if self.base_mayor and self.base_menor and self.altura_gondola:
            # Se usa Decimal('2') para mantener la precisión matemática
            self.area_perdida = ((self.base_mayor - self.base_menor) * self.altura_gondola) / Decimal('2')
            
        if self.base_menor and self.solape:
            self.distancia_entre_camaras = self.base_menor - self.solape
            
        if self.distancia_entre_camaras and self.distancia_entre_camaras > 0:
            largo_efectivo = self.gondola.largo_gondola - self.distancia_cabecera
            self.cantidad_camaras = math.ceil((largo_efectivo / self.distancia_entre_camaras)) + 1
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cálculo para {self.gondola.nombre}"