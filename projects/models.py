from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey


class ProjectPage(Orderable, Page):
    short_description = models.TextField()
    full_description = RichTextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.title:
            if self.project:
                self.title = self.project.name
        return super().save(*args, **kwargs)

    search_fields = Page.search_fields + (
        index.SearchField('short_description'),
        index.SearchField('full_description'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('full_description'),
        InlinePanel('links', label="Links"),
    ]


class ProjectLink(models.Model):
    TYPES = (
        ('main', 'Main'),
        ('github', 'GitHub'),
    )

    project = ParentalKey('projects.ProjectPage', related_name='links')
    type = models.CharField(max_length=20, choices=TYPES)
    description = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return "{0} / {1}".format(str(self.project), self.type)


class ProjectIndexPage(Page):
    subpage_types = ['projects.ProjectPage']

    def projects(self):
        return ProjectPage.objects.live()
