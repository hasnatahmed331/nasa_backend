from django.db import models

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    uuid = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True , blank=True , null=True)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Unique ID field
    name = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.name} "


class UsersTag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'tag']

    def __str__(self):
        return f"{self.user.name} - {self.tag.name}"
    
    
class ProjectsTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['project', 'tag']

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"

class CommunicationAccess(models.Model):
    has_access_to = models.ForeignKey(CustomUser, related_name='access_to', on_delete=models.CASCADE)
    to_this_person = models.ForeignKey(CustomUser, related_name='access_from', on_delete=models.CASCADE)
    status = models.CharField(choices=[('requested', 'Requested'), ('approved', 'Approved')], max_length=20)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.has_access_to.name} has access of {self.to_this_person.name} with status {self.status}"    

