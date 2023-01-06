import requests
import urllib.parse
from django.conf import settings
from django.http import HttpResponseRedirect

class BasePaymentAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def _make_request(self, method, endpoint, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Handle network errors and HTTP errors with status codes >= 400
            raise PaymentAPIError(f"An error occurred while making the request: {e}") from e
    
    def get(self, endpoint, params=None):
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint, data):
        return self._make_request("POST", endpoint, json=data)
    
    def put(self, endpoint, data):
        return self._make_request("PUT", endpoint, json=data)
    
    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)
    
    def calculate_tax(self, amount, tax_rate):
        return amount * tax_rate
    
    def apply_discount(self, amount, discount_rate):
        return amount * (1 - discount_rate)
    
    def charge(self, amount):
        # Make a charge request to the payment API
        pass
    
    def refund(self, charge_id, amount=None):
        # Make a refund request to the payment API
        pass
    
    def get_payment_status(self, payment_id):
        # Make a request to the payment API to get the status of a payment
        pass

class PaymentAPIError(Exception):
    pass

class PayPalAPI(BasePaymentAPI):
    def __init__(self, client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET, redirect_uri=settings.PAYPAL_CLIENT_URI):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = "https://api.paypal.com/v1/oauth2/token"
        self.auth_url = "https://www.paypal.com/signin/authorize"
    
    def authenticate(self, request):
        auth_code = request.GET.get("code")
        if auth_code:
            # Exchange the authorization code for an access token
            data = {
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            response = requests.post(self.token_url, data=data)
            if response.status_code == 200:
                access_token = response.json()["access_token"]
                # Save the access token to the user's profile
                request.user.paypal_access_token = access_token
                request.user.save()
                return HttpResponseRedirect("/payments/success")
            else:
                # Handle error response from PayPal
                pass
        else:
            # Redirect the user to PayPal's authorization endpoint
            params = {
                "client_id": self.client_id,
                "response_type":"code",
                "redirect_uri": self.redirect_uri,
                "scope": "https://uri.paypal.com/services/payments/futurepayments",
            }
            url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
            return HttpResponseRedirect(url)                   
                    
class MpesaAPI(BasePaymentAPI):
    def __init__(self):
        super().__init__(base_url="https://api.mpesa.com", api_key="your_mpesa_api_key")

class PrepaidCardAPI(BasePaymentAPI):
    def __init__(self):
        super().__init__(base_url="https://api.prepaidcard.com", api_key="your_prepaid_card_api_key")
        

'''
paypal = PayPalAPI()

try:
    amount = 100
    tax_rate = 0.15
    total_amount = paypal.calculate_tax(amount, tax_rate) + amount
    discount_rate = 0.10
    final_amount = paypal.apply_discount(total_amount, discount_rate)
    charge_response = paypal.charge(final_amount)
    charge_id = charge_response["id"]
    refund_response = paypal.refund(charge_id)
    payment_status = paypal.get_payment_status(charge_id)
except PaymentAPIError as e
    # Handle payment API errors
    print(f"An error occurred while making a payment: {e}")

# Another Example

'''