from django.contrib.auth.decorators import user_passes_test

def has_group(group):
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group).exists()
    
    return user_passes_test(in_group, login_url='403')
