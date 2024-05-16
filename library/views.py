from django.shortcuts import render,redirect
from .forms import createData,UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Data
import os, pandas as pd

def home(request):
    display_background_image = True
    return render(request,'home.html', {'display_background_image': display_background_image})
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    # Set display_background_image to True only for the initial registration page load
    display_background_image = request.method == 'GET'
    background_image_url = '\static\Background.avif'
    return render(request, 'register.html', {'form': form, 'background_image_url': background_image_url, 'display_background_image': display_background_image})



def add_songs(request):
    if request.method == 'POST':
        form = createData(request.POST)
        if form.is_valid():
            form.save()
            return redirect('song_list')  # Redirect to the song list page after successful form submission
    else:
        form = createData()
    
    return render(request, 'song_list.html', {'form': form})



def add_rec_songs(request):
    if request.method == 'POST':
        # Extract song details from the POST request
        song_name = request.POST.get('song_name', '')
        song_year = request.POST.get('song_year', '')
        song_artist = request.POST.get('song_artist', '')  # Ensure these names match the input names in the template
        song_genre = request.POST.get('song_genre', '')
        song_rating = request.POST.get('song_rating', '')
        
        # Ensure that the year value is converted to an integer
        if song_year:
            song_year = int(song_year)
        else:
            song_year = None  # Set to None if year is not provided
        
        # Ensure that the rating value is converted to an integer
        if song_rating == '':
            song_rating = 0
        else:
            song_rating = int(song_rating)

        # Create a new song entry in the playlist
        song = Data.objects.create(song=song_name, year=song_year, artist=song_artist, genre=song_genre, rating=song_rating)
        
        return redirect('song_list')  # Redirect to the song list page after successful addition to playlist
    else:
        form = createData()
    
    return render(request, 'song_list.html', {'form': form})

def login_view(request):
    display_background_image = True
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('song_list')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'display_background_image': display_background_image})

def logout_view(request):
    logout(request)
    return redirect('home') 

def song_list(request):
    songs = Data.objects.all()
    return render(request, 'song_list.html', {'songs': songs})


def delete_song(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        if song_id:
            try:
                song = Data.objects.get(id=song_id)
                song.delete()
            except Data.DoesNotExist:
                pass  # Handle the case where the song does not exist
    
    # Retrieve the updated list of songs after deletion
    songs = Data.objects.all()  # Or use any appropriate queryset to fetch the songs
    
    return render(request, 'song_list.html', {'songs': songs})


from django.shortcuts import render
from .code.package import recommend_songs 

def song_recommendation(request):
    if request.method == 'POST':
        # Process input data from the form
        song_name = request.POST.get('song_name')
        year = request.POST.get('year')
        
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Append the "code" directory to the current directory
        code_dir = os.path.join(current_dir, "code")

        # Construct the absolute path to the CSV file
        csv_file_path = os.path.join(code_dir, "data.csv")

        # Read the CSV file
        data = pd.read_csv(csv_file_path)


        # Call the recommendation function
        recommendations = recommend_songs([{'name': song_name, 'year': int(year)}], data)

        # Render the template with recommendations
        return render(request, 'recommendations.html', {'recommendations': recommendations})
    else:
        # Render the form for input
        return render(request, 'song_recommendation_form.html')

from django.http import HttpResponse
import pandas as pd
from .models import Data

def export_to_excel(request):
    # Assuming you have a queryset named 'songs' containing the data to export
    songs = Data.objects.all()

    # Convert queryset to DataFrame
    data = {
        'Song': [song.song for song in songs],
        'Artist': [song.artist for song in songs],
        'Year': [song.year for song in songs],
        'Genre': [song.genre for song in songs],
        'Rating': [song.rating for song in songs]
    }
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to hold the Excel file in memory
    from io import BytesIO
    buffer = BytesIO()

    # Create Excel writer object and write the DataFrame to it
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Set the buffer position to the beginning
    buffer.seek(0)

    # Prepare the HTTP response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=songs.xlsx'

    return response


