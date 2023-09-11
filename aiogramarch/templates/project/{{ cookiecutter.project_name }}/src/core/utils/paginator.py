"""
    Пагинатор состоящий из кнопок
"""


from typing import List, Callable, Awaitable

from math import ceil

from tortoise.queryset import QuerySet
from tortoise.models import Model

from aiogram.utils.keyboard import (
    InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
)


class Paginator:
    def __init__(self, objects_list: QuerySet, per_page: int = 10):
        self.objects_list = objects_list
        self.per_page = per_page
    
    async def __aiter__(self):
        for page_num in range(1, await self.num_pages):
            yield await self.page(page_num)

    @property
    async def num_pages(self) -> int:
        return ceil(await self.count / self.per_page)     

    @property
    async def count(self) -> int:
        return await self.objects_list.count()

    async def page(self, number: int):
        bottom = (number-1) * self.per_page
        return Page(
            objects_list=await self.objects_list.offset(bottom).limit(self.per_page), 
            number=number, 
            paginator=self,
            num_pages=await self.num_pages
        )


class Page:
    def __init__(
        self, objects_list: List[Model], number: int, paginator: Paginator,
        num_pages: int
    ):
        self.objects_list = objects_list
        self.number = number
        self.paginator = paginator
        self.num_pages = num_pages

    def __iter__(self):
        for i in self.objects_list:
            yield i

    def __repr__(self):
        return f"<Page {self.number} of {self.num_pages}>"

    def __len__(self):
        return len(self.objects_list)
    
    def has_next(self) -> bool:
        return self.number < self.num_pages

    def has_previous(self) -> bool:
        return self.number > 1

    def has_other_pages(self) -> bool:
        return self.has_previous() or self.has_next()

    def next_page_number(self) -> int:
        return self.number + 1

    def previous_page_number(self) -> int:
        return self.number - 1


async def get_paginate_keyboard(
    queryset: QuerySet, 
    i_button: Callable[[Model], Awaitable[InlineKeyboardButton]],
    next_button: Callable[[Page], Awaitable[InlineKeyboardButton]], 
    back_button: Callable[[Page], Awaitable[InlineKeyboardButton]],
    none_button: InlineKeyboardButton,
    per_page: int = 4, page_num: int = 1
) -> InlineKeyboardMarkup:
    paginator = Paginator(queryset, per_page)

    if page_num > await paginator.num_pages:
        page_num = 1
    elif page_num < 1:
        page_num = await paginator.num_pages

    page = await paginator.page(page_num)
    kbd = InlineKeyboardBuilder()
    if page.has_other_pages():
        for i in page:
            kbd.row(
                await i_button(i)
            )
        kbd.row(
            await back_button(page=page),
            InlineKeyboardButton(text=str(page_num), callback_data="123"),
            await next_button(page=page),
        )
        kbd.row(
            none_button
        )
    else:
        for i in page:
            kbd.row(
                await i_button(i)
            )
        kbd.row(
            none_button
        )

    return kbd.as_markup()
