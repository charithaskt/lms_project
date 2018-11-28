from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.utils import json

from custom_user_model import settings
from payment import Checksum
from payment.Checksum import generate_checksum, verify_checksum, generate_checksum_by_str, verify_checksum_by_str
from intranet import models
from intranet.models import Borrowers

@csrf_exempt
def pay(request):

    merchantMid = settings.PAYTM_MERCHANT_ID
    merchantKey = settings.PAYTM_MERCHANT_KEY
    order_id = Checksum.__id_generator__()
    channelId = 'WEB'
    custId = "dfsvfdc"
    txnAmount = '1000'
    website = 'WEBSTAGING'
    industryTypeId = 'Retail'
    callbackUrl = settings.HOST_URL + settings.PAYTM_CALLBACK_URL

    paytmParams = {
        'MID': merchantMid,
        'ORDER_ID': order_id,
        'CUST_ID':custId,
        'INDUSTRY_TYPE_ID': industryTypeId,
        'CHANNEL_ID':channelId,
        'TXN_AMOUNT': txnAmount,
        'WEBSITE':website,
        'CALLBACK_URL': callbackUrl,

    }

    paytmChecksum = generate_checksum(paytmParams, merchantKey)
    print(paytmChecksum)

    paytmParams['CHECKSUMHASH'] = paytmChecksum

    context = {'paytmDict': paytmParams}
    return render(request, 'payment/form1.html', context)




@csrf_exempt
def check(request):


    merchantKey = settings.PAYTM_MERCHANT_KEY

    if request.method == 'POST':

        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]

        print(data_dict)

        if 'CHECKSUMHASH' in data_dict.keys():

            paytmChecksum = request.POST['CHECKSUMHASH']

        else:
            paytmChecksum = ''



        isValidChecksum = verify_checksum_by_str(data_dict, merchantKey, paytmChecksum)

        context = {'paytmDict': data_dict}
        if (isValidChecksum):
            return render(request, 'payment/form2.html', context)
        else:
            return HttpResponse("checksum verify failed")
    else:

        return HttpResponse(status= 200)


def status(request):
    return render(request, 'payment/status.html')