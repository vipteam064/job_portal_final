import re
from django.utils.translation import gettext_lazy as _, ngettext
from django.core.exceptions import ValidationError

class NumberValidator:
    def validate(self, password, user=None):
        if re.search('\d', password) is None:
            raise ValidationError(
                _("The password must contain at least 1 digit (0-9)."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit (0-9)."
        )

class UppercaseValidator:
    def validate(self, password, user=None):
        if re.search('[A-Z]', password) is None:
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter (A-Z)."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter (A-Z)."
        )

class LowercaseValidator:
    def validate(self, password, user=None):
        if re.search('[a-z]', password) is None:
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter (a-z)."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter (a-z)."
        )

class SymbolValidator:
    def validate(self, password, user=None):
        if re.search('[@\$\!%\*\?&]', password) is None:
            raise ValidationError(
                _("The password must contain at least 1 symbol (@$!%*?&)"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol (@$!%*?&)"
        )

class MaximumLengthValidator:
    def __init__(self, max_length=20):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain at most %(max_length)d character.",
                    "This password is too long. It must contain at most %(max_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at most %(max_length)d character.",
            "Your password must contain at most %(max_length)d characters.",
            self.max_length
        ) % {'max_length': self.max_length}
