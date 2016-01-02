from django.core.management.base import BaseCommand
from django.db.models.loading import get_model


groups = {
    'President': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
        'default.UserSocialAuth',
    ),
    'Vice President': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
        'default.UserSocialAuth',
    ),
    'Treasurer': (
        'profiles.DuesPayment',
    ),
    'Secretary': (
        'tours.Tour',
        'profiles.DuesPayment',
        'profiles.InactiveSemester',
        'profiles.OverrideRequirement',
        'profiles.Person',
        'core.Setting',
        'auth.User',
        'auth.Group',
        'default.UserSocialAuth',
    ),
    'Tour Coordinators': (
        'tours.Tour',
        'tours.CanceledDay',
        'tours.DefaultTour',
        'tours.InitializedMonth',
        'tours.OpenMonth',
        'core.Setting',
    ),
    'Freshman Week Coordinators': (
        'tours.Tour',
        'shifts.Shift',
    ),
    'Board Members': (
        'shifts.Shift',
    ),
}


class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        ContentType = get_model("contenttypes", "ContentType")
        Permission = get_model("auth", "Permission")
        Group = get_model("auth", "Group")

        for group_name, model_names in groups.iteritems():
            content_types = [ContentType.objects.get(app_label=model_name.rsplit('.', 1)[0], model=model_name.rsplit('.', 1)[1].lower()) for model_name in model_names]
            group, created = Group.objects.get_or_create(name=group_name)
            for content_type in content_types:
                permissions = Permission.objects.filter(content_type=content_type)
                for permission in permissions:
                    group.permissions.add(permission)
