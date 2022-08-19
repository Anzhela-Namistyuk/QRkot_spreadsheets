from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (columnCount, drive_version, rowCount,
                                sheets_range, sheets_version)

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', sheets_version)
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': rowCount,
                                                      'columnCount': columnCount}}}]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', drive_version)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for res in projects:
        close_date = datetime.strptime(
            res['CharityProject']['close_date'], "%Y-%m-%dT%H:%M:%S.%f"
        )
        create_date = datetime.strptime(
            res['CharityProject']['create_date'], "%Y-%m-%dT%H:%M:%S.%f"
        )
        days = close_date.day - create_date.day
        hours = close_date.hour - create_date.hour
        minutes = close_date.minute - create_date.minute
        seconds = close_date.second - create_date.second
        microsecond = close_date.microsecond - create_date.microsecond
        day = 'day' if days < 2 else 'days'
        new_row = [str(res['CharityProject']['name']),
                   f'{days} {day}, {hours}:{minutes}:{seconds}.{microsecond}',
                   str(res['CharityProject']['description'])
                   ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=sheets_range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
