from django.core.checks import messages
from django.shortcuts import redirect, render
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse



# Create your views here.
@csrf_exempt
def create_user(request):
	if request.method == 'GET':
		custom_user = CustomUser.objects.all()
		serializer = CustomUserSerializer(custom_user, many=True)
		return JsonResponse(serializer.data, safe=False)


	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CustomUserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def update_user(request, pk):
	#retrieve update and delete a code snippet
	try:
		profile = CustomUser.objects.get(pk=pk)
	except CustomUser.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CustomUserSerializer(profile)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data =  JSONParser().parser(request)
		serializer = CustomUserSerializer(profile, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		profile.delete()
		return HttpResponse(status=204)



def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = auth.authenticate(email=email, password=password)

		if user is not None:
			auth.login(request, user)

			return redirect('/')

		else: 
			messages.info(request, 'Invalid Credentials')
			return redirect('login')

	else:
		return render(request)



def logout(request):
	auth.logout(request)
	return redirect('login')	