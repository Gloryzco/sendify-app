from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import phonenumbers

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if phone:
            try:
                user = UserModel.objects.get(phone=phone.as_e164)
            except UserModel.DoesNotExist:
                return None

            # Verify the password (you may use other authentication mechanisms)
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def clean_phone_number(self, phone):
        try:
            parsed_number = phonenumbers.parse(phone, None)
        except phonenumbers.NumberParseException:
            return None

        if not phonenumbers.is_possible_number(parsed_number) or \
           not phonenumbers.is_valid_number(parsed_number):
            return None

        # Format the phone number in E.164 format
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
