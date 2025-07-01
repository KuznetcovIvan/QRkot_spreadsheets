import copy
from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    FORMAT, MAX_SHEET_COLUMN, MAX_SHEET_ROW, SEC_IN_DAY
)

SPREADSHEET_TEMPLATE = dict(
    properties=dict(
        title='Отчёт от {date}',
        locale='ru_RU',
    ),
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=MAX_SHEET_ROW,
                columnCount=MAX_SHEET_COLUMN,
            )
        )
    )]
)
HEADER = [
    ['Отчёт от', '{date}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Дней сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body = copy.deepcopy(SPREADSHEET_TEMPLATE)
    spreadsheet_body['properties']['title'] = (
        spreadsheet_body['properties']['title']
        .format(date=dt.now().strftime(FORMAT))
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={'type': 'user',
                  'role': 'writer',
                  'emailAddress': settings.email},
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list[tuple[str, dt, dt, str]],
        wrapper_services: Aiogoogle
) -> None:
    table_values = [
        *[[HEADER[0][0], dt.now().strftime(FORMAT)], *HEADER[1:]],
        *[list(map(str, (
            project[0],
            round((project[1] - project[2]).total_seconds() / SEC_IN_DAY, 2),
            project[3]
        )))
            for project in sorted(projects, key=lambda pr: pr[1] - pr[2])]
    ]
    num_row, num_col = len(table_values), max(map(len, table_values))
    if num_row > MAX_SHEET_ROW or num_col > MAX_SHEET_COLUMN:
        raise ValueError('Превышены ограничения таблицы: '
                         f'{num_row}/{MAX_SHEET_ROW} строк, '
                         f'{num_col}/{MAX_SHEET_COLUMN} колонок.')
    service = await wrapper_services.discover('sheets', 'v4')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{num_row}C{num_col}',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values}
        )
    )
