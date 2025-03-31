import os

import fitz
from django.http import HttpResponse
from django.shortcuts import render

from .structure.resume import Resume


def show_info_page(request):
    file_path = request.session.get('pdf_path')
    file_name = request.session.get('pdf_name')
    if not file_path:
        return HttpResponse("Файл не найден", status=400)

    pdf_doc = fitz.open(file_path)

    # Извлекаем текст
    text = ""
    for page in pdf_doc:
        text += page.get_text()

    resume = Resume(text)

    # Извлекаем изображения
    images = []
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_data = base_image["image"]

            img_path = f'media/img/{file_name}.png'
            with open(img_path, "wb") as f:
                f.write(image_data)
            images.append(img_path)

        break

    if not os.path.exists(f'media/img/{file_name}.png'):
        file_name = ""

    return render(request, 'extractor/info_page.html',
                  {'img_name': file_name, 'name': resume.get_name(), 'position': resume.get_position(), 'phone_number': resume.get_phone_number(), 'email': resume.get_email(), 'website': resume.get_website(),
                   'work_experience': resume.get_work_experience(), 'education': resume.get_education(),
                   'skills': resume.get_skills(), 'languages': resume.get_languages()})
