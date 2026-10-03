#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# setup_repo.sh
#
# Розкладає всі згенеровані файли курсової по структурі репозиторію
# coursework_bdis і готує все до git-коміту.
#
# РЕЗУЛЬТУЮЧА СТРУКТУРА:
#
#   coursework_bdis/
#   ├── README.md
#   ├── .gitignore
#   ├── docker-compose.yml          <- вся архітектура (backend+Mongo+ES+Neo4j+Redis)
#   ├── backend/                    <- код застосунку (з podcast-platform-stubs.zip)
#   ├── docker-lab/                 <- лабораторна з контейнерами (з docker-lab.zip)
#   └── docs/
#       ├── Звіт_курсова_бд.pdf
#       ├── architecture_addendum_podcasts.md
#       └── containerization_report_section.md
#
# ЩО ПОТРІБНО ЗРОБИТИ ПЕРЕД ЗАПУСКОМ (докладно також в чаті):
#   1. git clone https://github.com/evheniikozlov/coursework_bdis.git
#   2. cd coursework_bdis
#   3. Скопіювати в цю папку (coursework_bdis/) усі файли, завантажені з чату:
#        - podcast-platform-stubs.zip
#        - docker-lab.zip
#        - architecture_addendum_podcasts.md
#        - containerization_report_section.md
#        - Звіт_курсова_бд.pdf   (ваш файл звіту, якщо вже є)
#   4. Покласти цей скрипт (setup_repo.sh) туди ж і запустити:
#        bash setup_repo.sh
#
# Якщо файли лежать в іншій папці — передайте шлях першим аргументом:
#   bash setup_repo.sh /шлях/до/папки/із/завантаженнями
# ============================================================================

SRC_DIR="${1:-.}"

ZIP_STUBS="$SRC_DIR/podcast-platform-stubs.zip"
ZIP_DOCKERLAB="$SRC_DIR/docker-lab.zip"
MD_ADDENDUM="$SRC_DIR/architecture_addendum_podcasts.md"
MD_CONTAINERIZATION="$SRC_DIR/containerization_report_section.md"
PDF_REPORT="$SRC_DIR/Звіт_курсова_бд.pdf"

# ---------------------------------------------------------------------------
# Перевірки перед стартом
# ---------------------------------------------------------------------------
if [ ! -d .git ]; then
  echo "ПОМИЛКА: у поточній папці немає .git" >&2
  echo "Запускайте скрипт з кореня клонованого репозиторію coursework_bdis:" >&2
  echo "  git clone https://github.com/evheniikozlov/coursework_bdis.git" >&2
  echo "  cd coursework_bdis" >&2
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "ПОМИЛКА: не знайдено команду 'unzip'." >&2
  echo "Linux:   sudo apt install unzip" >&2
  echo "macOS:   unzip зазвичай вже є" >&2
  echo "Windows: запускайте через Git Bash / WSL, або розпакуйте .zip вручну" >&2
  echo "         і закоментуйте відповідні блоки unzip нижче." >&2
  exit 1
fi

echo "=============================================================="
echo "Крок 1/7: створення структури папок"
echo "=============================================================="
mkdir -p docs
mkdir -p backend
mkdir -p docker-lab
echo "  -> docs/, backend/, docker-lab/ готові."

echo "=============================================================="
echo "Крок 2/7: розпакування backend-коду (podcast-platform-stubs.zip)"
echo "=============================================================="
if [ -f "$ZIP_STUBS" ]; then
  TMP1="$(mktemp -d)"
  unzip -q "$ZIP_STUBS" -d "$TMP1"
  # В архіві код лежить у підпапці podcast-platform/ — переносимо саме ВМІСТ
  # цієї підпапки в backend/, а не її саму (щоб не було backend/podcast-platform/...).
  cp -r "$TMP1"/podcast-platform/. backend/
  rm -rf "$TMP1"
  echo "  -> backend/ наповнено кодом (domain/, application/, adapters/, generator/, bootstrap/)."
else
  echo "  !! Файл не знайдено: $ZIP_STUBS — пропускаю цей крок."
fi

echo "=============================================================="
echo "Крок 3/7: розпакування docker-lab (docker-lab.zip)"
echo "=============================================================="
if [ -f "$ZIP_DOCKERLAB" ]; then
  TMP2="$(mktemp -d)"
  unzip -q "$ZIP_DOCKERLAB" -d "$TMP2"
  cp -r "$TMP2"/docker-lab/. docker-lab/
  rm -rf "$TMP2"
  echo "  -> docker-lab/ наповнено (app/, docker-compose.lab.yml, docker-compose.full-platform.yml, README.md)."
else
  echo "  !! Файл не знайдено: $ZIP_DOCKERLAB — пропускаю цей крок."
fi

echo "=============================================================="
echo "Крок 4/7: винесення docker-compose.yml у корінь репозиторію"
echo "=============================================================="
if [ -f docker-lab/docker-compose.full-platform.yml ]; then
  cp docker-lab/docker-compose.full-platform.yml docker-compose.yml
  # У файлі був шлях білда '../podcast-platform' (бо лежав поруч з podcast-platform/).
  # Тепер цей docker-compose.yml у корені, а код — у backend/, тож виправляємо шлях:
  sed -i.bak 's#context: \.\./podcast-platform#context: ./backend#' docker-compose.yml
  rm -f docker-compose.yml.bak
  echo "  -> docker-compose.yml створено в корені, build-context виправлено на ./backend."
else
  echo "  !! docker-lab/docker-compose.full-platform.yml не знайдено — пропускаю."
fi

echo "=============================================================="
echo "Крок 5/7: документація у docs/"
echo "=============================================================="
if [ -f "$MD_ADDENDUM" ]; then
  cp "$MD_ADDENDUM" docs/
  echo "  -> docs/architecture_addendum_podcasts.md додано."
else
  echo "  !! Не знайдено: $MD_ADDENDUM"
fi

if [ -f "$MD_CONTAINERIZATION" ]; then
  cp "$MD_CONTAINERIZATION" docs/
  echo "  -> docs/containerization_report_section.md додано."
else
  echo "  !! Не знайдено: $MD_CONTAINERIZATION"
fi

if [ -f "$PDF_REPORT" ]; then
  cp "$PDF_REPORT" docs/
  echo "  -> docs/Звіт_курсова_бд.pdf додано."
else
  echo "  (інфо) PDF звіту не знайдено за шляхом $PDF_REPORT — якщо файл має іншу назву,"
  echo "         скопіюйте його в docs/ вручну."
fi

echo "=============================================================="
echo "Крок 6/7: .gitignore"
echo "=============================================================="
cat > .gitignore <<'EOF'
# Python
__pycache__/
*.pyc
.venv/
venv/

# Логи лабораторної з контейнерами — самі лог-файли не комітимо,
# але структуру папки (.gitkeep) зберігаємо, щоб папка існувала в репо.
docker-lab/logs/*
!docker-lab/logs/.gitkeep

# OS / IDE
.DS_Store
.idea/
.vscode/
EOF
mkdir -p docker-lab/logs
touch docker-lab/logs/.gitkeep
echo "  -> .gitignore створено, docker-lab/logs/.gitkeep додано."

echo "=============================================================="
echo "Крок 7/7: фінальна перевірка структури"
echo "=============================================================="
find . -maxdepth 2 -not -path './.git*' -not -path '.' | sort

cat <<'EOF'

==============================================================
ГОТОВО. Залишилось вручну (навмисно НЕ виконано автоматично,
щоб ви могли переглянути зміни перед комітом):

  git status                 # подивитись, що буде додано
  git add -A
  git commit -m "Add backend stubs, docker-lab, containerization docs"
  git push

ПІСЛЯ пушу перевірте на GitHub, що:
  - backend/ не містить вкладеної папки podcast-platform/ всередині себе
  - docker-lab/logs/ у репо порожня (тільки .gitkeep), без реальних логів
  - docker-compose.yml у корені посилається на "context: ./backend"
==============================================================
EOF
