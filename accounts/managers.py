from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, national_code, age, password=None):
        """
        Creates and saves a User with the given national_code , age and password.
        """
        if not national_code:
            raise ValueError("Users must have an national code")

        user = self.model(
            national_code= national_code,
            age=age,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_code, age, password=None):
        """
        Creates and saves a superuser with the given national_code, age
        and password.
        """
        user = self.create_user(
            national_code,
            age=age,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
