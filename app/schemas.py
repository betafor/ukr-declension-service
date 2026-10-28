from pydantic import BaseModel, Field
from app.enums import TargetCase, GenderEnum
from typing import Optional

# Создаем общую текстовую шпаргалку по падежам для документации
CASE_DESCRIPTION_UA = (
    "Цільовий відмінок для відмінювання. Допустимі значення:\n"
    "* **nomn** — Називний (Хто? Що?)\n"
    "* **gent** — Родовий (Кого? Чого?)\n"
    "* **datv** — Давальний (Кому? Чому?)\n"
    "* **accs** — Знахідний (Кого? Що?)\n"
    "* **ablt** — Орудний (Ким? Чим?)\n"
    "* **loct** — Місцевий (На кому? На чому?)\n"
    "* **voct** — Кличний (Форма звертання)"
)

class FIORequest(BaseModel):
    last_name: str = Field(
        ...,
        description="Прізвище співробітника в називному відмінку",
        json_schema_extra={"example": "Востріков"}
    )
    first_name: str = Field(
        ...,
        description="Ім'я співробітника в називному відмінку",
        json_schema_extra={"example": "Ігор"}
    )
    middle_name: Optional[str] = Field(
        default=None,  # поле НЕ обязательное
        description="По батькові співробітника (необов'язково для іноземців)",
        json_schema_extra={"example": "Васильович"}
    )
    gender: GenderEnum = Field(
        ...,
        description="Стать співробітника: M (Чоловіча) або F (Жіноча)"
    )
    target_case: TargetCase = Field(
        ...,
        description=CASE_DESCRIPTION_UA
    )

class PhraseRequest(BaseModel):
    text: str = Field(
        ...,
        description="Повний текст посади або підрозділу (словосполучення)",
        json_schema_extra={"example": "Головний бухгалтер з обліку"}
    )
    target_case: TargetCase = Field(
        ...,
        description=CASE_DESCRIPTION_UA
    )

class DeclensionResponse(BaseModel):
    result: str = Field(
        ...,
        description="Результат відмінювання українською мовою",
        json_schema_extra={"example": "Вострікова Ігоря Васильовича"}
    )
