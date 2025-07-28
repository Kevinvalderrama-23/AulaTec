from django.urls import path
from . import views  # importa las vistas del archivo views.py

app_name = 'gestion_aulatec'  # Define un nombre de espacio para tus URLs

urlpatterns = [
    # URL para la autenticación y Home
    path('', views.home_view, name='home'),  # Página de inicio
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/docente/', views.DocenteDashboardView.as_view(), name='docente_dashboard'),
    path('dashboard/estudiante/', views.EstudianteDashboardView.as_view(), name='estudiante_dashboard'),

    # URL para listar todos los usuarios
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    # URL para crear un nuevo usuario
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    # URL para actualizar un usuario existente (pk es la clave primaria)
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    # URL para eliminar un usuario existente
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),

    # URLs para grado
    path('grados/', views.GradoListView.as_view(), name='grado_list'),
    path('grados/nuevo/', views.GradoCreateView.as_view(), name='grado_create'),
    path('grados/<int:pk>/editar/', views.GradoUpdateView.as_view(), name='grado_update'),
    path('grados/<int:pk>/eliminar/', views.GradoDeleteView.as_view(), name='grado_delete'),

    # URLs para estudiante
    path('estudiantes/', views.EstudianteListView.as_view(), name='estudiante_list'),
    path('estudiantes/nuevo/', views.EstudianteCreateView.as_view(), name='estudiante_create'),
    path('estudiantes/<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='estudiante_update'),
    path('estudiantes/<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='estudiante_delete'),

    # URLs para docente
    path('docentes/', views.DocenteListView.as_view(), name='docente_list'),
    path('docentes/nuevo/', views.DocenteCreateView.as_view(), name='docente_create'),
    path('docentes/<int:pk>/editar/', views.DocenteUpdateView.as_view(), name='docente_update'),
    path('docentes/<int:pk>/eliminar/', views.DocenteDeleteView.as_view(), name='docente_delete'),

    # URLs para materia
    path('materias/', views.MateriaListView.as_view(), name='materia_list'),
    path('materias/nuevo/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),

    # URLs para matrícula
    path('matriculas/nueva/', views.MatriculaCreateView.as_view(), name='matricula_form'),
    path('matriculas/', views.MatriculaListView.as_view(), name='matricula_list'),
    path('matriculas/<int:pk>/detalles/', views.MatriculaDetailView.as_view(), name='matricula_detail'),
    path('matriculas/<int:pk>/editar/', views.MatriculaUpdateView.as_view(), name='matricula_update'),
    path('matriculas/<int:pk>/eliminar/', views.MatriculaDeleteView.as_view(), name='matricula_delete'),
]
