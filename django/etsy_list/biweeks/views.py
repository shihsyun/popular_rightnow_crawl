# Create your views here.
from django.shortcuts import render
from pymongo import MongoClient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.core.cache import cache
from django.views.generic import TemplateView


class Allview(TemplateView):

    template_name = 'biweeks/home.html'

    def get(self, request):
        tmp = []
        today = datetime.date.today()
        for i in range(14):
            tmp.append(str(today - datetime.timedelta(days=i)))

        cache_key = 'biweeks_data'
        cache_time = 300
        total_results = cache.get(cache_key)
        if not total_results:
            db_client = MongoClient('mongodb://mongodb:27017')
            db = db_client['etsy']
            collect = db['popular_rightnow']
            total_results = list(collect.find({'appeardate': {'$in': tmp}}))
            cache.set(cache_key, total_results, cache_time)

        page = request.GET.get('page', 1)
        paginator = Paginator(total_results, 20)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, self.template_name, locals())
