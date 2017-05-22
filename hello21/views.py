import sys
import hashids
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from hello21 import settings
from hello21.models import Token


hasher = hashids.Hashids(salt=settings.HASHIDS_SALT, min_length=5)

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@api_view(['GET'])
@payment.required(100)
def buy(request):
    print(request)
    new_token = Token.objects.create()
    new_token.value = hasher.encode(new_token.id)
    new_token.save()

    return JsonResponse({'token': new_token.value}, status=200)


def _redeem(token):
    try:
        requested_token = Token.objects.get(value=token)
        if requested_token.redeemed:
            raise ValueError()
    except ObjectDoesNotExist:
        logger.error('User requested token {} that does not exist'.format(token))
        return JsonResponse({'success': False, 'error': 'Invalid or redeemed token.'}, status=400)
    except ValueError:
        logger.error('User requested token {} that was already redeemed.'.format(token))
        return JsonResponse({'sucess': False, 'error': 'Redeemed token.'}, status=400)

    requested_token.redeemed = True
    requested_token.save()

    return JsonResponse({'success': True, 'message': "Thanks!"}, status=200)


def get_redeemed_price(request):
    try:
        token = request.data['token']
    except:  # noqa
        return JsonResponse({'error': 'POST data must include "token"'}, status=400)

    try:
        requested_token = Token.objects.get(token.value)
        if requested_token.redeemed:
            raise ValueError()
    except:  # noqa
        return 100

    return 0


@api_view(['POST'])
@payment.required(get_redeemed_price)
def redeem(request):
    try:
        token = request.data['token']
    except KeyError:
        return JsonResponse({'error': 'POST data must include "token"'}, status=400)
    return _redeem(token)
