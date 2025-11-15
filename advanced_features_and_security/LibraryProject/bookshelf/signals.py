from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != "relationship_app":  # run only for this app
        return
    
    # Create groups
    editors_group, _ = Group.objects.get_or_create(name="Editors")
    viewers_group, _ = Group.objects.get_or_create(name="Viewers")
    admins_group, _ = Group.objects.get_or_create(name="Admins")

    # Retrieve permissions
    can_view = Permission.objects.get(codename="can_view")
    can_create = Permission.objects.get(codename="can_create")
    can_edit = Permission.objects.get(codename="can_edit")
    can_delete = Permission.objects.get(codename="can_delete")

    # Assign permissions to groups
    viewers_group.permissions.add(can_view)

    editors_group.permissions.add(can_view, can_create, can_edit)

    admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
