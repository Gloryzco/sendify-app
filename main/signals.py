

import os
import openai
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from .models import Message, EventPreference, LovedOneProfile

openai.api_key = os.getenv("OPENAI_API_KEY")


@receiver(post_save, sender=EventPreference)
def create_message(sender, instance, created, **kwargs):
    
    if created:
        messages= []
        loved_one = instance.loved_one
        loved_one:LovedOneProfile
        
        likes = ", ".join(loved_one.likes)
        
        
        for i in range(7):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"create a short sms for my {loved_one.relationship}. Today is {loved_one.pronoun} {instance.event}. {loved_one.pronoun} has a personality type of {loved_one.personality} and {loved_one.pronoun} love language is {loved_one.love_language}. {loved_one.pronoun} likes {likes}. {loved_one.pronoun} name is {loved_one.name} but i love to use the pet name {loved_one.pet_name}",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
            
        
            data = response.get("choices")[0].get("text").strip()

            messages.append(Message(event=instance, to = loved_one, text=data))

        Message.objects.bulk_create(messages)
    
    
    

@receiver(post_save, sender=Message)
def create_more_message(sender, instance, created, **kwargs):
    
    event = instance.event
    
    if event.messages.filter(is_deleted=False, is_sent=False).count() <=1:
        
    
        loved_one = event.loved_one
        loved_one:LovedOneProfile
        messages=[]
        likes = ", ".join(loved_one.likes)
        
        
        for i in range(10):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"create a short sms for my {loved_one.relationship}. Today is {loved_one.pronoun} {instance.event}. {loved_one.pronoun} has a personality type of {loved_one.personality} and {loved_one.pronoun} love language is {loved_one.love_language}. {loved_one.pronoun} likes {likes}. {loved_one.pronoun} name is {loved_one.name} but i love to use the pet name {loved_one.pet_name} ",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
            
        
            data = response.get("choices")[0].get("text").strip()

            messages.append(Message(event=instance, to = loved_one, text=data))

        Message.objects.bulk_create(messages)