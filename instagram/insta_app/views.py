from django.shortcuts import render
from django.http import JsonResponse, response
from django.contrib.auth.models import User
from .models import Album,Picture,Caption, Pos,Similarity
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html', {})


# To view all albums
def albums(request,username):


    # Creates a new album if method is 'POST'
    if request.method == 'POST':
        title = request.POST['title']
        tag = request.POST['tag']
        
        try:
            # Creates album for the  given user
            user = User.objects.get(username=username)
            album = Album(title=title,creator=user)
            album.save()
            
            # Adds tag to the album
            if not tag is None:
                album.tags.add(tag)
                album.save()

        #  if user doesnt exist
        except User.DoesNotExist as e:
            status= 404
            message= "Please register user for proceeding"
            return JsonResponse({'message': message}, status=status)

        #  Internal server errors
        except Exception as e:
            status= 500
            message= "Something went wrong. Please try again later."
            return JsonResponse({'message': message}, status=status) 

        # success message
        return JsonResponse({'message':'album created',
                            'title' : album.title,
                            })


    # If method is 'GET'
    # Displays titles of all albums of the user 
    
    try:
        user = User.objects.get(username=username)
            
        # Set up pagination
        p = Paginator(user.album_set.all(),10)
        page = request.GET.get('page')
        albums = p.get_page(page)

    #  if user doesn't exist   
    except User.DoesNotExist as e:
        status= 404
        message= "Please register user for proceeding"
        return JsonResponse({'message': message}, status=status)

    # Cathches all other exceptions  
    except Exception as e:
        status= 500
        message= "Something went wrong. Please try again later."
        return JsonResponse({'message': message}, status=status) 

    response = []
    # Returns all album titles 
    for album in albums:
            
        response.append({
            'title': album.title,
                    
        }
        )
    return JsonResponse(response, safe=False)

    

# To view all published albums
def published_albums(request,username):
    try:
        user = User.objects.get(username=username)
        
        # Set up pagination
        p = Paginator(user.album_set.filter(published=True).all(),10)
        page = request.GET.get('page')
        albums = p.get_page(page)

    # If user doesn't exist
    except User.DoesNotExist as e:
        status= 404
        message= "Please register user for proceeding"
        return JsonResponse({'message': message}, status=status)

    # Cathches all other exceptions   
    except Exception as e:
        status= 500
        message= "Something went wrong. Please try again later."
        return JsonResponse({'message': message}, status=status) 

    #  Returns all published album titles
    response = []
    for album in albums:
        response.append({
            'title': album.title,
                
        }
        )
    return JsonResponse(response, safe=False)


# To publish an album
def publish_album(request,username,title):
    
    try:
        user = User.objects.get(username=username)
        albums = user.album_set.all()
        album = albums.filter(title=title).first()
       
        # If album doesn't exist
        if album is None:
            status= 404
            message= "Album does not exist"
            return JsonResponse({'message': message}, status=status)
        
        # Publishes album
        album.published = True
        album.save()
    
    # If user doesn't exist
    except User.DoesNotExist as e:
        status= 404
        message= "Please register user for proceeding"
        return JsonResponse({'message': message}, status=status)

    # Catches all otehr exceptions
    except Exception as e:
        status= 500
        message= "Something went wrong. Please try again later."
        return JsonResponse({'message': message}, status=status) 
    
    # Returns success message
    return JsonResponse({'message':'album  published'})



# To add new photo to album
def add_photo(request,username,title):
    
    # Adds a new photo to the album if method is 'POST'
    if request.method == 'POST':

        image = request.FILES.get('image')
        caption = request.POST['caption']
        font_color = request.POST['font_color']
        position = request.POST['position']
        top = request.POST['top']
        bottom = request.POST['bottom']
        right = request.POST['right']
        left = request.POST['left']

        try:  
            user = User.objects.get(username=username)
            albums = user.album_set.all()
            album = albums.filter(title=title).first()
                
            # If album doesn't exist
            if album is None:
                status= 404
                message= "Album does not exist"
                return JsonResponse({'message': message}, status=status)
                
            # New picture created
            picture = Picture(image=image,album=album)
            picture.save()
            message = "Photo added"

            # If picture caption is given
            if not caption == "":
                caption = Caption(title=caption,font_color=font_color,picture=picture)
                caption.save()
                pos = Pos(caption=caption)

                # If  position attributes are given
                if not position == "":
                    pos.position = position
                    pos.top = top
                    pos.bottom = bottom
                    pos.right = right
                    pos.left = left
                                    
                pos.save()

        # If user doesn't exist
        except User.DoesNotExist as e:
            status= 404
            message= "Please register user for proceeding"
            return JsonResponse({'message': message}, status=status) 
            
        # Catches all other errors
        except Exception as e:
            status= 500
            message= "Something went wrong. Please try again later."
            return JsonResponse({'message': message}, status=status) 

        # Returns Picture ID of the newly created resource
        return JsonResponse({'message': message,
                            'picture_id':picture.image_id}) 
      


# To add new hashtag to album
def add_hashtag(request,username,title):
    
    if request.method == 'POST':
        tag = request.POST['tag']
    
        try:
            user = User.objects.get(username=username)
            albums = user.album_set.all()
            album = albums.filter(title=title).first()
            
            # If album doesn't exist
            if album is None:
                status= 404
                message= "Album does not exist"
                return JsonResponse({'message': message}, status=status)
            
            # Saves hashtag
            album.tags.add(tag)
            album.save()
       
        #   If user doesn't exist
        except User.DoesNotExist as e:
            status= 404
            message= "Please register user for proceeding"
            return JsonResponse({'message': message}, status=status)
        
        # Catches all other exceptions
        except Exception as e:
            status= 500
            message= "Something went wrong. Please try again later."
            return JsonResponse({'message': message}, status=status) 
            
        return JsonResponse({'message':'New tag added'})


# Display contents of an particular album
def display_album(request,username,title):
   
    try:
        user = User.objects.get(username=username)
        albums = user.album_set.all()
        album = albums.filter(title=title).first()
       
        #  Returns error if album doesn't exist 
        if album is None:
            status= 404
            message= "Album does not exist"
            return JsonResponse({'message': message}, status=status)

        # Sets up pagination
        p = Paginator(album.picture_set.all(),10)
        page = request.GET.get('page')
        pictures = p.get_page(page)
    
    # If user doesn't exist
    except User.DoesNotExist as e:
        status= 404
        message= "Please register user for proceeding"
        return JsonResponse({'message': message}, status=status)

    # Catches all other exceptions  
    except Exception as e:
        status= 500
        message= "Something went wrong. Please try again later."
        return JsonResponse({'message': message}, status=status) 
    
    # Returns details of all pictures in the album
    response = []
    for picture in pictures:
        picture_details = {}
        picture_details['url'] = picture.image.url
        picture_details['date_created'] =picture.date_created
        
        # If picture caption not set, redirect
        try:
            picture_details['caption'] = picture.caption.title
            picture_details['font_color'] = picture.caption.font_color
            picture_details['position'] = picture.caption.pos.position
            picture_details['top'] = picture.caption.pos.top
            picture_details['bottom'] = picture.caption.pos.bottom
            picture_details['left'] = picture.caption.pos.left
            picture_details['right'] = picture.caption.pos.right
            response.append(picture_details)
        
        except AttributeError as e:
            response.append(picture_details)
    return JsonResponse(response, safe=False)   



# To view users with similar interest
def similar_users(request,username):
    try:
        user = User.objects.get(username=username)
        response = []
        
         # Sets up pagination
        p = Paginator(Similarity.objects.filter(user=user).all(),10)
        page = request.GET.get('page')
        similarities = p.get_page(page)

    # If user doesn't exist
    except User.DoesNotExist as e:
        status= 404
        message= "Please register user for proceeding"
        return JsonResponse({'message': message}, status=status)

    # Catches all other exceptions 
    except Exception as e:
        status= 500
        message= "Something went wrong. Please try again later."
        return JsonResponse({'message': message}, status=status) 
    
    # Returns similar-user details if similarity score greater than 10
    for similarity in similarities:
        if similarity.score > 10:
            response.append(similarity.similar_user.username)
    return JsonResponse(response, safe=False)


# To delete a photo
def delete_photo(request,username,title,image_id):
    
    if request.method == 'DELETE':
        try:
            user = User.objects.get(username=username)
            album = user.album_set.filter(title=title).first()
            
            # If album doesn't exist
            if album is None:
                status= 404
                message= "Album does not exist"
                return JsonResponse({'message': message}, status=status)

            picture = album.picture_set.filter(image_id=image_id).first()
            
            # If picture doesn't exist
            if picture is None:
                status= 404
                message= "Picture ID is incorrect"
                return JsonResponse({'message': message}, status=status)
            
            # Deletes picture
            picture.delete()

        # If user doesn't exist
        except User.DoesNotExist as e:
            status= 404
            message= "Please register user for proceeding"
            return JsonResponse({'message': message}, status=status)
            
        # Catches all other exceptions
        except Exception as e:
            status= 500
            message= "Something went wrong. Please try again later."
            return JsonResponse({'message': message}, status=status) 

        # Returns success message
        return JsonResponse({'message':'Photo deleted'})


# To delete an entire album
def delete_album(request,username,title):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(username=username)
            album = user.album_set.filter(title=title).first()
            
            # If album doesn't exist
            if album is None:
                status= 404
                message= "Album does not exist"
                return JsonResponse({'message': message}, status=status)
            
            # Deletes album
            album.delete()

        # If user doesn't exist
        except User.DoesNotExist as e:
            status= 404
            message= "Please register user for proceeding"
            return JsonResponse({'message': message}, status=status)

        # Catches all other excepions     
        except Exception as e:
            status= 500
            message= "Something went wrong. Please try again later."
            return JsonResponse({'message': message}, status=status) 
        
        # Returns success message
        return JsonResponse({'message':'Album deleted'})

