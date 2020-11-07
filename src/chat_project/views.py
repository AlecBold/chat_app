from django.http import HttpResponse


def test(request):
    html = "<html><p>hi</p></html>"
    return HttpResponse(html)
