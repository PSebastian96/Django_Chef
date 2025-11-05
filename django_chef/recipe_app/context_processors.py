import datetime

def show_date(request):
    current_date = datetime.date.today()
    return {
        'current_date': current_date,
    }