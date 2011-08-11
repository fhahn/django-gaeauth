from django.contrib.auth.models import User
from django.test import TestCase

class ModelsTest(TestCase):
    def test_password_indexed(self):
        """Tests that the password field on the User model is indexed."""
        password_indexed = False
        for field in User._meta.local_fields:
            if field.column == 'password':
                password_indexed = field.db_index
        self.assertTrue(password_indexed)
