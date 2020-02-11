from django.shortcuts import render
import requests
import json
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def log_search(request):
    return render(request, "SRM/srm-index.html")


@login_required()
def search_result(request):
    cookies = {
        'warehouse': '',
        'token': ""
    }
    data = request.POST.dict()
    object_type = data['object_type']
    object_id = data["object_id"]
    params = {
        "object_type": object_type,
        "object_id": object_id
    }
    r = requests.get(
        "",
        cookies=cookies,
        params=params
    )
    res = r.json()
    context = json.dumps(res, indent=4, ensure_ascii=False)
    return render(request, "SRM/srm-index.html", {"context": context})
print()
