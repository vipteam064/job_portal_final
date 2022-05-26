from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, PROTECT
from django.core import validators
from django.utils.translation import gettext_lazy as _
from job_portal_final.custom_fields import *
import job_portal_final.myvalidators as myvalidators

# Create your models here.
class Country_master(models.Model):
    country_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='Country name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('A country with that name already exists.'),
        }
    )

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State_master(models.Model):
    country = models.ForeignKey(Country_master, on_delete=PROTECT)
    state_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='State name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('A state with that name already exists.'),
        }
    )

    def __str__(self):
        return self.state_name

    class Meta:
        verbose_name = 'State'

class City_master(models.Model):
    state = models.ForeignKey(State_master, on_delete=PROTECT)
    city_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='City name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('A city with that name already exists.'),
        }
    )

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

class Area_master(models.Model):
    city = models.ForeignKey(City_master, on_delete=PROTECT)
    area_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='Area name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('An area with that name already exists.'),
        }
    )
    # NOTE: setting pincode to unique=True for now, but different areas in different countries might have the same pincode
    pincode = UpperCharField(
        max_length=10,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^(?!0)[0-9]{6}$',
                message='Pincode must be a 6 digit code and should not start with 0.'
            ),
        ],
        error_messages={
            'unique': _('An area with that pincode already exists.'),
        }
    )

    def __str__(self):
        return self.area_name

    class Meta:
        verbose_name = 'Area'

class Institute_master(models.Model):
    INSTITUTE_TYPE_CHOICES = ((False, 'School'), (True, 'College or University'))
    institute_name = UpperCharField(
        max_length=60,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='Institute name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('An institute with that name already exists.'),
        }
    )
    institute_type = models.BooleanField(choices=INSTITUTE_TYPE_CHOICES)

    def __str__(self):
        return self.institute_name

    class Meta:
        verbose_name = 'Institute'

class Degree_master(models.Model):
    # NOTE: Since degree_name regex doesn't allow numbers you will have to force it to save '10TH CLASS' and '12TH CLASS'
    degree_name = UpperCharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='Degree name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ]
    )
    degree_type = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=PROTECT
    )

    def clean(self):
        valid_degree_types = Degree_master.objects.filter(Q(degree_type__isnull=True) & ~Q(degree_name__in=['10TH CLASS', '12TH CLASS']))
        if hasattr(self, 'degree_type') and self.degree_type not in valid_degree_types:
            raise ValidationError({'degree_type': f'Degree type should be one of the following - {", ".join([str(i) for i in valid_degree_types])}.'})

    def __str__(self):
        if self.degree_type:
            return self.degree_type.degree_name + ' OF ' + self.degree_name
        else:
            return self.degree_name

    class Meta:
        verbose_name = 'Degree'
        constraints = [
            models.UniqueConstraint(name='unique_degree', fields=['degree_name', 'degree_type']),
        ]

class Skill_master(models.Model):
    skill_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'[a-zA-Z]+',
                message='Skill name should contain atleast one letter.'
            ),
            # same as name_regex but + and digits are allowed and diacritics are not included
            validators.RegexValidator(
                regex=r'^(?![ \'()\-\.\+])(?:[a-zA-Z\d]|[\'()\-\.](?![\'()\-\.])| (?! )|\+)+(?<![ \'(\-])$',
                message='Skill name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), + (plus signs) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('A skill with that name already exists.'),
        }
    )

    def __str__(self):
        return self.skill_name

    class Meta:
        verbose_name = 'Skill'

class Industry_master(models.Model):
    industry_name = UpperCharField(
        max_length=30,
        unique=True,
        validators=[
            # same as name_regex but / is allowed, and diacritics are not included
            validators.RegexValidator(
                regex=r'^(?![ \'()\-\.\/])(?:[a-zA-Z]|[\'()\-\.\/](?![\'()\-\.\/])| (?! ))+(?<![ \'(\-\/])$',
                message='Industry name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), / (forward slashes) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('An industry with that name already exists.'),
        }
    )

    def __str__(self):
        return self.industry_name

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

class Membership_master(models.Model):
    membership_name = UpperCharField(
        max_length=40,
        unique=True,
        validators=[
            # should not start with space
            # should contain atleast one letter or space
            # space cannot be followed by itself
            # The word may end with plus sign(s)
            # should not end with space
            validators.RegexValidator(
                regex=r'^(?! )(?:[a-zA-Z]| (?! ))+\+*(?<! )$',
                message='Membership name must contain only letters, space or + (plus sign) .'
            ),
        ],
        error_messages={
            'unique': _('A membership with that name already exists.'),
        }
    )
    membership_description = models.TextField(max_length=200)
    price = models.PositiveIntegerField()
    duration = models.PositiveSmallIntegerField(validators=[
        validators.MinValueValidator(1, message='Duration must be more than 1.'),
    ])
    number_of_post = models.PositiveSmallIntegerField(validators=[
        validators.MinValueValidator(1, message='Number of posts must be more than 1.'),
    ])

    def __str__(self):
        return self.membership_name

    class Meta:
        verbose_name = 'Membership'
