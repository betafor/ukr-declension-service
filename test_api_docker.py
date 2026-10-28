import requests
import yaml
from datetime import datetime

BASE_URL = "http://127.0.0.1:8080"

CASE_HINTS = {
    "nomn": "Називний",
    "gent": "Родовий",
    "datv": "Давальний",
    "accs": "Знахідний",
    "ablt": "Орудний",
    "loct": "Місцевий",
    "voct": "Кличний"
}

phrases_tests = [
    {"text": "IT-директор", "target_case": "datv"},
    {"text": "PR-менеджер", "target_case": "ablt"},
    {"text": "Генеральний директор ТОВ", "target_case": "datv"},
    {"text": "Керівник департаменту з маркетингу", "target_case": "datv"},
    {"text": "інженер-програміст", "target_case": "datv"},
    {"text": "Виробничий підрозділ (Рожівка)", "target_case": "datv"},
    {"text": "Відділ R&D НРК (ФРОДО)", "target_case": "ablt"},
    {"text": "Департамент розвитку нових продуктів", "target_case": "datv"},
    {"text": "Департамент розвитку продукту турелі \"БУРЯ\"", "target_case": "gent"}
]

fio_tests = [
    {"last_name": "Ковальчук", "first_name": "Олег", "middle_name": "Петрович", "gender": "M", "target_case": "datv"},
    {"last_name": "Ковальчук", "first_name": "Олена", "middle_name": "Petrivna", "gender": "F", "target_case": "datv"},
    {"last_name": "Сміт", "first_name": "Джон", "middle_name": "", "gender": "M", "target_case": "gent"},
    {"last_name": "Кідман", "first_name": "Ніколь", "gender": "F", "target_case": "datv"},
    {"last_name": "Востріков", "first_name": "Ігор", "middle_name": "Васильович", "gender": "M", "target_case": "voct"}
]


def run_tests():
    print("=== ЗАПУСК АВТОМАТИЧНОГО ТЕСТУВАННЯ МІКРОСЕРВІСУ ===")

    # 🌟 Объявляем структуру данных, которая запишется в YAML
    report_data = {
        "metadata": {
            "service_name": "UA Declension Service",
            "version": "1.0.3",
            "execution_time": datetime.utcnow().isoformat() + "Z",
            "status": "SUCCESS"
        },
        "phrase_declension_results": [],
        "fio_declension_results": []
    }

    print("\n📋 ПЕРЕВІРКА ПОСАД ТА ПІДРОЗДІЛІВ:")
    print("-" * 80)
    for t in phrases_tests:
        test_result = {
            "input": t["text"],
            "case": t["target_case"],
            "case_ua": CASE_HINTS.get(t["target_case"], "")
        }
        try:
            res = requests.post(f"{BASE_URL}/decline/phrase", json=t)
            hint = CASE_HINTS.get(t['target_case'], "")
            if res.status_code == 200:
                output = res.json().get('result')
                print(f"✅ Вхід: '{t['text']}' [{t['target_case']} - {hint}] -> Результат: '{output}'")
                test_result.update({"output": output, "status": "PASSED"})
            else:
                print(f"❌ Помилка {res.status_code} для '{t['text']}': {res.text}")
                test_result.update({"status": "FAILED", "error": res.text, "code": res.status_code})
                report_data["metadata"]["status"] = "FAILED"
        except Exception as e:
            print(f"💥 Системна помилка: {e}")
            test_result.update({"status": "ERROR", "error": str(e)})
            report_data["metadata"]["status"] = "FAILED"

        report_data["phrase_declension_results"].append(test_result)

    print("\n👤 ПЕРЕВІРКА ПІБ (ВКЛЮЧАЮЧИ ІНОЗЕМЦІВ):")
    print("-" * 80)
    for t in fio_tests:
        m_name = t.get('middle_name', '')
        full_in = f"{t['last_name']} {t['first_name']} {m_name if m_name else ''}".strip()

        test_result = {
            "input": full_in,
            "gender": t["gender"],
            "case": t["target_case"],
            "case_ua": CASE_HINTS.get(t["target_case"], "")
        }
        try:
            res = requests.post(f"{BASE_URL}/decline/fio", json=t)
            hint = CASE_HINTS.get(t['target_case'], "")
            if res.status_code == 200:
                output = res.json().get('result')
                print(f"✅ Вхід: '{full_in}' ({t['gender']}) [{t['target_case']} - {hint}] -> Результат: '{output}'")
                test_result.update({"output": output, "status": "PASSED"})
            else:
                print(f"❌ Помилка {res.status_code} для '{full_in}': {res.text}")
                test_result.update({"status": "FAILED", "error": res.text, "code": res.status_code})
                report_data["metadata"]["status"] = "FAILED"
        except Exception as e:
            print(f"💥 Системна помилка: {e}")
            test_result.update({"status": "ERROR", "error": str(e)})
            report_data["metadata"]["status"] = "FAILED"

        report_data["fio_declension_results"].append(test_result)

    # ВОТ ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ГЕНЕРАЦИЮ ЯМЛ-ФАЙЛА НА ДИСК:
    report_filename = "test_report_docker.yaml"
    with open(report_filename, "w", encoding="utf-8") as f:
        yaml.dump(report_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"\n💾 Звіт про тестування успішно збережено у файл: {report_filename}")

    # ГЕНЕРАЦИЯ КРАСИВОГО HTML-ОТЧЕТА
    html_content = f"""<!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Звіт про тестування сервісу відмінювання</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 40px; }}
            .container {{ max-width: 1100px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            h2 {{ color: #2980b9; margin-top: 30px; }}
            .meta {{ background: #ebf5fb; padding: 15px; border-radius: 6px; font-size: 14px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; background: white; }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #34495e; color: white; font-weight: 600; }}
            tr:hover {{ background-color: #f9f9f9; }}
            .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
            .badge-case {{ background-color: #e1f5fe; color: #0288d1; }}
            .badge-passed {{ background-color: #d4edda; color: #155724; }}
            .badge-failed {{ background-color: #f8d7da; color: #721c24; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Звіт про автоматичне тестування</h1>
            <div class="meta">
                <strong>Сервіс:</strong> {report_data['metadata']['service_name']} | 
                <strong>Версія:</strong> {report_data['metadata']['version']} | 
                <strong>Статус:</strong> <span class="badge badge-passed">{report_data['metadata']['status']}</span><br>
                <strong>Час запуску:</strong> {report_data['metadata']['execution_time']}
            </div>

            <h2>📋 Відмінювання посад та підрозділів</h2>
            <table>
                <tr><th>Вхідне словосполучення</th><th>Відмінок</th><th>Результат сервісу</th><th>Статус</th></tr>"""

    # 🌟 Исправлено: собираем строки БЕЗ капризных f-строк
    for r in report_data["phrase_declension_results"]:
        html_content += "\n<tr>"
        html_content += f"<td><strong>{r['input']}</strong></td>"
        html_content += f"<td><span class='badge badge-case'>{r['case_ua']} [{r['case']}]</span></td>"
        html_content += f"<td style='color: #2c3e50;'>{r['output']}</td>"
        html_content += "<td><span class='badge badge-passed'>Успішно</span></td>"
        html_content += "</tr>"

    html_content += """
            </table>

            <h2>👤 Відмінювання ПІБ (включаючи іноземців)</h2>
            <table>
                <tr><th>Вхідні дані (ПІБ)</th><th>Стать</th><th>Відмінок</th><th>Результат сервісу</th><th>Статус</th></tr>"""

    # 🌟 Исправлено: собираем строки БЕЗ капризных f-строк
    for r in report_data["fio_declension_results"]:
        html_content += "\n<tr>"
        html_content += f"<td><strong>{r['input']}</strong></td>"
        html_content += f"<td>{r['gender']}</td>"
        html_content += f"<td><span class='badge badge-case'>{r['case_ua']} [{r['case']}]</span></td>"
        html_content += f"<td style='color: #2c3e50;'>{r['output']}</td>"
        html_content += "<td><span class='badge badge-passed'>Успішно</span></td>"
        html_content += "</tr>"

    html_content += """
            </table>
        </div>
    </body>
    </html>"""

    # Запись физического файла на диск
    with open("test_report_docker.html", "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"💾 Гарний веб-звіт успішно збережено у файл: test_report.html")

if __name__ == "__main__":
    run_tests()