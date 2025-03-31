# Файл с различными методами
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PDFFileForm
import PyPDF2


def show_home_page(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['file']
		file_path = f'media/pdfs/{uploaded_file.name}'
		# сохранение файла
		with open(file_path, 'wb+') as destination:
			for chunk in uploaded_file.chunks():
				destination.write(chunk)

		# сохранение пути к файлу
		request.session['pdf_path'] = file_path
		request.session['pdf_name'] = uploaded_file.name
		return redirect('info_page')
	else:
		form = PDFFileForm()
	return render(request, 'main/home_page.html', {'form': form})