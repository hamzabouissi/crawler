from .tasks import search
from celery import group
from datetime import date,timedelta
from collections import defaultdict

def boot():

    urls,period,daterange_int = [],3,3
    start_date = date.today()+timedelta(weeks=1)

    for _ in range(0,daterange_int):
        final_date = start_date+timedelta(period)
        urls.append([f"https://www.booking.com/searchresults.en-us.html?label=gen173nr-1FCAEoggI46AdIM1gEaOIBiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAIDuALaouPrBcACAQ&sid=6a14e78eff418140472303415012548e&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaOIBiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAIDuALaouPrBcACAQ%3Bsid%3D6a14e78eff418140472303415012548e%3Bsb_price_type%3Dtotal%26%3B&ss=Mecca&is_ski_area=0&ssne=Mecca&ssne_untouched=Mecca&dest_id=-3096949&dest_type=city&checkin_month={start_date.month}&checkin_monthday={start_date.day}&checkin_year={start_date.year}&checkout_month={final_date.month}&checkout_monthday={final_date.day}&checkout_year={final_date.year}&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1",start_date.strftime("%Y-%m-%d"),final_date.strftime("%Y-%m-%d")])
        start_date+=timedelta(1)
    return urls

if __name__=='__main__':
    urls = boot()
    search.delay(urls[0])
    #s = group(search.s(url) for url in urls)()

