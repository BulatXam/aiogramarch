from typing import Union

from pydantic import BaseModel


class SuccessPay(BaseModel):
    MERCHANT_ID: str	         # ID Вашего магазина
    AMOUNT: int	                 # Сумма платежа
    intid: str                   # Номер операции Free-Kassa
    MERCHANT_ORDER_ID: str       # Ваш номер заказа
    P_EMAIL: str	             # Email плательщика
    P_PHONE: str	             # Телефон плательщика (если указан)
    CUR_ID: str	                 # ID электронной валюты
    SIGN: str	                 # Подпись запроса
    us_key: str	                 # Дополнительные параметры
    payer_account: str	         # Номер счета/карты плательщика
    commission: int              # Сумма коммиссии
