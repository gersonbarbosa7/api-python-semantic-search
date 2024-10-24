from datetime import datetime, date

def convert_dates_to_string(results, data_key='publication_date'):
    # Converting date fields to strings to save on redis
    for result in results:
        if isinstance(result.get('publication_date'), (date, datetime)):
            result[data_key] = result[data_key].isoformat()

    return results