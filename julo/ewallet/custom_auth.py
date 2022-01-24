from .models import CustomUser

# requires to define two functions authenticate and get_user

class CustomAuth:
    def authenticate(self, request, customer_xid=None):
        print("authenticate", customer_xid)
        try:
            user = CustomUser.objects.get(id=customer_xid)
            return user

        except CustomUser.DoesNotExist:
            return None
        except Exception:
            return None

    def get_user(self, user_id):
        print("masuk")
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None