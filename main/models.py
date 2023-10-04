from django.db import models

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    uuid = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Unique ID field
    name = models.CharField(max_length=50)
    TYPE_CHOICES = [
        ('Domain', 'Domain'),
        ('Skill', 'Skill'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # LEVEL_CHOICES = [
    #     ('basic', 'Basic'),
    #     ('intermediate', 'Intermediate'),
    #     ('advanced', 'Advanced'),
    # ]
    # level = models.CharField(max_length=15, choices=LEVEL_CHOICES , null=True)

    def __str__(self):
        return f"{self.name}    "



class UsersTag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'tag']

    def __str__(self):
        return f"{self.userdata.username} - {self.tag.name}"
    
    
class ProjectsTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['project', 'tag']

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"


