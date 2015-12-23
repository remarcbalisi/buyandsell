from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ItemForm, ImageForm, CommentForm, CategoryForm
from .models import User, Item, Type, Image, Category, Comment, Ranking
from django.http import Http404
from django.contrib.auth.decorators import login_required

def index(request):
	if request.user.is_authenticated():
		return redirect('system.views.user_home')

	else:
		items = Item.objects.all().order_by('ranking_id')
		return render(request, 'system/index3.html', {'items':items})

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
		if request.user.is_authenticated() and request.user.is_admin and request.method == 'POST':

			fname = request.POST['fname']
			lname = request.POST['lname']
			contact_number = request.POST['contact_number']
			email = request.POST['email']
			password = request.POST['password']

			try:
				user2 = User.objects.create_superuser(email=email, password=password)
				success = "User %s %s successfully added!" %(fname, lname)
				return render(request, 'system/admin/user_add.html', {'success':success})

			except:
				exist = "User with email %s already exist" %(email)
				return render(request, 'system/admin/user_add.html', {'exist':exist})

		elif request.method == 'POST':

			fname = request.POST['fname']
			lname = request.POST['lname']
			contact_number = request.POST['contact_number']
			email = request.POST['email']
			password = request.POST['password']

			try:
				user = User.objects.create_user(email=email, password=password)
				user.first_name = fname
				user.last_name = lname
				user.contact_number = contact_number
				user.save()
				return redirect('system.views.user_login')

			except:
				exist = "User with email %s already exist" %(email)
				return render(request, 'system/user_add.html', {'exist':exist})

		elif request.user.is_authenticated() and request.user.is_admin:
			return render(request, 'system/admin/user_add.html')

		elif request.user.is_authenticated():
			return redirect('system.views.user_home')

		else:
			return render(request, 'system/user_add.html')

	except KeyError:
		return render(request, 'system/error.html')

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
			exist = "Wrong password or email"
			return render(request, 'system/user_login.html', {'exist':exist})

	elif request.user.is_authenticated():
		return redirect('system.views.user_home')

	return render(request, 'system/user_login.html')

def user_logout(request):

	logout(request)
	success = "successfully logged out!"
	return render(request, 'system/user_login.html', {'success':success})

# if successfully log in, this function is called.
# the user is either admin or not admin
# different view for admin and not admin
@login_required
def user_home(request):
	user = User.objects.get(pk=request.user.id)

	#if user is an admin
	if user.is_admin:
		types = Type.objects.all()
		categories = Category.objects.all()
		user_count = User.objects.all().count()
		post_count = Item.objects.all().count()
		items = Item.objects.all().order_by('ranking_id')
		return render(request, 'system/admin/user_home.html', {'user': user, 'types': types,
														 'categories': categories, 'user_count':user_count, 'post_count':post_count, 'items':items})

	#if user is not an admin.
	elif not user.is_admin:
		types = Type.objects.all()
		categories = Category.objects.all()
		items = Item.objects.all().order_by('-ranking_id')
		return render(request, 'system/user_home.html', {'user': user, 'types': types,
														 'categories': categories, 'items':items})

@login_required
def user_view(request, user_pk):

	user = User.objects.get(pk=user_pk)
	this_user = User.objects.get(pk=request.user.pk)

	if this_user.is_admin:
		return render(request, 'system/admin/user_view.html', {'user': user})

	elif not this_user.is_admin:
		types = Type.objects.all()
		return render(request, 'system/user_view.html', {'user': user, 'types': types})

@login_required
def user_update(request):

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
			exist = "category failed to update!"

			if user.is_admin:
				return render(request, 'system/admin/user_update.html', {'exist':exist})

			elif not user.is_admin:
				return render(request, 'system/user_update.html', {'exist':exist})

	elif user.is_admin:
		types = Type.objects.all()
		return render(request, 'system/admin/user_update.html', {'user': user, 'types': types})

	else:
		types = Type.objects.all()
		return render(request, 'system/user_update.html', {'user': user, 'types': types})


#######################USER###############################################################
#######################USER###############################################################
#######################USER###############################################################


#######################ITEM###############################################################
#######################ITEM###############################################################
#######################ITEM###############################################################
@login_required
def item_add(request, type_pk):

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

			#create ranking of items
			rank = Ranking.objects.create(item_rank=timezone.now())
			item.ranking_id = rank
			item.save()

			#setting the image
			#get the item instance
			this_item = Item.objects.get(id=item.pk)
			item_image.title = item.name
			item_image.item_id = this_item
			item_image.save()
			return redirect('system.views.item_of_user')

		else:
			print form.errors
			raise Http404

	else:
		form = ItemForm()
		categories = Category.objects.all()
		types = Type.objects.all()
		return render(request, 'system/item_add.html', {'form': form, 'categories': categories, 
														'types': types, 'post_type': post_type})

@login_required
def item_update(request, item_pk):

	item = get_object_or_404(Item, pk=item_pk)
	user = User.objects.get(pk=request.user.id)
	image = get_object_or_404(Image, item_id=item)

	if request.method == "POST":
		form = ItemForm(request.POST, instance=item)
		form_image = ImageForm(request.FILES, instance=image)

		if form.is_valid() and form_image.is_valid():
			model = form.save(commit=False)
			image = form_image.save(commit=False)

			model.post_date = timezone.now()
			model.save()
			image.save()
			image.item_id = model
			image.save()

			rank = Ranking.objects.create(item_rank=timezone.now())
			model.ranking_id = rank
			model.save()
			return redirect('system.views.user_home')

		else:
			print form.errors
			raise Http404

	else:
		categories = Category.objects.all()
		types = Type.objects.all()
		form = ItemForm(instance=item)
		image_form = ImageForm(instance=image)
		return render(request, 'system/item_update.html', {'categories': categories, 
														'types': types, 'image':image, 'item':item, 'form':form, 'image_form':image_form})

@login_required
def item_delete(request, item_pk):
	try:
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().filter(user_id=user)
		images = Image.objects.all().filter(item_id=items)
		item = get_object_or_404(Item, pk=item_pk)
		image = get_object_or_404(Image, item_id=item)
		image.delete()
		item.delete()
		success = "Item deleted!"
		types = Type.objects.all()
		return render(request, 'system/item_of_user.html', {'items': items, 'images': images,
																	'types': types, 'types':types, 'success':success})

	except:
		return redirect('system.views.item_of_user')

def item_browse(request):

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().order_by('-ranking_id')

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

	user = User.objects.get(pk=request.user.id)
	items = Item.objects.all().filter(type_id=type_pk).order_by('-ranking_id')
	categories = Category.objects.all()

	if user.is_admin:
		return redirect('system.views.user_home')

	elif not user.is_admin:
		types = Type.objects.all()
		categories = Category.objects.all()
		return render(request, 'system/item_browse.html', {'user': user, 'types': types, 
														 'items': items, 'categories':categories})

def item_browse_bycategory(request, category_pk):

	user = User.objects.get(pk=request.user.id)
	items = Item.objects.all().filter(category_id=category_pk).order_by('-ranking_id')
	category = get_object_or_404(Category, pk=category_pk)
	categories = Category.objects.all()

	if user.is_admin:
		return redirect('system.views.user_home')

	elif not user.is_admin:
		types = Type.objects.all()
		categories = Category.objects.all()
		return render(request, 'system/item_browse.html', {'user': user, 'types': types, 
														 'items': items, 'category':category, 'categories':categories})

#this method display the item (from browse) of the selected item.
@login_required
def item_view(request, item_pk):

	user = User.objects.get(pk=request.user.id)
	users = User.objects.all()
	item = get_object_or_404(Item, pk=item_pk)
	comments = Comment.objects.all().filter(item_id=item_pk).order_by('-post_comment')

	if request.method == 'POST':
		form = CommentForm(request.POST)
		print "request is post"

		if form.is_valid():
			comment = form.save()
			comment.save()
			comment.item_id = item
			comment.user_id = user
			comment.publish()
			comment.save()
			rank = Ranking.objects.create(item_rank=timezone.now())
			item.ranking_id = rank
			item.save()

			types = Type.objects.all()
			image = get_object_or_404(Image, item_id=item_pk)
			return render(request, 'system/item_view.html', {'user': user, 'types': types, 
														 	 'item': item, 'image': image,
														 	 'comments': comments,
														 	 'users': users})

	if user.is_admin:
		return redirect('system.views.user_home')

	elif not user.is_admin:
		types = Type.objects.all()
		image = get_object_or_404(Image, item_id=item_pk)
		return render(request, 'system/item_view.html', {'user': user, 'types': types, 
														 'item': item, 'image': image,
														 'comments': comments,
														 'users': users})

@login_required
def item_of_user(request):
		user = User.objects.get(pk=request.user.id)
		items = Item.objects.all().filter(user_id=user)
		images = Image.objects.all().filter(item_id=items)

		if user.is_admin:
			return redirect('system.views.user_home')

		elif not user.is_admin:
			types = Type.objects.all()
			return render(request, 'system/item_of_user.html', {'items': items, 'images': images,
																'types': types})
#######################ITEM###############################################################
#######################ITEM###############################################################
#######################ITEM###############################################################

@login_required
def category_add(request):
	if request.method == 'POST' and request.user.is_admin:
		form = CategoryForm(request.POST)
		category_name = request.POST['name']
		check_category = Category.objects.all().filter(name=category_name)

		if len(check_category) == 0:
			if form.is_valid():
				category = form.save()
				category.save()
				success = "Category %s successfully added!" %(category_name)
				return render(request, 'system/admin/category_add.html', {'success':success})

			else:
				exist = "category %s failed to add!" %(category_name)
				return render(request, 'system/admin/category_add.html', {'exist':exist})

		if len(check_category) > 0:
			exist = "category %s already exist!" %(category_name)
			return render(request, 'system/admin/category_add.html', {'exist':exist})

	elif not request.method == 'POST' and request.user.is_admin:
		return render(request, 'system/admin/category_add.html')

	else:
		return redirect('system.views.user_home')

@login_required
def category_view(request):
	if request.user.is_admin:
		categories = Category.objects.all()
		return render(request, 'system/admin/category_view.html', {'categories':categories})

	else:
		redirect('system.views.user_home')

@login_required
def category_delete(request, category_pk):
	try:
		if request.user.is_admin:
			categories = Category.objects.all()
			category = get_object_or_404(Category, pk=category_pk)
			category.delete()
			success = "Category deleted!"
			return render(request, 'system/admin/category_view.html', {'categories':categories, 'success':success})

		else:
			redirect('system.views.user_home')

	except:
		return redirect('system.views.item_of_user')