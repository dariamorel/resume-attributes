import fitz
from django.http import HttpResponse
from django.shortcuts import render

from .structure.resume import Resume


def show_info_page(request):
    file_path = request.session.get('pdf_path')
    if not file_path:
        return HttpResponse("Файл не найден", status=400)

    pdf_doc = fitz.open(file_path)
    text = ""
    for page in pdf_doc:
        text += page.get_text()

    resume = Resume(text)

    return render(request, 'extractor/info_page.html',
                  {'name': resume.get_name(), 'position': resume.get_position(), 'phone_number': resume.get_phone_number(), 'email': resume.get_email(), 'website': resume.get_website(),
                   'work_experience': resume.get_work_experience(), 'education': resume.get_education(),
                   'skills': resume.get_skills(), 'languages': resume.get_languages()})
