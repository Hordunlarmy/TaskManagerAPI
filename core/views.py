import socket

from django.http import JsonResponse


def ping(request):
    hostname = socket.gethostname()
    return JsonResponse({"message": f"Hi!, I am {hostname} and I am alive."})


def api_ping(request):
    hostname = socket.gethostname()
    return JsonResponse({"message": f"Hi!, I am {hostname} and I am alive."})
