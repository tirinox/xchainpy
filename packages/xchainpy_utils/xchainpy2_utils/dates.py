from datetime import datetime, timezone


def parse_iso_date(date_str: str) -> datetime:
    """
    Parse an ISO date string to a datetime object.
    :param date_str: The ISO date string to parse.
    :return: A datetime object.
    """
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        # Before Python 3.11, datetime.fromisoformat() stumbles on Z in the end of the string
        if date_str.endswith('Z'):
            dt = datetime.fromisoformat(date_str[:-1])
            # set UTC timezone
            return dt.replace(tzinfo=timezone.utc)
        else:
            raise
