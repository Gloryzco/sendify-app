from rest_framework import serializers

from main.models import LovedOneProfile, Message, EventPreference, Subscription


class LovedOneProfileSerializer(serializers.ModelSerializer):
    
    messages = serializers.SerializerMethodField()
    event_preference = serializers.SerializerMethodField()
    
    class Meta:
        model = LovedOneProfile
        fields = "__all__"
        
        
    
    def get_messages(self, obj):
        return MessageSerializer(obj.messages.filter(is_deleted=False), many=True).data
    
    def get_event_preference(self, obj):
        return EventPreferenceSerializer(obj.preference.filter(is_deleted=False), many=True).data
    


class EventPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPreference
        fields = "__all__"
        
 
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"       
        
        

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"  
        
        
        

class SubscribeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields = ("payment_ref", "amount", "subscription_type",)
        