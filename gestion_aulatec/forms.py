from django import forms
from .models import Usuario,Grado,Estudiante,Docente,Materia,Matricula

#formulario para el modelo Usuario
class UsuarioForm(forms.ModelForm):
    # Añadimos un campo de contraseña y confirmación que NO están en el modelo
    # Esto es solo para la entrada del formulario
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        # NO INCLUYAS 'password' aquí, porque AbstractBaseUser ya lo maneja internamente.
        # Los campos que se incluyen aquí son los que *tú* definiste en tu modelo.
        fields = ['TipoId', 'NumId', 'Nombres', 'Apellidos', 'Rol', 'Celular']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.") # Error asociado a un campo
            # O raise forms.ValidationError("Las contraseñas no coinciden.") para un error global
        return cleaned_data

#formulario para el modelo Grado
class GradoForm(forms.ModelForm):
      class Meta:
            model = Grado
            exclude = ['IdGrado','NumEstudiantes'] #IdGrado es PK, NumEstudiantes Se Actualiza con logica

            labels = {
                  'NumGrado':'Número de Grado',
                  'NumCurso':'Número de Curso',
            }

            widgets = {
                  'NumCurso': forms.TextInput(attrs={'placeholder': 'A,B,C'})
            }

# formulario para el modelo Estudiante
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['IdEstudiante'] # IdEstudiante es PK autoincremental
        # O:
        # fields = ['IdUsuario', 'IdGrado']
        labels = {
            'IdUsuario': 'Usuario Asociado',
            'IdGrado': 'Grado Asignado',
        }

#formulario para el modelo Docente
class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        exclude = ['IdDocente'] #IdDocente es PK autoincremental
        
        labels = {
            'IdUsuario':'Usuario Asociado (Docente)',        
        }
    
#formulario para el modelo Materia
class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        exclude = ['IdMateria']

        labels = {
            'NombreMateria' : 'Nombre de la Materia',
            'IdDocente' : 'Docente Asignado (Docente)',
        }

#formulario del login 
class LoginForm(forms.Form):
    NumId = forms.CharField(max_length=50, label='Número de identificación')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

#Formulario para Matricula
class MatriculaForm(forms.Form):
    #Información del Colegio/Año Lectivo
    nombre_colegio = forms.CharField(max_length=255, label="Nombre del Colegio", initial="Mi Colegio Ejemplo")
    anio_lectivo = forms.IntegerField(label="Año Lectivo", initial=2025)
    IdGrado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        label="Grado a Matricular",
        empty_label="Seleccione un Grado"
    )

    # Información del Estudiante 
    estudiante_nombres = forms.CharField(max_length=100, label="Nombres del estudiante")
    estudiante_apellidos = forms.CharField(max_length=100, label="Apellidos del estudiante")
    estudiante_tipo_id = forms.CharField(max_length=20, label="Tipo de documento")
    estudiante_num_id = forms.CharField(max_length=50, label="Número de documento")
    estudiante_celular = forms.CharField(max_length=20, label="Teléfono de contacto del estudiante", required=False)
    
    fecha_nacimiento_estudiante = forms.DateField(label="Fecha de nacimiento", widget=forms.DateInput(attrs={'type': 'date'}))
    lugar_nacimiento_estudiante = forms.CharField(max_length=100, label="Lugar de nacimiento", required=False)
    direccion_residencia_estudiante = forms.CharField(max_length=255, label="Dirección de residencia")
    barrio_vereda_estudiante = forms.CharField(max_length=100, label="Barrio/Vereda", required=False)
    eps_seguro_medico_estudiante = forms.CharField(max_length=100, label="EPS o seguro médico", required=False)
    tiene_condicion_medica = forms.BooleanField(label="¿Tiene alguna condición médica o discapacidad?", required=False)
    especificacion_condicion_medica = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="En caso afirmativo, especifique",
        required=False
    )

    #Información del Acudiente
    Acudiente_TipoId = forms.CharField(label="Tipo de Identificación Acudiente", max_length=50) 
    Acudiente_NumId = forms.CharField(label="Número de Identificación Acudiente", max_length=50)
    Acudiente_Nombres = forms.CharField(label="Nombres del Acudiente", max_length=100)
    Acudiente_Apellidos = forms.CharField(label="Apellidos del Acudiente", max_length=100)
    Acudiente_Celular = forms.CharField(label="Celular del Acudiente", max_length=20, required=False)
    Acudiente_Parentesco = forms.CharField(label="Parentesco con el Estudiante", max_length=50)


    # Información Académica
    ultimo_grado_cursado = forms.CharField(max_length=50, label="Último grado cursado", required=False)
    institucion_anterior = forms.CharField(max_length=255, label="Institución anterior", required=False)
    ciudad_municipio_institucion_anterior = forms.CharField(max_length=100, label="Ciudad o municipio", required=False)
    repite_grado = forms.BooleanField(label="¿Repite grado?", required=False)
    requiere_apoyo_pedagogico = forms.BooleanField(label="¿Requiere apoyo pedagógico especial?", required=False)

    # Autorizaciones
    autoriza_tratamiento_datos = forms.BooleanField(label="Autorizo el tratamiento de los datos personales conforme a la Ley de Protección de Datos.", required=True)
    
    # CAMPOS PARA DOCUMENTOS REQUERIDOS (CHECKLIST) 
    # Documentos Requeridos del Estudiante
    doc_identidad_estudiante_presentado = forms.BooleanField(
        label="Copia del documento de identidad o registro civil.",
        required=False # O 'True' si es obligatorio marcarlo
    )
    certificado_notas_anterior_presentado = forms.BooleanField(
        label="Certificado de notas del año anterior.",
        required=False
    )
    fotocopia_carnet_vacunacion_presentado = forms.BooleanField(
        label="Fotocopia del carné de vacunación (para estudiantes menores).",
        required=False
    )
    fotocopia_eps_seguro_medico_presentado = forms.BooleanField(
        label="Fotocopia de la EPS o seguro médico.",
        required=False
    )
    fotos_tamano_documento_presentadas = forms.BooleanField(
        label="2 fotos recientes tamaño documento.",
        required=False
    )
    certificado_medico_presentado = forms.BooleanField(
        label="Certificado médico (opcional según el colegio).",
        required=False
    )
    
    # Documentos del Acudiente
    copia_cedula_acudiente_presentado = forms.BooleanField(
        label="Copia de la cédula del padre, madre o acudiente responsable.",
        required=False
    )
    comprobante_residencia_acudiente_presentado = forms.BooleanField(
        label="Comprobante de residencia (factura de servicios).",
        required=False
    )


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('tiene_condicion_medica') and not cleaned_data.get('especificacion_condicion_medica'):
            self.add_error('especificacion_condicion_medica', 'Debe especificar la condición médica.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdGrado'].queryset = Grado.objects.all()

    def save(self, commit=True):
        pass # La lógica de guardado sigue en la vista