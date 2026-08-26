from django.test import TestCase

from ..models import Usuario


class UsuarioRolTests(TestCase):
    def test_rol_default(self):
        """Verifica que el rol por defecto es 'docente'."""
        usuario = Usuario(username="docente1")
        self.assertEqual(usuario.rol, Usuario.Rol.DOCENTE)

    def test_rol_choices(self):
        """Verifica que existen las 4 opciones válidas de rol."""
        choices = dict(Usuario.Rol.choices)
        self.assertEqual(
            choices,
            {
                "docente": "Docente",
                "preceptor": "Preceptor",
                "directivo": "Directivo",
                "admin": "Admin",
            },
        )

    def test_es_docente(self):
        """Verifica que es_docente=True si rol=docente."""
        usuario = Usuario(username="docente1", rol=Usuario.Rol.DOCENTE)
        self.assertTrue(usuario.es_docente)
        self.assertFalse(usuario.es_preceptor)
        self.assertFalse(usuario.es_directivo)
        self.assertFalse(usuario.es_admin)

    def test_es_admin(self):
        """Verifica que es_admin=True si rol=admin."""
        usuario = Usuario(username="admin1", rol=Usuario.Rol.ADMIN)
        self.assertTrue(usuario.es_admin)
        self.assertFalse(usuario.es_docente)

    def test_str(self):
        """Verifica que __str__ retorna nombre completo o username."""
        usuario_nombre = Usuario(
            username="jperez",
            first_name="Juan",
            last_name="Pérez",
        )
        self.assertEqual(str(usuario_nombre), "Juan Pérez")

        usuario_sin_nombre = Usuario(username="jperez")
        self.assertEqual(str(usuario_sin_nombre), "jperez")