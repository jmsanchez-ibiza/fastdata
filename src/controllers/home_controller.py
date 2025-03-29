from src.views.home_views import clients_page, contact_page, home_page, news_page, services_page

def init_routes(rt):
    HomeControler(rt)


class HomeControler:
    
    def __init__(self, rt):
        self.rt = rt
        self.init_routes()
    
    def init_routes(self):
        self.rt("/")(self.home)
        self.rt("/home")(self.home)
        self.rt("/clients")(self.clients)
        self.rt("/services")(self.services)
        self.rt("/news")(self.news)
        self.rt("/contact")(self.contact)
        # self.rt("/clients")(self.clients)
        # self.rt("/clients_edit/{client_id}")(self.edit)
        # self.rt("/clients_delete/{client_id}")(self.delete)
        # self.rt("/client_post")(self.processs_post)
        # self.rt("/client_filter")(self.filter)
    

    def home(self, session, request):
        return home_page(session=session)
    
    def clients(self, session, request):
        return clients_page(session=session)
    
    def services(self, session, request):
        return services_page(session=session)
    
    def news(self, session, request):
        return news_page(session=session)
    
    def contact(self, session, request):
        return contact_page(session=session)