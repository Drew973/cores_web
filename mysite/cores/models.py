from django.db import models



class Job(models.Model):
    job_number = models.CharField(max_length=100,primary_key=True)
    client = models.CharField(max_length=100)
    project = models.CharField(max_length=100)



class Core(models.Model):
    
    job_number = models.ForeignKey(Job, on_delete=models.CASCADE)
    sample_number = models.PositiveIntegerField(primary_key=True)
    core_number = models.IntegerField()
    sec = models.CharField(max_length=50,blank=True)
    chainage = models.IntegerField()


    class Meta:
        unique_together = ('job_number', 'core_number',)
        
        
class Layer(models.Model):
    sample_number = models.ForeignKey(Core, on_delete=models.CASCADE)
    material = models.CharField(max_length=30,blank=True)
