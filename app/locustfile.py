from locust import HttpUser, between, task

class MyUser(HttpUser):

    wait_time = between(1, 10)

    @task
    def get_country_list(self):
        self.client.get("/countrylist")
    
    @task
    def get_global_summary_small(self):
        self.client.get("/summary/global?start_date=2021-07-01&end_date=2021-07-12")

    @task
    def get_global_summary_all(self):
        self.client.get("/summary/global?start_date=2020-01-22&end_date=2021-07-12")

    @task
    def get_country_summary_small(self):
        self.client.get("/summary/country?country=Singapore&start_date=2021-07-01&end_date=2021-07-12")

    @task
    def get_country_summary_all(self):
        self.client.get("/summary/country?country=Singapore&start_date=2020-01-22&end_date=2021-07-12")

    @task
    def get_global_daily_small(self):
        self.client.get("/daily/global?start_date=2021-07-01&end_date=2021-07-12")

    @task
    def get_global_daily_all(self):
        self.client.get("/daily/global?start_date=2020-01-22&end_date=2021-07-12")

    @task
    def get_country_daily_small(self):
        self.client.get("/daily/country?country=Singapore&start_date=2021-07-01&end_date=2021-07-12")

    @task
    def get_country_daily_all(self):
        self.client.get("/daily/country?country=Singapore&start_date=2020-01-22&end_date=2021-07-12")
        