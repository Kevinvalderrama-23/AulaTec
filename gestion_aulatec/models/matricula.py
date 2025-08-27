from django.db import models

class Matricula(models.Model):
    NumMatricula = models.CharField(max_length=100, unique=True, verbose_name="Número de Matrícula")
    IdEstudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, verbose_name="Estudiante")
    IdGrado = models.ForeignKey('Grado', on_delete=models.CASCADE, verbose_name="Grado a Matricular")
    anio_lectivo = models.IntegerField(verbose_name="Año Lectivo")
    nombre_colegio = models.CharField(max_length=200, verbose_name="Nombre del Colegio de Procedencia")
    fecha_nacimiento_estudiante = models.DateField(verbose_name="Fecha de Nacimiento del Estudiante")
    lugar_nacimiento_estudiante = models.CharField(max_length=100, verbose_name="Lugar de Nacimiento del Estudiante")
    barrio_vereda_estudiante = models.CharField(max_length=100, verbose_name="Barrio/Vereda del Estudiante")
    eps_seguro_medico_estudiante = models.CharField(max_length=100, verbose_name="EPS o Seguro Médico del Estudiante")
    tiene_condicion_medica = models.BooleanField(default=False, verbose_name="¿Tiene alguna condición médica?")
    especificacion_condicion_medica = models.TextField(blank=True, null=True, verbose_name="Especificar condición médica (si aplica)")

    ultimo_grado_cursado = models.CharField(max_length=50, verbose_name="Último Grado Cursado")
    institucion_anterior = models.CharField(max_length=200, verbose_name="Institución Educativa Anterior")
    ciudad_municipio_institucion_anterior = models.CharField(max_length=100, verbose_name="Ciudad/Municipio de la Institución Anterior")
    repite_grado = models.BooleanField(default=False, verbose_name="¿Repite Grado?")
    requiere_apoyo_pedagogico = models.BooleanField(default=False, verbose_name="¿Requiere Apoyo Pedagógico?")
    autoriza_tratamiento_datos = models.BooleanField(default=False, verbose_name="Autoriza Tratamiento de Datos")

    #CAMPOS DEL ACUDIENTE 
    Acudiente_TipoId = models.CharField(max_length=50, verbose_name="Tipo ID Acudiente") # Puedes hacer esto choices si quieres
    Acudiente_NumId = models.CharField(max_length=50, verbose_name="Número de Identificación Acudiente")
    Acudiente_Nombres = models.CharField(max_length=100, verbose_name="Nombres del Acudiente")
    Acudiente_Apellidos = models.CharField(max_length=100, verbose_name="Apellidos del Acudiente")
    Acudiente_Celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular del Acudiente")
    Acudiente_Parentesco = models.CharField(max_length=50, verbose_name="Parentesco con el Estudiante") # Puedes hacer esto choices
    #FIN CAMPOS DEL ACUDIENTE

    doc_identidad_estudiante_presentado = models.BooleanField(default=False, verbose_name="Documento de Identidad Estudiante Presentado")
    certificado_notas_anterior_presentado = models.BooleanField(default=False, verbose_name="Certificado de Notas Anterior Presentado")
    fotocopia_carnet_vacunacion_presentado = models.BooleanField(default=False, verbose_name="Fotocopia Carnet de Vacunación Presentado")
    fotocopia_eps_seguro_medico_presentado = models.BooleanField(default=False, verbose_name="Fotocopia EPS/Seguro Médico Presentado")
    fotos_tamano_documento_presentadas = models.BooleanField(default=False, verbose_name="Fotos Tamaño Documento Presentadas")
    certificado_medico_presentado = models.BooleanField(default=False, verbose_name="Certificado Médico Presentado")
    copia_cedula_acudiente_presentado = models.BooleanField(default=False, verbose_name="Copia Cédula Acudiente Presentado")
    comprobante_residencia_acudiente_presentado = models.BooleanField(default=False, verbose_name="Comprobante de Residencia Acudiente Presentado")

    FechaMatricula = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Matrícula")

    class Meta:
        db_table = 'Matricula'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return f"Matrícula {self.NumMatricula} - {self.IdEstudiante.IdUsuario.Nombres} {self.IdEstudiante.IdUsuario.Apellidos}"
