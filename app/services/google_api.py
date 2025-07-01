from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json={
                'properties': {
                    'title': f'Отчёт от {dt.now().strftime(FORMAT)}',
                    'locale': 'ru_RU'
                },
                'sheets': [
                    {'properties': {'sheetType': 'GRID',
                                    'sheetId': 0,
                                    'title': 'Лист1',
                                    'gridProperties': {'rowCount': 50,
                                                       'columnCount': 10}}}]
            }
        )
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json={'type': 'user',
                  'role': 'writer',
                  'emailAddress': settings.email},
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', dt.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Дней сбора', 'Описание']
    ]
    for project in projects:
        table_values.append([
            str(project['name']),
            str(project['days']),
            str(project['description'])
        ])
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values}
        )
    )
