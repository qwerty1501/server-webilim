import json
import uuid

import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.conf import settings
import json
import simplejson


MERCHANT_ID = settings.MERCHANT_ID
PAY_SECRET_KEY = settings.PAY_SECRET_KEY

BASE_URL = settings.BASE_URL
CALLBACK_BASE_URL = settings.CALLBACK_BASE_URL


def get_url(user_data=None, course=None, discount_price=None) -> str:
    if discount_price:
        price = simplejson.dumps(discount_price)
    else:
        price = simplejson.dumps(user_data.package_membership.price)
    data = {
        "order": f"{user_data.id}",
        "amount": price,
        "currency": "KGS",
        "description": f'{user_data}',
        "language": "ru",
        # "payment_system": payment_system,
        "options": {
            "callbacks": {
                "result_url": CALLBACK_BASE_URL + "/api/v1/purchases/payment_response/",
                "check_url": CALLBACK_BASE_URL,
                "cancel_url": CALLBACK_BASE_URL,
                # "success_url": CALLBACK_BASE_URL + f"/user/checkout/?status=success&order={user_data.id}",
                # "failure_url": CALLBACK_BASE_URL + f"/user/checkout/?status=error&order={user_data.id}",
                "success_url": CALLBACK_BASE_URL,
                "failure_url": CALLBACK_BASE_URL,
                "back_url": CALLBACK_BASE_URL,
                "capture_url": CALLBACK_BASE_URL
            }
        }
    }
    response = requests.post(BASE_URL + "v4/payments",
                             json=data,
                             auth=(MERCHANT_ID, PAY_SECRET_KEY),
                             headers={'X-Idempotency-Key': f'{user_data.id}'}
                             )
    if response.status_code != status.HTTP_201_CREATED:
        raise ValidationError({"message": "Ошибка при запросе PayBox"})
    data = json.loads(response.content)
    if not course:
        user_data.payment_url = user_data.payment_url if user_data.payment_url else data['payment_page_url']
        user_data.payment_id = user_data.payment_id if user_data.payment_id else data.get('id', None)
        user_data.paid_price = price
        user_data.type = user_data.package_membership.get_type_display()
        user_data.save()
    return data


def get_payment_info(payment_id: str) -> dict:
    response = requests.get(BASE_URL + f"v4/payments/{payment_id}",
                            auth=('534869', 'PewoawvojgOjlbtV'),
                            headers={'X-Idempotency-Key': f'{str(uuid.uuid4())}'}
                            )
    if response.status_code != status.HTTP_200_OK:
        raise ValidationError({"message": "Ошибка при запросе PayBox " + str(response.status_code)})

    data = json.loads(response.content)

    return data


def cancel_payment(purchase):
    response = requests.post(BASE_URL + f"payments/{purchase.payment_id}/cancel",
                             json={},
                             auth=('534869', 'PewoawvojgOjlbtV'),
                             headers={'X-Idempotency-Key': f'{purchase.uuid}'}
                             )
    data = json.loads(response.content)

    return data.get('code', None)



# for callback
"""
:arg response dict {'id': 426151639, 'status': {'code': 'success'}, 
'order': '62', 'amount': '20900.00', 'refund_amount': '0.00', 'currency': 'KGS', 
'description': 'Оплата товаров симпл', 'payment_system': 'EPAYWEBKGS', 
'expires_at': '2021-02-10T05:10:53Z', 'created_at': '2021-02-09T11:10:53Z', 
'updated_at': '2021-02-09T11:11:26Z', 
'param1': None, 'param2': None, 'param3': None, 
'options': {'callbacks': {'result_url': 'https://simple.kg/api/v1/purchases/payment_response/', 
'check_url': 'https://simple.kg', 'success_url': 'https://simple.kg/purchase/success', 
'failure_url': 'https://simple.kg/purchase/failure', 'back_url': 'https://simple.kg', 
'cancel_url': 'https://simple.kg'}, 
'user': {'email': 'luckyweqer@gmail.com', 'phone': '996500369152'}, 'receipt_positions': None}}
"""
from django.shortcuts import get_object_or_404

# from application.payment.models import PaymentHistory
# from application.purchase.models import Purchase


# def result_handler(response: dict) -> PaymentHistory:
#     purchase_id = response['order']
#     purchase = get_object_or_404(Purchase, pk=purchase_id)

#     if response['status']['code'] != 'success':
#         data = {
#             "error": True,
#             "error_message": "error",  # TODO check error body response
#             "transaction_id": response['id'],
#         }
#     else:
#         data = {
#             "purchase": purchase,
#             "amount": int(response['amount']),
#             "transaction_id": response['id'],
#         }
#     purchase.payment_status = response['status']['code']
#     purchase.save()

#     return PaymentHistory.objects.create(**data)