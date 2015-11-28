from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ItemForm, ImageForm
from .models import User, Item, Type, Image, Category
from django.http import Http404

def index(request):

	if not request.user.is_authenticated():
		return render(request, 'system/index2.html')

	if request.user.is_authenticated():
		return redirect('system.views.user_home')

def about(request):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)

		#if user is an admin
		if user.is_admin:
			return HttpResponse("You're an Admin")

		#if user is not an admin.
		elif not user.is_admin:
			types = Type.objects.all()
			return render(request, 'system/about.html', {'user': user, 'types': types})

	if not request.user.is_authenticated():
		return render(request, 'system/about.html')

#######################USER###############################################################
#######################USER###############################################################
#######################USER###############################################################
def user_add(request):

	try:
		if request.method == 'POST':

			fname = request.POST['fname']
			lname = request.POST['lname']
			contact_number = request.POST['contact_number']
			email = request.POST['email']
			password = request.POST['password']

			user = User.objects.create_user(email=email, password=password)
			user.first_name = fname
			user.last_name = lname
			user.contact_number = contact_number
			user.save()

			return redirect('system.views.user_login')

		else:
			form = UserForm()
	except:
		form = UserForm()
		return render(request, 'system/user_add.html', {'form': form})

	return render(request, 'system/user_add.html', {'form': form})

def user_login(request):

	if request.method == 'POST':

		try:
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user is not None and user.is_active:
				login(request, user)
				return redirect('system.views.user_home')

		except User.DoesNotExist:
			return redirect('system.views.user_login')

	elif request.user.is_authenticated():
		return redirect('system.views.user_home')

	return render(request, 'system/user_login.html')

def user_logout(request):

	logout(request)
	return redirect('system.views.user_login')

# if successfully log in, this function is called.
# the user is either admin or not admin
# different view for admin and not admin
def user_home(request):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)

		#if user is an admin
		if user.is_admin:
			return HttpResponse("You're an Admin")

		#if user is not an admin.
		elif not user.is_admin:
			types = Type.objects.all()
			categories = Category.objects.all()
			return render(request, 'system/user_home.html', {'user': user, 'types': types,
															 'categories': categories})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')

def user_view(request, user_pk):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		user_view_pk = User.objects.get(pk=user_pk)

		if user.is_admin:
			return HttpResponse("You're an Admin")

		elif not user.is_admin:
			types = Type.objects.all()
			return render(request, 'system/user_view.html', {'user': user,'user_view_pk':user_view_pk, 'types': types})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')

def user_update(request):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)

		if request.method == 'POST':

			form = UserForm(request.POST, instance=user)

			fname = request.POST['fname']
			lname = request.POST['lname']
			contact_number = request.POST['contact_number']
			email = request.POST['email']
			password = request.POST['password']

			if form.is_valid():
				user.first_name = fname
				user.last_name = lname
				user.contact_number = contact_number
				user.email = email
				user.set_password(password)
				user.save()
				return redirect('system.views.user_home')
			else:
				raise Http404
		else:
			form = UserForm(instance=user)
			types = Type.objects.all()
			return render(request, 'system/user_update.html', {'user': user, 'types': types})

	return redirect('system.views.user_login')

#######################USER###############################################################
#######################USER###############################################################
#######################USER###############################################################


#######################ITEM###############################################################
#######################ITEM###############################################################
#######################ITEM###############################################################
def item_add(request, type_pk):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		post_type = get_object_or_404(Type, pk=type_pk)

		if request.method == "POST":
			form = ItemForm(request.POST)
			form_image = ImageForm(request.POST, request.FILES)

			if form.is_valid() and form_image.is_valid():
				#saving the form to image and item image
				item = form.save()
				item_image = form_image.save()

				item.save()
				item_image.save()

				item.post_date = timezone.now()
				#get the user. instance
				item_user = User.objects.get(id=user.pk)
				#get the type. instance
				item_type = Type.objects.get(id=post_type.pk)
				#save the Item attribute(user_id) as the id of the selected user
				item.user_id = item_user
				#save the Item attribute(user_id) as the id of the selected user
				item.type_id = item_type
				item.save()

				#setting the image
				#get the item instance
				this_item = Item.objects.get(id=item.pk)
				item_image.title = item.name
				item_image.item_id = this_item
				item_image.save()
				return redirect('system.views.user_home')

			else:
				print form.errors
				raise Http404

		else:
			form = ItemForm()
			categories = Category.objects.all()
			types = Type.objects.all()
			return render(request, 'system/item_add.html', {'form': form, 'categories': categories, 
															'types': types, 'post_type': post_type})


	return redirect('system.views.user_login')

def item_browse(request):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().order_by('post_date')

		if user.is_admin:
			return HttpResponse("You're an Admin")

		elif not user.is_admin:
			types = Type.objects.all()
			categories = Category.objects.all()
			return render(request, 'system/item_browse.html', {'user': user, 'types': types, 
															 'items': items, 'categories':categories})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')


def item_browse_bytype(request, type_pk):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().filter(type_id=type_pk).order_by('post_date')

		if user.is_admin:
			return HttpResponse("You're an Admin")

		elif not user.is_admin:
			types = Type.objects.all()
			categories = Category.objects.all()
			return render(request, 'system/item_browse.html', {'user': user, 'types': types, 
															 'items': items})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')

#this method display the item (from browse) of the selected item.
def item_view(request, item_pk):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		item = get_object_or_404(Item, pk=item_pk)

		if user.is_admin:
			return HttpResponse("You're an Admin")

		elif not user.is_admin:
			types = Type.objects.all()
			image = get_object_or_404(Image, item_id=item_pk)
			return render(request, 'system/item_view.html', {'user': user, 'types': types, 
															 'item': item, 'image': image})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')


def item_of_user(request):
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().filter(user_id=user)
		images = Image.objects.all().filter(item_id=items)

		if user.is_admin:
			return HttpResponse("You're an Admin")

		elif not user.is_admin:
			types = Type.objects.all()
			return render(request, 'system/item_of_user.html', {'items': items, 'images': images,
																'types': types})

	if not request.user.is_authenticated():
		return redirect('system.views.user_login')
#######################ITEM###############################################################
#######################ITEM###############################################################
#######################ITEM###############################################################