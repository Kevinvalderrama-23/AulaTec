from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout # Importar funciones de autenticación
from django.contrib.auth.decorators import login_required # Decorador para proteger vistas
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para CBVs
from django.contrib import messages # Para mensajes de feedback al usuario
import random 
import string


from .models import Usuario, Grado, Estudiante, Docente, Materia,Matricula
from .forms import MatriculaForm, UsuarioForm, GradoForm, EstudianteForm, DocenteForm, MateriaForm, LoginForm


def generar_contrasena_segura(longitud=12):                         
    #genera una contraseña aleatoria segura.
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

# Create your views here.
# CBV (Class Based Views)

# --- Vistas para el CRUD de Usuario ---

# Leer (Listar todos los usuarios)
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'gestion_aulatec/usuario_list.html'
    context_object_name = 'usuarios' # Nombre de la variable en la plantilla para la lista de usuarios
    def test_func(self):
        # Solo administradores pueden ver la lista de usuarios
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a la gestión de usuarios.')
        return redirect('gestion_aulatec:home') # O la página de login
     
# Crear (Agregar un nuevo usuario)
class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:login') # Redirige al login después de crear

    def form_valid(self, form):
        usuario = form.save(commit=False)
        # Usa el campo 'password' del formulario para hashear
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        messages.success(self.request, 'Usuario registrado con éxito. Ya puedes iniciar sesión.')
        return super().form_valid(form) # Llama al método original para manejar la redirección, etc.

# Actualizar (Editar un usuario existente)
class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')  # Redirige a la lista de usuarios después de actualizar uno

# Eliminar (Borrar un usuario)
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion_aulatec/usuario_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')  # Redirige a la lista de usuarios después de eliminar uno
    
    # Opcional: Personalizar el objeto que se mostrará en el template
    context_object_name = 'usuario' # Para que en el template puedas usar {{ usuario.Nombres }}


#--Vistas para el CRUD de Grado---

class GradoListView(ListView):
    model = Grado
    template_name = 'gestion_aulatec/grado_list.html'
    context_object_name = 'grados'

class GradoCreateView(CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')

class GradoUpdateView(UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')   

class GradoDeleteView(DeleteView):
    model = Grado
    template_name = 'gestion_aulatec/grado_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')
    
    context_object_name = 'grado'

# --- Vistas para el CRUD de Estudiante ---

# 1. Leer (Listar todos los Estudiantes) con filtro
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'gestion_aulatec/estudiante_list.html' # Nueva plantilla
    context_object_name = 'estudiantes' # Nombre de la variable en la plantilla
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Obtiene el término de búsqueda de la URL (ej. ?q=nombre)
        query = self.request.GET.get('q')

        #print(f"Debug: Terminos de busqueda (q): '{query}' ")

        if query:
            # Filtra por Nombres o Apellidos del Usuario asociado
            # Usa Q para combinar condiciones OR
            queryset = queryset.filter(
                Q(IdUsuario__Nombres__icontains=query) |
                Q(IdUsuario__Apellidos__icontains=query)
            )

        #print(f"DEBUG: Longitud del queryset resultante: {queryset.count()}")
        #print(f"DEBUG: Contenido del queryset:")
        #for obj in queryset:
           #print(f"  - Estudiante ID: {obj.IdEstudiante}, Usuario: {obj.IdUsuario.Nombres} {obj.IdUsuario.Apellidos}")
        # ------------------------------------    


        return queryset.order_by('IdUsuario__Nombres', 'IdUsuario__Apellidos') # Opcional: ordenar

# 2. Crear un nuevo Estudiante
class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'gestion_aulatec/estudiante_form.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:estudiante_list') # Redirige a la lista de estudiantes

# 3. Actualizar un Estudiante existente
class EstudianteUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'gestion_aulatec/estudiante_form.html' # Reusa la misma plantilla
    success_url = reverse_lazy('gestion_aulatec:estudiante_list')

# 4. Eliminar un Estudiante
class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'gestion_aulatec/estudiante_confirm_delete.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:estudiante_list')
    context_object_name = 'estudiante' # Para usar {{ estudiante.IdUsuario.Nombres }} en el template

#Vistas para el CRUD de Docentes

#Leer (Listar todos los docentes)
class DocenteListView(ListView):
    model = Docente
    template_name = 'gestion_aulatec/docente_list.html' # Nueva plantilla
    context_object_name = 'docentes' # Nombre de la variable en la plantilla

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Filtra por Nombres o Apellidos del Usuario asociado
            queryset = queryset.filter(
                Q(IdUsuario__Nombres__icontains=query) |
                Q(IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('IdUsuario__Nombres', 'IdUsuario__Apellidos')

# 2. Crear un nuevo Docente
class DocenteCreateView(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list') # Redirige a la lista de docentes

# 3. Actualizar un Docente existente
class DocenteUpdateView(UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html' # Reusa la misma plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list')

# 4. Eliminar un Docente
class DocenteDeleteView(DeleteView):
    model = Docente
    template_name = 'gestion_aulatec/docente_confirm_delete.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list')
    context_object_name = 'docente' # Para usar {{ docente.IdUsuario.Nombres }} en el template

# Vistas para el CRUD de materia

#Leer (Listar todas las materias)
class MateriaListView(ListView):
    model = Materia
    template_name = 'gestion_aulatec/materia_list.html'
    context_object_name = 'materias'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(NombreMateria__icontains=query) |
                Q(IdDocente__IdUsuario__Nombres__icontains=query) |
                Q(IdDocente__IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('NombreMateria')
    
# Crear un nueva Materia
class MateriaCreateView(CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')

# Actualizar una Materia Existente
class MateriaUpdateView(UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')

# Eliminar una materia 
class MateriaDeleteView(DeleteView):
    model = Materia
    template_name = 'gestion_aulatec/materia_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')
    context_object_name = 'materia'

#Vistas de Autenticación(Login)
def login_view(request):
    if request.user.is_authenticated: #Si el usuario ya esta logueado, redirigir.
        return redirect('gestion_aulatec:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            NumId = form.cleaned_data['NumId']
            password = form.cleaned_data['password']
            # Autenticar al usuario
            user = authenticate(request,username=NumId, password=password)
            if user is not None:
                login(request, user) #Iniciar Sesión del usuario
                messages.success(request, f'Bienvenido!')
                #redireccionamiento depende del rol
                if user.Rol == 'Administrador':
                    return redirect('gestion_aulatec:admin_dashboard')#una url para el menu de administradores
                elif user.Rol == 'Docente':
                    return redirect('gestion_aulatec:docente_dashboard')#una Url para el menu de docente
                elif user.Rol == 'Estudiante':
                    return redirect('gestion_aulatec:estudiante_dashboard')#una Url para el menu del estudiante
                else: 
                    return redirect('gestion_aulatec:home')#una Url por defecto
            else:
                messages.error(request, 'Numero de identificacion o contraseña incorrecta.')

    else :
        form = LoginForm()
    return render(request, 'gestion_aulatec/login.html', {'form': form })

@login_required #Decorador para asegurar que el usuario este logueado para acceder a las vistas.
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('gestion_aulatec:logout')#Redirigir a la pagina de login despues de cerrar sesion

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/admin_dashboard.html'
    model = Usuario # O el modelo principa que quieras mostrar
    context_object_name = 'usuarios'

    def test_func(self):
        #solo permite el acceso si el usuario es Admninistrador
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home') # Redirige a una página de inicio o login
    
class DocenteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/docente_dashboard.html'
    model = Materia # Ejemplo: un docente ve sus materias
    context_object_name = 'materias'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Docente'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')

class EstudianteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/estudiante_dashboard.html'
    model = Estudiante # Ejemplo: un estudiante ve su perfil
    context_object_name = 'estudiante_perfil' # Asegúrate de filtrar por el usuario logueado en get_queryset

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')

    def get_queryset(self):
        # Filtra para obtener el perfil del estudiante logueado
        return Estudiante.objects.filter(IdUsuario=self.request.user)

def home_view(request):
    return render(request,'gestion_aulatec/home.html')

# Vistas CRUD Matricula
class MatriculaCreateView(LoginRequiredMixin, UserPassesTestMixin, View): # CAMBIADO de CreateView a View
    template_name = 'gestion_aulatec/matricula_form.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para realizar matrículas.')
        return redirect('gestion_aulatec:home')

    # Método GET: Muestra el formulario vacío
    def get(self, request, *args, **kwargs):
        form = MatriculaForm()
        return render(request, self.template_name, {'form': form})

    # Método POST: Procesa el formulario enviado
    def post(self, request, *args, **kwargs):
        form = MatriculaForm(request.POST) 
        if form.is_valid():
            try:
                # 1. Crear/Obtener Usuario para el Estudiante
                estudiante_usuario_data = {
                    'TipoId': form.cleaned_data['estudiante_tipo_id'],
                    'NumId': form.cleaned_data['estudiante_num_id'],
                    'Nombres': form.cleaned_data['estudiante_nombres'],
                    'Apellidos': form.cleaned_data['estudiante_apellidos'],
                    'Rol': 'Estudiante',
                    'Celular': form.cleaned_data['estudiante_celular'],
                }

                contrasena_estudiante = generar_contrasena_segura(12)    

                estudiante_usuario, created_eu = Usuario.objects.get_or_create(
                    NumId=estudiante_usuario_data['NumId'],
                    defaults={
                        'TipoId': estudiante_usuario_data['TipoId'],
                        'Nombres': estudiante_usuario_data['Nombres'],
                        'Apellidos': estudiante_usuario_data['Apellidos'],
                        'Rol': estudiante_usuario_data['Rol'],
                        'Celular': estudiante_usuario_data['Celular'],
                    }
                )
                if created_eu:
                    estudiante_usuario.set_password(contrasena_estudiante)
                    estudiante_usuario.save()
                else:
                    for key, value in estudiante_usuario_data.items():
                        setattr(estudiante_usuario, key, value)
                    estudiante_usuario.save()

                # 2. Crear/Obtener el objeto Estudiante
                estudiante, created_eu = Estudiante.objects.get_or_create(
                    IdUsuario=estudiante_usuario,
                    defaults={}
                )

                # 5. Crear la Matrícula (ahora con los campos booleanos)
                num_matricula = f"MAT-{form.cleaned_data['anio_lectivo']}-{random.randint(10000, 99999)}"
                while Matricula.objects.filter(NumMatricula=num_matricula).exists():
                     num_matricula = f"MAT-{form.cleaned_data['anio_lectivo']}-{random.randint(10000, 99999)}"

                matricula = Matricula(
                    NumMatricula=num_matricula,
                    IdEstudiante=estudiante, # El objeto estudiante ya fue creado/obtenido arriba
                    IdGrado=form.cleaned_data['IdGrado'], # Accede al campo del form directamente
                    anio_lectivo=form.cleaned_data['anio_lectivo'],
                    nombre_colegio=form.cleaned_data['nombre_colegio'],
                    fecha_nacimiento_estudiante=form.cleaned_data['fecha_nacimiento_estudiante'],
                    lugar_nacimiento_estudiante=form.cleaned_data['lugar_nacimiento_estudiante'],
                    barrio_vereda_estudiante=form.cleaned_data['barrio_vereda_estudiante'],
                    eps_seguro_medico_estudiante=form.cleaned_data['eps_seguro_medico_estudiante'],
                    tiene_condicion_medica=form.cleaned_data['tiene_condicion_medica'],
                    especificacion_condicion_medica=form.cleaned_data['especificacion_condicion_medica'],
                    ultimo_grado_cursado=form.cleaned_data['ultimo_grado_cursado'],
                    institucion_anterior=form.cleaned_data['institucion_anterior'],
                    ciudad_municipio_institucion_anterior=form.cleaned_data['ciudad_municipio_institucion_anterior'],
                    repite_grado=form.cleaned_data['repite_grado'],
                    requiere_apoyo_pedagogico=form.cleaned_data['requiere_apoyo_pedagogico'],
                    autoriza_tratamiento_datos=form.cleaned_data['autoriza_tratamiento_datos'],

                    # --- Asignar los campos del acudiente directamente al objeto matricula ---
                    Acudiente_TipoId = form.cleaned_data['Acudiente_TipoId'],
                    Acudiente_NumId = form.cleaned_data['Acudiente_NumId'],
                    Acudiente_Nombres = form.cleaned_data['Acudiente_Nombres'],
                    Acudiente_Apellidos = form.cleaned_data['Acudiente_Apellidos'],
                    Acudiente_Celular = form.cleaned_data['Acudiente_Celular'],
                    Acudiente_Parentesco = form.cleaned_data['Acudiente_Parentesco'],
                    # --- FIN Asignación campos acudiente ---

                    doc_identidad_estudiante_presentado=form.cleaned_data['doc_identidad_estudiante_presentado'],
                    certificado_notas_anterior_presentado=form.cleaned_data['certificado_notas_anterior_presentado'],
                    fotocopia_carnet_vacunacion_presentado=form.cleaned_data['fotocopia_carnet_vacunacion_presentado'],
                    fotocopia_eps_seguro_medico_presentado=form.cleaned_data['fotocopia_eps_seguro_medico_presentado'],
                    fotos_tamano_documento_presentadas=form.cleaned_data['fotos_tamano_documento_presentadas'],
                    certificado_medico_presentado=form.cleaned_data['certificado_medico_presentado'],
                    copia_cedula_acudiente_presentado=form.cleaned_data['copia_cedula_acudiente_presentado'],
                    comprobante_residencia_acudiente_presentado=form.cleaned_data['comprobante_residencia_acudiente_presentado'],
                    )
                matricula.save()

                messages.success(request, f'Matrícula {matricula.NumMatricula} creada con éxito para {estudiante.IdUsuario.Nombres}.')
                messages.info(request, f'Contraseña inicial estudiante (C.I.: {estudiante.IdUsuario.NumId}): {contrasena_estudiante}.')

                return redirect(reverse_lazy('gestion_aulatec:matricula_list'))
            except Exception as e:
                messages.error(request, f'Ocurrió un error al guardar la matrícula: {e}')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, self.template_name, {'form': form})
            
# Listar Matriculas.
# Esta parte también tiene un pequeño ajuste, aunque no es la causa del error actual
class MatriculaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_list.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')

#detalles de matricula
class MatriculaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_detail.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
#editar matricula
class MatriculaUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_form.html'
    context_object_name = 'matriculas'
    form_class = MatriculaForm

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
#eliminar matricula
class MatriculaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:matricula_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'La matrícula "{self.object.NumMatricula}" ha sido eliminada exitosamente.')
        return response