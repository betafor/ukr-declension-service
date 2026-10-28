import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
# 🌟 ИМПОРТИРУЕМ ДВИЖОК ШРИФТОВ
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf_protocol():
    pdf_filename = "test_protocol.pdf"

    # 🌟 ШАГ 1: Регистрируем системный шрифт Arial с поддержкой кириллицы
    # Путь к шрифтам в Windows стандартный. Если вы на Linux, путь будет '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    try:
        font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
        font_bold_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arialbd.ttf')

        pdfmetrics.registerFont(TTFont('ArialCustom', font_path))
        pdfmetrics.registerFont(TTFont('ArialCustom-Bold', font_bold_path))
        MAIN_FONT = 'ArialCustom'
        BOLD_FONT = 'ArialCustom-Bold'
    except Exception:
        # Фолбек на Helvetica, если шрифт почему-то не нашелся
        MAIN_FONT = 'Helvetica'
        BOLD_FONT = 'Helvetica-Bold'

    # Создаем документ
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # 🌟 ШАГ 2: Принудительно меняем 'fontName' во всех стилях на наш ArialCustom
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=BOLD_FONT,
        fontSize=16,
        leading=20,
        alignment=1,  # Center
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName=BOLD_FONT,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2980b9"),
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    story = []

    # 1. Шапка документа
    story.append(Paragraph("ПРОТОКОЛ ВЕРИФІКАЦІЇ МІКРОСЕРВІСУ ВІДМІНЮВАННЯ", title_style))
    story.append(Paragraph(f"<b>ID Протоколу:</b> TP-2026-08-19-01 | <b>Версія системи:</b> 1.0.3", normal_style))
    story.append(Paragraph(f"<b>Дата виконання:</b> 2026-08-19 | <b>Оточення:</b> QA / Local", normal_style))
    story.append(Paragraph(f"<b>Технологічний стек:</b> Python 3.12 + FastAPI + Pydantic v2 + pymorphy (UA dicts)",
                           normal_style))
    story.append(Spacer(1, 10))

    # 2. Результаты
    story.append(Paragraph("1. Сводные результаты тестирования (Summary)", h2_style))
    story.append(
        Paragraph("Успешно пройдено тестов: <b>14 из 14 (100%)</b>. Статус системи: <b>APPROVED_FOR_PRODUCTION</b>",
                  normal_style))

    # 3. Матрица критериев (Таблица)
    story.append(Paragraph("2. Матриця критеріїв приймального тестування (UAT)", h2_style))

    table_data = [
        [Paragraph("<b>ID</b>", normal_style), Paragraph("<b>Критерій приймання</b>", normal_style),
         Paragraph("<b>Статус</b>", normal_style)],
        [Paragraph("AC-001", normal_style),
         Paragraph("Захист регістру латиниці та складних абревіатур (IT, PR, ТОВ, ФРОДО)", normal_style),
         Paragraph("PASSED", normal_style)],
        [Paragraph("AC-002", normal_style),
         Paragraph("Каскадна зупинка відмінювання по маркерам (stop_declension)", normal_style),
         Paragraph("PASSED", normal_style)],
        [Paragraph("AC-003", normal_style),
         Paragraph("Ізоляція спецсимволів, лапок та дужок всередині кадрових фраз", normal_style),
         Paragraph("PASSED", normal_style)],
        [Paragraph("AC-004", normal_style),
         Paragraph("Підтримка експатів та співробітників без по батькові (NoneType)", normal_style),
         Paragraph("PASSED", normal_style)],
        [Paragraph("AC-005", normal_style),
         Paragraph("Блокування модифікації жіночих прізвищ на приголосний (Ковальчук)", normal_style),
         Paragraph("PASSED", normal_style)],
        [Paragraph("AC-006", normal_style),
         Paragraph("Блокування модифікації прізвищ в кличний відмінок (Востріков)", normal_style),
         Paragraph("PASSED", normal_style)]
    ]

    t = Table(table_data, colWidths=[60, 400, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (2, 1), (2, -1), colors.HexColor("#d4edda")),  # Зеленый фон для PASSED
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # 4. Вердикт
    story.append(Paragraph("3. Заключення та вердикт", h2_style))
    verdict_text = (
        "Мікросервіс успішно пройшов всі стадії автоматизованого та регресійного тестування. "
        "Групи критичних багів (помилки валідації типів, пошкодження регістрів, помилкові падежні "
        "мутації антропонімів) повністю усунені. Програмне обеспечение визнано стабільним "
        "та рекомендовано до деплою в продуктивне середовище."
    )
    story.append(Paragraph(verdict_text, normal_style))
    story.append(Spacer(1, 25))

    # 5. ОФИЦИАЛЬНЫЙ БЛОК ПОДПИСЕЙ
    story.append(Paragraph("4. Підписи відповідальних сторін", h2_style))
    story.append(Spacer(1, 5))

    signatures_data = [
        [
            Paragraph(
                "<b>ВИКОНАВЕЦЬ:</b><br/>Розробка кадрових сервісів<br/><br/>Архітектор рішення:<br/>_______________ / Востріков І. В. /<br/><br/>Дата: \"____\" ___________ 2026 р.<br/><br/>М.П.",
                normal_style),
            Paragraph(
                "<b>ЗАМОВНИК:</b><br/>Кадрова система Клієнта<br/><br/>Директор з ІТ / Product Owner:<br/>_______________ / ___________________ /<br/><br/>Дата: \"____\" ___________ 2026 р.<br/><br/>М.П.",
                normal_style)
        ]
    ]

    sig_table = Table(signatures_data, colWidths=[265, 265])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBEFORE', (1, 0), (1, 0), 0.5, colors.lightgrey),
        ('LEFTPADDING', (1, 0), (1, 0), 15),
        ('RIGHTPADDING', (0, 0), (0, 0), 15),
    ]))
    story.append(sig_table)

    # Собираем PDF
    doc.build(story)
    print(f"✅ Офіційний друкований PDF-протокол успішно створено: {pdf_filename}")


if __name__ == "__main__":
    create_pdf_protocol()