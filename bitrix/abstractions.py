#from db import Organization
from aiogram.types.message import Message


class IncomingMessage():
    def __init__(self, raw: dict):

        self.connector = raw['data[CONNECTOR]']
        self.chat_id = int(raw['data[MESSAGES][0][chat][id]'])
        try:
            self.text = raw['data[MESSAGES][0][message][text]'].split('[br]')[1]
        except IndexError:
            self.text = raw['data[MESSAGES][0][message][text]']
        self.im = {'chat_id': raw['data[MESSAGES][0][im][chat_id]'], 'message_id': raw['data[MESSAGES][0][im][message_id]']}


class OutgoingMessage():
    def __init__(self, message: Message):
        self.data = {
            'user': {'id': message.from_user.id, 'name': message.from_user.full_name},
            'message': {'text': message.text},
            'chat': {'id': message.from_user.id}
        }


class Lead():
    def __init__(self, 
                 title: str, 
                 number: str, 
                 #organization: Organization, 
                 responsible_id: int, 
                 name: str = None, 
                 birthday_data: dict = {}):

        self.birthday_data = self._parse_birthday_data(birthday_data)

        self.fields = {
            'TITLE': title,
            'NAME': name,
            'HAS_PHONE': 'Y',
            'PHONE': [{'VALUE': number, 'VALUE_TYPE': 'WORK'}],
            #'UF_CRM_LEAD_1653746487781': f'{organization.city.name} - {organization.name}',
            'ASSIGNED_BY_ID': responsible_id,
            **self.birthday_data
        }

    def _parse_birthday_data(self, raw: dict) -> dict:

        if raw == {}: return {}

        date = raw.get('date')
        time = raw.get('time')
        child_name = raw.get('child_name')
        born_date = raw.get('born_date')
        parent_name = raw.get('parent_name')

        return {
            'NAME': parent_name,
            'UF_CRM_1630095279137': self._date_validate(date),
            'UF_CRM_1593519593': child_name,
            'UF_CRM_1644598445446': self._date_validate(born_date),
            'COMMENTS': time
        }

    def _date_validate(self, date_raw: str) -> str:
        if date_raw is None: return None
        try:
            date_raw = date_raw.split('.')
            year = self._year_validate(date_raw[2])
            mounth = date_raw[1]
            day = date_raw[0]
            date = f'{year}-{mounth}-{day}'
            return date
        except IndexError:
            return None

    def _year_validate(self, year_raw: str) -> str:
        if len(year_raw) == 2: return f'20{year_raw}'
        else: return year_raw
