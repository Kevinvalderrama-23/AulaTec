from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin #importar para Autenticación
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, NumId, password=None, **extra_fields):
        if not NumId:
            raise ValueError('El número de identificación debe ser proporcionado.')
        user = self.model(NumId=NumId , **extra_fields) # Crea el usuario con NumId
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, NumId, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('Rol', 'Administrador')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Llama a create_user con 'num_id' como el primer argumento posicional
        # y luego pasa el resto de los extra_fields.
        # 'createsuperuser' de Django lo espera así cuando USERNAME_FIELD es el primer argumento.
        return self.create_user(NumId, password, **extra_fields)

# Modelo para la tabla Usuario
class Usuario(AbstractBaseUser, PermissionsMixin): # Hereda de AbstractBaseUser y PermissionsMixin
    IdUsuario = models.AutoField(primary_key=True)
    TipoId = models.CharField(max_length=20)
    NumId = models.CharField(max_length=50, unique=True)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    # Contrasena ya no se define aquí directamente, AbstractBaseUser la maneja
    Rol = models.CharField(max_length=50)
    Celular = models.CharField(max_length=20, blank=True, null=True)

    # Campos requeridos por AbstractBaseUser (para el admin de Django, etc.)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager() # Asigna tu CustomUserManager

    USERNAME_FIELD = 'NumId' # Campo que se usará para el login (nombre de usuario)
    REQUIRED_FIELDS = ['TipoId', 'Nombres', 'Apellidos', 'Rol'] # Campos requeridos al crear superusuario

    def __str__(self):
        return f"{self.Nombres} {self.Apellidos} ({self.Rol})"

    # Métodos necesarios para PermissionsMixin si no usas los grupos y permisos de Django directamente
    # (aunque PermissionsMixin los provee, si solo usas el campo Rol, puedes ignorar estos para el login)
    
    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser # O implementa lógica de rol más compleja

    def has_module_perms(self, app_label):
        return self.is_active and self.is_superuser # O implementa lógica de rol más compleja

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

#Modelo para la tabla Grado

class Grado(models.Model):

    IdGrado = models.AutoField(primary_key=True)
    NumGrado = models.IntegerField(unique=True) #El numero de grado debe ser unico 
    NumCurso = models.CharField(max_length=20) # puede ser a, b o 501, 502
    NumEstudiantes = models.IntegerField(default=0) #Campo numerico para la cantidad de estudiantes (default=0) establece un valor inicial

    def __str__(self):
        if self.NumCurso:
            return f"Grado{self.NumGrado}"
        return f"Grado{self.NumGrado}"

    class Meta:
        db_table = 'Grado'
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        
        #Esta es una restricción a nivel de base de datos, lo que asegura que no puedas tener dos registros iguales
        unique_together = ('NumGrado','NumCurso') 

# Modelo para la tabla Estudiante
class Estudiante(models.Model):
    IdEstudiante = models.AutoField(primary_key=True)
    # Clave Foránea a Usuario
    # on_delete=models.CASCADE significa que si el Usuario asociado es eliminado,
    # este Estudiante también será eliminado.
    IdUsuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)
    IdGrado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        nombre_usuario = f"{self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}" if self.IdUsuario else "Usuario Desconocido"
        grado_info = f" (Grado {self.IdGrado.NumGrado}{self.IdGrado.NumCurso})" if self.IdGrado else ""
        return f"{nombre_usuario}{grado_info}"

    class Meta:
        db_table = 'Estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

#Modelo para la tabla docente
class Docente(models.Model):
    IdDocente = models.AutoField(primary_key = True)
     # Clave Foránea a Usuario
    # on_delete=models.CASCADE significa que si el Usuario asociado es eliminado,
    # este Docente también será eliminado.
    # unique=True para asegurar que cada Usuario solo puede ser un Docente.
    IdUsuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        # Muestra el nombre completo del Usuario asociado si existe
        if self.IdUsuario:
            return f"Docente: {self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}"
        return "Docente sin Usuario asignado" # En caso de que IdUsuario sea nulo (lo cual no debería ocurrir con OneToOneField sin null=True)

    class Meta:
        db_table = 'Docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

#Modelo para la tabla materia
class Materia(models.Model):
    IdMateria = models.AutoField(primary_key = True, unique=True )
    NombreMateria = models.CharField(max_length = 50)
    IdDocente = models.ForeignKey(Docente, on_delete = models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        if self.IdDocente and self.IdDocente.IdUsuario:
            return f"{self.NombreMateria} (Docente: {self.IdDocente.IdUsuario.Nombres}{self.IdDocente.IdUsuario.Apellidos})" 
        return f"{self.NombreMateria} (Docente no asigando)"

    class Meta:
        db_table = 'Materia'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'


#Modelo para la tabla Matricula
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
