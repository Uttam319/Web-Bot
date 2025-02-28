from booking.booking import Booking


with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency='USD')
    bot.select_place_to_go(input("Where you want to go ?"))
    bot.select_dates(check_in_date=input("What is the check in date ?"),
                     check_out_date=input("What is the check out date ?"))
    bot.select_adults(int(input("How many people ?")))
    bot.click_search()
    bot.apply_filtrations()
    bot.refresh()  # A workaround to let our bot to grab the data properly
    bot.report_results()
