from celery import shared_task
from .models import EventPreference, get_current_subscription
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.helpers.vonage_api import sms
import time


def update_event(event):
    
    """Updates the event send date based on the frequency preference"""
    if event.frequency == "yearly":
        event.next_send_date =  timezone.now() + relativedelta(years=1)
    elif event.frequency == "daily":
        event.next_send_date =  timezone.now() + timezone.timedelta(days=1)
    elif event.frequency == "weekly":
        event.next_send_date =  timezone.now() + timezone.timedelta(weeks=1)
    elif event.frequency == "monthly":
        event.next_send_date =  timezone.now() + relativedelta(months=1)
    
    event.save()
    
    return
            
@shared_task
def send_scheduled_messages(): 
    today = timezone.now().date()
    today_event = EventPreference.objects.filter(next_send_date=today) 
    if today_event.count() > 0: 
        for event in today_event: 
            loved_one = event.loved_one
            
            current_sub = get_current_subscription(loved_one.user)
            
            if current_sub is None or current_sub.has_expired:
                #TODO: should notify user that message did not send
                
                # name = loved_one.user.first_name
                # receiver = loved_one.user.phone.as_e164
                # message_body = f"Hi, {name}\nToday is your {loved_one.relationship}'s {event.event} but we could not process your message because you don't have an active subscription."
                # sender="Doting App"
                
                
                # # notify
                
                # responseData = sms.send_message(
                #     {
                #         "from": "Doting App",
                #         "to": receiver,
                #         "text": message_body,
                #     }
                # )
                
                update_event(event=event)
                
                continue
            
            
            
            message = event.messages.filter(is_deleted=False, is_sent=False).first()
            
            if event.send_to_me:
                name = loved_one.user.first_name
                receiver = loved_one.user.phone.as_e164
                message_body = f"Hi, {name}\nToday is your {loved_one.relationship}'s {event.event}. A message will be sent to you to wish them well."
                sender="Doting App"
                
                
                # notify
                
                responseData = sms.send_message(
                    {
                        "from": "Doting App",
                        "to": receiver,
                        "text": message_body,
                    }
                )
                
                
                #add a little delay so the first sends before the other
                
                time.sleep(2)
                message_body = message.text
            else:
                receiver = loved_one.phone_number.as_e164
                message_body = message.text
                sender =  loved_one.user.phone.as_e164
                
            responseData = sms.send_message(
            {
                "from": sender,
                "to": receiver,
                "text": message_body,
            }
        )
            
            update_event(event=event)
            
            message.is_sent=True
            message.save()
            
            
            
