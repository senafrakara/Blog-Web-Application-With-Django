from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
# Create your views here.


def register(request):
    if request.method == 'POST':
        #eğer post yaratılmış kişi içini doldurmuş ve save demişse yani post metodu request edilmişse, is_valid true dönüyorsa onu db ye kaydeder bilgileri
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #if form data is valid then save it into the database
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('blog-home')

    else:
        #eğer post request edilmemişse yani form yaratılmamışsa boş bir form yaratılır burada da. Hem save edilmesi hem de yaratılması için aynı metod kullanılıyor yani
        form = RegistrationForm()

    #context dictionary is created in here and it will contain the name form that contains the value for this form that we've created above here
    #and once we create that this we can pass this in as the third argument in the below return statement
    #so we can actually access the form within our template and this template is register.html within our users dictionary
    context = {'form': form}
    return render(request, 'users/register.html', context)



