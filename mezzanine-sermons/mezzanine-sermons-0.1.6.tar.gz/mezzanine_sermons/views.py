from datetime import date

from django.shortcuts import render

from mezzanine_sermons.models import Sermon, SermonSeries


def sermons(request):
    """
    Displays home sermon page containing:
    - today's sermon (if available)
    - past 5 sermons (if available)
    - next 5 sermons (if available)
    - sermon series list (if available)
    """
    sermon_today = Sermon.objects.filter(date=date.today())
    sermons_pastfive = Sermon.objects.filter(date__lt=date.today())[:5]
    sermons_nextfive = Sermon.objects.filter(date__gt=date.today())[:5]
    context = {'sermon_today': sermon_today, 'sermons_pastfive': sermons_pastfive,
               'sermons_nextfive': sermons_nextfive}
    return render(request, 'mezzanine_sermons/upcoming_and_recent_sermons.html', context)


def sermon_series_list(request):
    """
    Displays page containing list of all sermon series (if any)
    """
    sermon_series = SermonSeries.objects.filter().order_by('-start_date')
    context = {'sermon_series': sermon_series}
    return render(request, 'mezzanine_sermons/sermon_series_list.html', context)


def single_sermon_series(request, series_id):
    """
    Displays all the sermons from a given series
    """
    series = SermonSeries.objects.get(id=series_id)
    sermons = Sermon.objects.filter(series=series).order_by('date')
    context = {'series': series, 'sermons': sermons}
    return render(request, 'mezzanine_sermons/single_sermon_series.html', context)
