from django.contrib.auth.models import User

# Add an index for the User.password field since we'll be using it to store
# GAE user_ids.
for field in User._meta.local_fields:
    if field.column == 'password':
        field.db_index = True
        break
