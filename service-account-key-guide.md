## Для получения JSON-файла с ключом доступа к сервисному аккаунту
### 1. Создайте проект в Google Cloud:
- Перейдите в [`Google Cloud Console`](https://console.cloud.google.com/projectselector2/home/dashboard) → Нажмите кнопку `Create Project` → Задайте имя проекту → Нажмите кнопку `Create`.
### 2. Подключите Google Drive API и Google Sheets API к созданному проекту:
- На плитке `APIs` нажмите `Go to APIs overview`.
- Нажмите `Enabled APIs and services` или выберите в левом меню пункт `Library`.
- В открывшемся окне поочерёдно выберите и включите:
    - `Google Drive API`
    - `Google Sheets API`
### 3. Создайте сервисный аккаунт:
- Перейдите в раздел `Credentials`.
- Нажмите `Create credentials` → выберите пункт `Service account`.
- Заполните поля:
    - `Service account name`
    - `Service account ID`
    - `Service account description`
- Выберите роль для сервисного аккаунта (например, `Editor` или `Owner` — в зависимости от задач).
- При необходимости назначьте права администратора вашему пользовательскому аккаунту.
### 4. Скачайте JSON-файл с ключом доступа:
- Перейдите на экран `Credentials/<название вашего сервисного аккаунта>`.
- Нажмите вкладку `Keys` → `Add Key` → `Create New Key`.
- Выберите формат `JSON` → нажмите `Create`.
- Файл с приватным ключом будет автоматически скачан на ваш компьютер.