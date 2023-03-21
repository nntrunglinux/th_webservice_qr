from datetime import datetime

def update_report_params(report_params, value):
    for param in report_params:
        if param['name'] == 'p_po_number':
            param.update({'values': value})

def float_to_currency_str(number_str):
    return "{:,}".format(number_str)

def safe_cast(val, to_type, default=None):
    try:
        if val is None:
            return default
        else:
            return to_type(val)
    except (ValueError, TypeError):
        return default

def date_safe_cast(
    timestamp_str: str,
    format_datetime="%Y-%m-%dT%H:%M:%S.%f%z",
    format_str="%d-%m-%Y",
    default="9999-01-01",
):
    try:
        timestamp_datetime = datetime.strptime(timestamp_str, format_datetime)
        timestamp_datetime_str = timestamp_datetime.strftime(format_str)
        return timestamp_datetime_str
    except (ValueError, TypeError):
        return default
