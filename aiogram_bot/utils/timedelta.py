import datetime
import re
import typing

from aiogram import types

PATTERN = re.compile(r"(?P<value>\d+)(?P<modifier>[wdhms])")
LINE_PATTERN = re.compile(r"^(\d+[wdhms]){1,}$")

MODIFIERS = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str) -> datetime.timedelta:
    match = LINE_PATTERN.match(value)
    if not match:
        raise TimedeltaParseError("Invalid time format")

    try:
        result = datetime.timedelta()
        for match in PATTERN.finditer(value):
            value, modifier = match.groups()

            result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        raise TimedeltaParseError("Timedelta value is too large")

    return result


async def parse_timedelta_from_message(
    message: types.Message,
) -> typing.Optional[datetime.timedelta]:
    _, *args = message.text.split()

    if args:  # Parse custom duration
        try:
            duration = parse_timedelta(args[0])
        except TimedeltaParseError:
            await message.reply("Failed to parse duration")
            return
        if duration <= datetime.timedelta(seconds=30):
            return datetime.timedelta(seconds=30)
        return duration
    else:
        return datetime.timedelta(minutes=15)
