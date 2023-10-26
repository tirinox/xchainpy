from datetime import datetime, timezone


def parse_iso_date(date_str: str):
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
