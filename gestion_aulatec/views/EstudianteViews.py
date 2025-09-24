from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.db.models import Q
from django.urls import reverse_lazy

from gestion_aulatec.models import Estudiante
from gestion_aulatec.forms import EstudianteForm

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
