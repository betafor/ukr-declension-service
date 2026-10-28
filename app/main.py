from fastapi import FastAPI
from app.schemas import FIORequest, PhraseRequest, DeclensionResponse
from app.services import decline_fio_word, decline_phrase_smart

app = FastAPI(
    title="Сервіс відмінювання (UA Declension Service)",
    description=(
        "Локальний мікросервіс для автоматичного та коректного відмінювання "
        "ПІБ (з урахуванием статі), посад та підрозділів українською мовою."
    ),
    swagger_ui_parameters={"defaultModelExpandDepth": 3, "displaySchemaPropertiesChoices": True},
    version="1.0.4"
)


@app.get(
    "/ping",
    tags=["System (Системні)"],
    summary="Перевірка працездатності сервісу (Health Check)",
    description="Повертає статус 'ok', якщо сервіс активний і працює."
)
async def ping():
    return {"status": "ok"}


@app.post(
    "/decline/fio",
    response_model=DeclensionResponse,
    tags=["UA Declension (Відмінювання)"],
    summary="Відмінювання ПІБ (Прізвище, Ім'я, По батькові)",
    description="Приймає ПІБ окремими частинами, враховує особливості чоловічих та жіночих закінчень в українській мові."
)
async def decline_fio(request: FIORequest):
    ln = decline_fio_word(request.last_name, 'ln', request.gender.value, request.target_case.value)
    fn = decline_fio_word(request.first_name, 'fn', request.gender.value, request.target_case.value)
    # ЗАХИСТ: якщо по батькові відсутнє (None), передаємо пустий рядок
    m_name = request.middle_name if request.middle_name is not None else ""
    mn = decline_fio_word(m_name, 'mn', request.gender.value, request.target_case.value)

    # Собираем только те части, которые реально существуют, исключая пустые строки
    full_name = " ".join([word for word in [ln, fn, mn] if word])

    return DeclensionResponse(result=full_name)


@app.post(
    "/decline/phrase",
    response_model=DeclensionResponse,
    tags=["UA Declension (Відмінювання)"],
    summary="Відмінювання словосполучень (посади, підрозділи)",
    description="Розумне відмінювання фраз: змінює лише головні слова, залишаючи залежні слова та прийменники (наприклад, 'з маркетингу', 'кадрів') у незмінному вигляді."
)
async def decline_phrase(request: PhraseRequest):
    result = decline_phrase_smart(request.text, request.target_case.value)
    return DeclensionResponse(result=result)
