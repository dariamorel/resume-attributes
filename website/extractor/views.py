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

    print(text)

    resume = Resume(text)

    main_info = resume.get_main_info()
    name = main_info.name.text
    phone_number = main_info.phone_number.text
    email = main_info.email.text
    website = main_info.website.text
    position = main_info.position.text

    work_experience = resume.get_work_experience().get_info()
    education = resume.get_education().get_info()
    skills = resume.get_skills().get_info()

    return render(request, 'extractor/info_page.html',
                  {'name': name, 'phone_number': phone_number, 'email': email, 'website': website, 'position': position,
                   'work_experience': work_experience, 'education': education,
                   'skills': skills})
