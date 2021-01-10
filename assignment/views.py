from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from .models import Document, ConsumerData
from django.http import HttpResponseRedirect
from pathlib import Path
import os
from django.http import HttpResponse
from django.contrib import messages
import pdftotext
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DataSerializer


def index(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        data = form.cleaned_data['document']
        form.save()
        path = os.path.join(settings.MEDIA_ROOT, f'documents/', str(data))

        try:
            with open(path, 'rb') as f:
                pdf = pdftotext.PDF(f)
            
            ConsumerData.objects.create(title=str(data), data='\n\n'.join(pdf))
            return redirect('data_view')
        except :
            messages.error(request, "Not a PDF file")
            return redirect("index")
    return render(request, 'assignment/index.html', {
        'form': form,
    })

    

def data_view(request):
    datas = ConsumerData.objects.all()
    return render(request, 'assignment/data.html', {'datas':datas})

def data_view_detail(request, pk):
    data = get_object_or_404(ConsumerData, pk=pk)
    return render(request, 'assignment/data_detail.html', {'data':data})


class ConsumerDataView(APIView):
    def get(self, request):
        data = ConsumerData.objects.all()
        ser = DataSerializer(data, many=True)
        return Response({"data":ser.data})
    
    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        saved_data = get_object_or_404(ConsumerData.objects.all(), pk=pk)
        data = request.data.get('consumer_data')
        ser = DataSerializer(instance=saved_data, data=data, partial=True)

        if ser.is_valid(raise_exception=True):
            saved_data = ser.save()
        return Response({"Data has been updated."})
    
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        saved_data = get_object_or_404(ConsumerData.objects.all(), pk=pk)
        saved_data.delete()
        return Response({"Data has been deleted."})





