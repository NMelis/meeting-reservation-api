from django.contrib.auth.models import AbstractUser
from typing import final, Final
from django.utils.translation import gettext_lazy as _

#: That's how constants should be defined.
_POST_TITLE_MAX_LENGTH: Final = 80


@final
class User(AbstractUser):

    def __str__(self):
        return _("Пользователь: %(name)s ") % {
            "name": self.username,
        }
