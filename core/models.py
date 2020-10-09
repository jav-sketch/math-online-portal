from django.db import models

# Create your models here.


class Course(models.Model):
    CATEGORY = (
        ('FT', 'FULL TIME'),
        ('AS', 'AFTER SCHOOL'),
        ('EC', 'EVENING CLASSES'),
        ('PT', 'PRIVATE TUTORING'),
        ('SC', 'SATURDAY CLASSES'),
        ('SC', 'SPECIALIZED COURSES'),
    )

    CATEGORY_CHOICES = (
        ('N', 'NONE'),
        ('PT', 'PART-TIME'),
        ('F', 'FULL-TIME'),
    )
    title = models.CharField(max_length=200, null=True)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY, max_length=20)
    evening = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    price = models.FloatField()
    slug = models.SlugField()

    def __str__(self):
        return self.title
