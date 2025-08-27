from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import Usuario

#Prueba de Cración de usuarios 
class PruebasIntegracionUsuario(TestCase):

    def test_crear_usuario(self):
        datos_usuario = {
            'TipoId':'CC',
            'NumId':'0000',
            'Nombres':'Kevin',
            'Apellidos':'Valderrama',
            'Rol':'Administrador',
            'Celular':'3004897185',
            'password':'123456789',
            'password_confirm':'123456789'
        }
        
        url_registro = reverse('gestion_aulatec:usuario_create')
        response = self.client.post(url_registro, datos_usuario)

        self.assertTrue(Usuario.objects.filter(NumId='0000').exists())

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestion_aulatec:login'))

#Pruebas de Inicio de Sesion
class PruebasInicioSesion(TestCase):
    def setUp(self):
        self.password = 'contraseña_encriptada'
        self.usuario_valido = Usuario.objects.create_user(
            NumId='0000',
            password = self.password,
            TipoId = 'CC',
            Nombres = 'Kevin',
            Apellidos = 'Valderrama',
            Rol = 'Administrador'
        )

    def test_inicio_sesion_exitoso(self):

        login_exitoso = self.client.login(NumId='0000', password=self.password)

        self.assertTrue(login_exitoso)

        response = self.client.get(reverse('gestion_aulatec:admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'gestion_aulatec/admin_dashboard.html')
        self.assertContains(response, 'Kevin')

    def test_inicio_sesion_fallido(self):

        login_fallido = self.client.login(NumId='0000', password='contraseña_incorrecta')

        self.assertFalse(login_fallido)

        response = self.client.get(reverse('gestion_aulatec:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('gestion_aulatec:login')}?next={reverse('gestion_aulatec:admin_dashboard')}")
        
#Pruebas 