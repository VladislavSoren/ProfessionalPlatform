from django.core.exceptions import ObjectDoesNotExist

from shop_projects.models import Project, Creator


def user_is_creator(self):
    try:
        _ = self.request.user.creator
    except ObjectDoesNotExist:
        return False
    else:
        return True


def project_belongs_creator(self):
    project_object = Project.objects.get(pk=self.kwargs['pk'])
    projects_current_creator = self.request.user.creator.projects_for_creators.all()

    if project_object in projects_current_creator:
        return True
    else:
        return False


def creator_belongs_user(self):
    creator_object = Creator.objects.get(pk=self.kwargs['pk'])
    creator_current_user = self.request.user.creator

    if creator_current_user == creator_object:
        return True
    else:
        return False
