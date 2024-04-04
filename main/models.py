from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class LovedOneProfile(models.Model):
    name = models.CharField(max_length=50)
    pet_name = models.CharField(max_length=50)
    pronoun = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50)
    love_language = models.CharField(max_length=20)
    personality = models.CharField(max_length=20)
    likes = ArrayField(models.CharField(max_length=255),
                       size=5)
    phone_number = PhoneNumberField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
    def delete_permanently(self):
        super().delete()
    
    def __str__(self):
        return f"{self.name}"



class EventPreference(models.Model):
    event = models.CharField(max_length=50)
    loved_one = models.ForeignKey(LovedOneProfile, related_name="preference", on_delete=models.CASCADE)
    event_day = models.DateField()
    frequency = models.CharField(max_length=20, choices=(
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ))
    next_send_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    send_to_me = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
    def delete_permanently(self):
        super().delete()
        
    def __str__(self):
        return f"{self.loved_one.name}'s {self.event}"
        
        
    
class Message(models.Model):
    event = models.ForeignKey(EventPreference, related_name="messages", on_delete=models.CASCADE)
    to = models.ForeignKey(LovedOneProfile, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    is_sent = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
    def delete_permanently(self):
        super().delete()
        
        
    def __str__(self):
        return f"{self.event.loved_one.name}'s {self.event.event} message {self.id}"
    
    


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    subscription_type = models.CharField(max_length=50, choices=(("annual", "annual"),
                                                                 ("monthly", "monthly"))) # 'annual' or 'monthly'
    amount= models.FloatField()
    payment_ref = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
    def delete_permanently(self):
        super().delete()
        
        
    def __str__(self):
        return f"{self.subscription_type.title()} subscription for {self.user.first_name}"
    
    def has_expired(self):
        return timezone.now() > self.end_date
    

def get_current_subscription(user):
    """Use this to get the current subscription of the user"""
    
    return user.subscriptions.filter(is_deleted=False).order_by('-date_added').first()



class SMSResponse(models.Model):
    text_json = models.JSONField()
    ai_response = models.TextField()
    service = models.CharField(max_length=50, choices=(("twilio","twilio"),
                                                       ("vonage", "vonage"),))
    timestamp = models.DateTimeField(auto_now_add=True)
    