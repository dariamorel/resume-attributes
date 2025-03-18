# Файл с различными методами
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PDFFileForm
import PyPDF2


def show_home_page(request):
	if request.method == 'POST':
		# form = PDFFileForm(request.POST, request.FILES)
		# if form.is_valid():
		# 	pdf_file = request.FILES['file']
		# 	pdf_reader = PyPDF2.PdfReader(pdf_file)
		# 	text = ""
		# 	for page in pdf_reader.pages:
		# 		text += page.extract_text()

		uploaded_file = request.FILES['file']
		file_path = f'media/{uploaded_file.name}'
		# сохранение файла
		with open(file_path, 'wb+') as destination:
			for chunk in uploaded_file.chunks():
				destination.write(chunk)

		# сохранение пути к файлу
		request.session['pdf_path'] = file_path
		return redirect('info_page')
	else:
		form = PDFFileForm()
	return render(request, 'main/home_page.html', {'form': form})