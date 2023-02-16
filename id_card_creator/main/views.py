from django.shortcuts import render, HttpResponse
from .forms import IDCardForm
from id_card_creator.settings import BASE_DIR
import os
from .draft1 import createID
from datetime import datetime as dt
import zipfile
from io import StringIO, BytesIO

# Create your views here.
def homepage(request):
    if request.method == 'POST':
        form = IDCardForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            try:
                createID(data['last_name'],data['first_name'], data['user_number'], data['department'], data['photo'], data['level'])
                msg = 'done'
            except:
                msg = 'failed'
            
            if msg == 'done':
                return render(request, 'main/home.html', context={
                    'form':form,
                    'msg' : msg,
                    'img1':  os.path.join(f"{data['user_number']}_front.png"),
                    'img2':  os.path.join(f"{data['user_number']}_back.png"),
                })

    form = IDCardForm()
    return render(request, 'main/home.html', context={
        'form':form,
    })

def downloadImages(request, front, back):
    filenames = [os.path.join(BASE_DIR,'media',x) for x in [front, back]]
    zip_subdir = str(front).split('_')[0]
    zip_filename = '%s.zip' % zip_subdir

    s = BytesIO()

    zf = zipfile.ZipFile(s, 'w')

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        print(type(zip_path))

        zf.write(fpath, zip_path)
    
    zf.close()

    resp = HttpResponse(s.getvalue(), content_type= "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp
    # return HttpResponse('Hello')