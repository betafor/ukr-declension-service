from enum import Enum

class TargetCase(str, Enum):
    nomn = "nomn"  # Називний (Хто? Що?)
    gent = "gent"  # Родовий (Кого? Чого?)
    datv = "datv"  # Давальний (Кому? Чому?)
    accs = "accs"  # Знахідний (Кого? Що?)
    ablt = "ablt"  # Орудний (Ким? Чим?)
    loct = "loct"  # Місцевий (На кому? На чому?)
    voct = "voct"  # Кличний (Форма звертання)

class GenderEnum(str, Enum):
    M = "M"        # Чоловіча стать
    F = "F"        # Жіноча стать