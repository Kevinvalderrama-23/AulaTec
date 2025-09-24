from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para CBVs(Vistas basadas en clases)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, View, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
import random
import string

from gestion_aulatec.forms import MatriculaForm
from gestion_aulatec.models import Usuario,Estudiante,Matricula

#funcion para generar una constrasela aleatoria segura
def generar_contrasena_segura(longitud=12):                         
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena


# Vistas CRUD Matricula
class MatriculaCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
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