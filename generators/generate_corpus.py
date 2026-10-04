#!/usr/bin/env python3
"""
Генератор корпусу подкаст-епізодів у JSONL для курсової з БД.

Головний принцип: генератор — це прилад керованості, а не «реалістичності».
Реалістичність тексту оцінюється в 0 балів; керованість дає тобі:
  - передбачувані позитивні/негативні тести пошуку (ти наперед знаєш словник);
  - контрольований розподіл по шардинг-ключах (show_id / рік / мова);
  - навмисне перетину сутностей (гості повторюються) -> графовим і
    рекомендаційним запитам є що повертати.

Один документ = один ЕПІЗОД. Вивід — JSONL (документ на рядок), стрімом,
щоб файл будь-якого розміру не тримався в пам'яті ні тут, ні в replayer'і.

Запуск:
    python generate_corpus.py --episodes 50000 --out corpus.jsonl
"""

import argparse
import json
import random
from datetime import date, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# ХРЕБЕТ: тематичні словники. Саме ці слова вкидаються в описи.
# Наслідок: запит по будь-якому слові звідси гарантовано щось знайде
# (позитивний тест), а будь-яке слово, якого тут НЕМАЄ, гарантовано дасть
# пустий результат (негативний тест). Ти керуєш видачею наперед.
# ─────────────────────────────────────────────────────────────────────────────
TOPICS = {
    "ml": ["нейромережі", "трансформери", "градієнтний спуск", "датасет",
           "перенавчання", "ембединги", "класифікатор", "функція втрат",
           "машинне навчання", "інференс"],
    "startups": ["венчурний капітал", "раунд інвестицій", "юніт-економіка",
                 "піввот", "продукт-маркет фіт", "стартап", "засновник",
                 "MVP", "рантвей", "трекшн"],
    "history": ["індустріалізація", "архівні документи", "історіографія",
                "першоджерела", "хронологія", "радянський період",
                "колективізація", "статистика перепису"],
    "science": ["квантова механіка", "чорні діри", "еволюція", "нейрони",
                "гіпотеза", "експеримент", "спостереження", "теорія відносності"],
    "cinema": ["режисер", "монтаж", "сценарій", "оператор-постановник",
               "прем'єра", "кінофестиваль", "довгий кадр", "звукорежисура"],
}

FILLER = ["сьогодні", "також", "розмова", "гість", "детально", "питання",
          "думка", "приклад", "історія", "підхід", "досвід", "команда",
          "проєкт", "рішення", "ідея", "практика", "висновок", "контекст"]

TITLE_TEMPLATES = [
    "Все про {kw}",
    "{kw}: розбір по суті",
    "Як влаштовано {kw}",
    "Випуск про {kw} та {kw2}",
    "{kw} простими словами",
    "Розмова про {kw}",
    "{kw} і {kw2}: що варто знати",
    "Глибоке занурення: {kw}",
    "{kw} — міфи та реальність",
    "Практичний гайд: {kw}",
    "{kw}: з чого почати",
]

# Опис збирається як вступ + 2-4 речення тіла + (опційно) згадка гостя + фінал.
# Шаблони навмисно збудовані так, щоб ключове слово в НАЗИВНОМУ відмінку читалося
# природно (конструкції «тема — X», «ключові поняття: X, Y», двокрапка+перелік),
# тож текст виглядає пристойно без жодного відмінювання й без залежностей.
DESC_OPENINGS = [
    "Тема цього випуску — {kw}.",
    "Головний сюжет розмови: {kw} та {kw2}.",
    "Цей епізод присвячений темі «{kw}».",
    "У фокусі — {kw} і все, що навколо неї.",
    "Розбираємо велику тему: {kw}.",
]
DESC_BODY = [
    "Ключові поняття випуску: {kw}, {kw2}, {fill}.",
    "Окремий блок — про {kw} і чому це важливо.",
    "Обговорюємо: {kw}, {kw2} та практичні приклади.",
    "Другий розділ — {kw}: розбір, {fill} і поширені помилки.",
    "Торкаємось і суміжних питань: {kw2}, {fill}.",
    "Багато уваги приділяємо темі {kw2}.",
    "Практична частина — як {kw} працює на реальних кейсах.",
    "Розділи випуску: вступ, {kw}, {kw2}, підсумки.",
]
DESC_GUEST = [
    "Гість епізоду — {guest}, з ним говоримо про {kw}.",
    "До розмови долучається {guest}.",
    "У студії — {guest}; головна тема бесіди: {kw}.",
]
DESC_CLOSINGS = [
    "Насамкінець — відповіді на питання та підсумки по темі {kw}.",
    "У фіналі повертаємось до {kw} й підбиваємо підсумки.",
    "Таймкоди, лінки та джерела — в описі.",
    "Слухайте до кінця: {fill} і головні висновки.",
]

FIRST_NAMES = ["Олег", "Ірина", "Максим", "Наталя", "Андрій", "Софія",
               "Дмитро", "Олена", "Богдан", "Марія", "Сергій", "Юлія",
               "Тарас", "Катерина", "Ігор", "Вікторія", "Роман", "Оксана",
               "Артем", "Анна", "Володимир", "Тетяна", "Павло", "Дарина",
               "Микола", "Христина", "Василь", "Аліна", "Юрій", "Людмила",
               "Денис", "Ольга", "Віктор", "Галина", "Степан", "Зоряна"]
LAST_NAMES = ["Коваленко", "Шевченко", "Бондаренко", "Ткаченко", "Мельник",
              "Кравчук", "Поліщук", "Савченко", "Гриценко", "Лисенко",
              "Марченко", "Руденко", "Панченко", "Романюк", "Захарченко",
              "Дмитренко", "Іванченко", "Петренко", "Сидоренко", "Литвиненко",
              "Мороз", "Бойко", "Кравченко", "Олійник", "Пономаренко",
              "Ковальчук", "Ткачук", "Шевчук", "Мазур", "Гончар",
              "Кузьменко", "Данилюк", "Гаврилюк", "Наконечний"]


def build_people(n, rng):
    """Пул людей, СПІЛЬНИЙ для ведучих і гостей. Одна людина може вести одне
    шоу і бути гостем в іншому — це збагачує граф. Пул навмисне менший за
    кількість епізодів, тож перетину виникають самі собою."""
    combos = [f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES]
    rng.shuffle(combos)                        # перемішуємо весь картезіанський добуток імен
    people = []
    for i in range(n):
        # ключем графа завжди є унікальний person_id; ім'я — лише відображення.
        # Комбінацій (36x34 = 1224) більше за типовий пул, тож суфікси не потрібні;
        # якщо колись задаси --people > 1224, імена почнуть повторюватись без чисел.
        name = combos[i % len(combos)]
        people.append({"person_id": f"p_{i:05d}", "name": name})
    return people


def build_shows(n_shows, people, rng):
    """Пул шоу. Кожне шоу має фіксовану тему (1, іноді 2) і 1-2 постійних
    ведучих із пулу людей. show_id — природний шардинг-ключ."""
    shows = []
    for i in range(n_shows):
        topics = [rng.choice(list(TOPICS))]
        if rng.random() < 0.25:                      # чверть шоу — крос-тематичні
            topics.append(rng.choice(list(TOPICS)))
        hosts = rng.sample(people, k=rng.randint(1, 2))
        shows.append({
            "show_id": f"show_{i:04d}",
            "show_title": f"Подкаст «{rng.choice(FILLER).capitalize()}»",
            "topics": sorted(set(topics)),
            "host_ids": [h["person_id"] for h in hosts],
            "host_names": [h["name"] for h in hosts],
        })
    return shows


def make_text(topics, guest_names, rng):
    """Заголовок + опис із вкиданням ключових слів теми епізоду.
    Метод — шаблони+інжекція: нуль залежностей, мікросекунди на документ,
    і повний контроль над тим, які слова опиняться в тексті. Опис структурований
    (вступ -> тіло -> гість -> фінал) і згадує реальні сутності графа (гостя),
    тож сніпети в пошуку виглядають як справжні нотатки до випуску."""
    kws = [k for t in topics for k in TOPICS[t]]
    pick = lambda: rng.choice(kws)

    def fmt(tmpl):
        return tmpl.format(kw=pick(), kw2=pick(), fill=rng.choice(FILLER),
                           guest=(guest_names[0] if guest_names else "гість"))

    title = fmt(rng.choice(TITLE_TEMPLATES)).capitalize()

    parts = [fmt(rng.choice(DESC_OPENINGS))]
    for st in rng.sample(DESC_BODY, k=rng.randint(2, 4)):
        parts.append(fmt(st))
    if guest_names and rng.random() < 0.8:            # згадуємо гостя, коли він є
        parts.append(fmt(rng.choice(DESC_GUEST)))
    parts.append(fmt(rng.choice(DESC_CLOSINGS)))
    return title, " ".join(parts)


def make_episode(idx, shows, people, start, span_days, rng):
    show = rng.choice(shows)                          # нерівномірність тут -> «гарячі» шарди
    topics = show["topics"]

    n_guests = rng.choices([0, 1, 2, 3], weights=[15, 45, 30, 10])[0]
    guests = rng.sample(people, k=n_guests) if n_guests else []

    title, desc = make_text(topics, [g["name"] for g in guests], rng)

    published = start + timedelta(days=rng.randint(0, span_days))
    return {
        "episode_id": f"ep_{idx:07d}",
        "show_id": show["show_id"],
        "show_title": show["show_title"],
        "title": title,
        "description": desc,                          # <- поле, яке індексує пошук
        "topics": topics,
        "host_ids": show["host_ids"],
        "guest_ids": [g["person_id"] for g in guests],
        "guest_names": [g["name"] for g in guests],
        "published": published.isoformat(),
        "year": published.year,                       # зручний альтернативний шардинг-ключ
        "duration_sec": int(rng.gauss(3600, 1200)) % 10800 + 300,
        "language": rng.choices(["uk", "en"], weights=[80, 20])[0],
    }


def main():
    ap = argparse.ArgumentParser(description="Генератор JSONL-корпусу подкастів")
    ap.add_argument("--episodes", type=int, default=50_000)
    ap.add_argument("--shows", type=int, default=200)
    ap.add_argument("--people", type=int, default=800,
                    help="пул людей; менше за episodes -> більше перетинів у графі")
    ap.add_argument("--start-date", default="2023-01-01")
    ap.add_argument("--days", type=int, default=1000,
                    help="діапазон дат публікації від start-date")
    ap.add_argument("--seed", type=int, default=42,
                    help="фіксований seed -> відтворюваний корпус для чесних замірів")
    ap.add_argument("--out", default="corpus.jsonl")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    people = build_people(args.people, rng)
    shows = build_shows(args.shows, people, rng)
    start = date.fromisoformat(args.start_date)

    with open(args.out, "w", encoding="utf-8", buffering=1 << 20) as f:
        for i in range(args.episodes):
            ep = make_episode(i, shows, people, start, args.days, rng)
            f.write(json.dumps(ep, ensure_ascii=False))
            f.write("\n")

    print(f"OK: {args.episodes} епізодів -> {args.out}")
    print(f"    шоу: {args.shows}, людей у пулі: {args.people} "
          f"(~{args.episodes / args.people:.0f} появ на людину в середньому)")


if __name__ == "__main__":
    main()
