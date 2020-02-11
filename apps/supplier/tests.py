import requests
import json
# Create your tests here.
def search_result(request, *args, **kwargs):
    data = request.POST.dict()
    object_type = data['object_type']
    object_id = data["object_id"]
    params = {
        "object_type": object_type,
        "object_id": object_id
    }
    cookies = {
        'warehouse': '',
        'token': ""
    }
    r = requests.get(
        "",
        cookies=cookies,
        params=params
    )
    context = r.json()
    return context



if __name__ == '__main__':
    search_result("object_type", "object_id")


# if __name__ == '__main__':
#     test("20", "14451043")
