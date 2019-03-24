from projectx_app.models.rpo import Country, CountryCode
def get_initial_values():
    initial_country_exist = False
    initial_country_code_exist = False
    initial_country = False
    initial_countrycode = False
    try:
        initial_country = Country.objects.get(country_name="India")
        initial_country_exist = True
        initial_countrycode = CountryCode.objects.get(country_code_name="+91")
        initial_country_code_exist = True
    except:
        print("===no contry or contry code=====")


    return initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode