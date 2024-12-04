

        


from django.conf import settings
import requests




class FlutterWave:
    def __init__(self):
        # Hardcoded keys for debugging
        self.public_key = "FLWPUBK_TEST-9fdb696e6231ed66705c0838462ddf5a-X"
        self.secret_key = "FLWSECK_TEST-60ac8e059e21962e517ce2b17065dda2-X"
        self.base_url = "https://api.flutterwave.com/v3"

    def create_checkout_url(self, payment):
        """
        Creates a checkout URL for Flutterwave payment.
        """
        url = f"{self.base_url}/payments"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "tx_ref": payment.tx_ref,
            "amount": payment.amount,
            "currency": payment.currency,
            "redirect_url": f"https://bd34-102-67-16-3.ngrok-free.app/flutterwave/v1/verify-payment/{payment.tx_ref}",
            "customer": {
                "email": payment.email,
                "phone_number": payment.customer_phone,
                "name": payment.customer_name,
            },
            "customizations": {
                "title": "Payment for Your Order",
                "logo": "",
            }
        }

        print(f"Sending request to Flutterwave: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("status") == "success":
                    return response_data["data"]["link"]
                else:
                    raise Exception(f"Error creating checkout: {response_data.get('message')}")
            else:
                raise Exception(f"Error creating checkout: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise Exception(f"Error creating checkout: {e}")

    def verify_payment(self, tx_ref, transaction_id):
        """
        Verifies the payment status by transaction reference and transaction ID.
        """
        verify_url = f"{self.base_url}/transactions/{transaction_id}/verify"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(verify_url, headers=headers)
            print(f"Verify Payment Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("status") == "success" and response_data["data"].get("status") == "successful":
                    return True, response_data["data"]
                else:
                    return False, response_data["data"]
            else:
                return False, response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False, {"error": str(e)}

