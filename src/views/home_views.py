from fasthtml.common import *
from src.auth.login import is_user_admin, is_user_logged
from src.core.html_wrappers import *
from src.config import NAVBAR_BG_COLOR, APP_NAME
from src.utils.js_scripts import bootstrap_tooltips_js

# ------------------------------------------------------------------------ #
# Helper form
def helper_modal():
    return \
    Div(id='exampleModal', tabindex='-1', aria_labelledby='exampleModalLabel', aria_hidden='true', cls='modal fade')(
        Div(cls='modal-dialog')(
            Div(cls='modal-content')(
                Div(cls='modal-header')(
                    H1('Your Attention !!', id='exampleModalLabel', cls='modal-title fs-5'),
                    Button(type='button', data_bs_dismiss='modal', aria_label='Close', cls='btn-close')
                ),
                Div(cls='modal-body')(
                    Card(
                        H5("Modal body..."),
                        H6("This is a simple modal to show how to use it."),
                        P("You can put any content you want here."),
                    )
                ),
                Div(cls='modal-footer')(
                    Button('Cancel', type='button', data_bs_dismiss='modal', cls='btn btn-secondary mx-1'),
                    Button('Ok', type='button', cls='btn btn-primary mx-1')
                )
            )
        )
    )
# ------------------------------------------------------------------------ #

# Options menu
def menu(session):
    
    # If not logged in, display the visitor website.
    if not is_user_logged(session):

        ret = Ul(cls='navbar-nav me-auto ml-4 mb-2 mb-md-0')(
            Li(cls='nav-item')(
                A('Clients', href='/clients_page', cls='nav-link text-primary', hx_get='/clients_page', hx_target='#main-content'),
            ),
            Li(cls='nav-item')(
                A('Services', href='/services', cls='nav-link text-primary', hx_get='/services', hx_target='#main-content')
            ),
            Li(cls='nav-item')(
                A('News', href='/news', cls='nav-link text-primary', hx_get='/news', hx_target='#main-content')
            ),
            Li(cls='nav-item')(
                A('Contact', href='/contacs', cls='nav-link text-primary', hx_get='/contact', hx_target='#main-content')
            ),
        )

    else:  # We have login, now handle the 'user-role'.
        ret =  Ul(cls='navbar-nav me-auto ml-4 mb-2 mb-md-0')(
            
            Li(cls="nav-item px-1")(
                A(cls="nav-link text-primary icon-link icon-link-hover",
                    hx_get="/users", hx_target="#main-content",
                    title="User Management.\nManagement of the application's user list.", data_bs_placement='bottom')(
                        I(cls="bi-person-circle text-primary"),"Users",
                    ),
            ) if is_user_admin(session) else "",   # Only showed if user has admin role

            Li(cls='nav-item px-1')(
                A(cls='nav-link text-primary icon-link icon-link-hover',
                    hx_get='/clients', hx_target='#main-content',
                    title='Customers Management.\nManagement of your customers.', data_bs_placement='bottom')(
                        I(cls="bi-person-lines-fill text-primary"),
                        'Customers',
                    ),
            ),
            
            Li(cls='nav-item dropdown')(
                A(data_bs_toggle='dropdown', aria_expanded='false', cls='nav-link dropdown-toggle text-primary')('Dropdown'),
                Div(cls='dropdown-menu', style=f'background-color: {NAVBAR_BG_COLOR};')(
                    A('Action 1', href='#', cls='dropdown-item text-primary'),
                    A('Action 2', href='#', cls='dropdown-item text-primary'),
                    A('Action 3', href='#', cls='dropdown-item text-primary'),
                    Div(cls='dropdown-divider'),
                    A(cls='dropdown-item text-primary', href="#", title="Reports")(
                            I(cls="bi-journals text-primary"),Span(cls="px-1")("Reports"),
                        ),
                ),
            ),

        )

    return ret

# Login area
# If the user is logged in, show the logout button and the user name.
def login_area(session):
    if is_user_logged(session):
        # We are lgged in, show the logout option
        ret = A(cls='nav-link icon-link icon-link-hover pr-2',
            href="/logout",
            data_bs_toggle='tooltip',
            title='Cerrar la sessión', data_bs_placement='bottom')(
                Button(cls="btn btn-danger p-1 m-0")(
                    I(cls="bi-person-x fs-4 mx-1"),
                    Span(f"{session['user']['username']}\n{session['user']['role']}"),
                ),
        )
    else: # No authenticated
        ret = A(cls='nav-link icon-link icon-link-hover pr-2',
            href="/login",
            hx_get='/login', hx_target='#main-content',
            data_bs_toggle='tooltip',
            title='Users Login', data_bs_placement='bottom')(
                Button(cls="btn btn-success p-1 m-0")(
                    I(cls="bi-person-check fs-4 mx-1"),
                    Span("Login"),
                ),
        )
    
    return ret

# Navbar
def navbar(title, session):
    return Header(
    Nav(id="main-navbar")(
        Div(cls='container-fluid')(
            
            # Logo
            A(cls='navbar-brand', href='/home')(
                I(cls="bi bi-recycle fs-1 fs-bold text-primary"),
            ),

            # App's name
            A(title, href='/home', cls='navbar-brand ml-0 mr-4 text-primary fs-2 fw-bold'),
    

            # 'Hamburger' menu button
            # This button is only shown on small screens.
            Button(
                type='button',
                data_bs_toggle='collapse', data_bs_target='#my-navbar',
                aria_controls='my-navbar', aria_expanded='false', aria_label='Cambar navegación',
                cls='navbar-toggler')(
                Span(cls='navbar-toggler-icon')
            ),

            Div(id='my-navbar', cls='collapse navbar-collapse w-full')(
                
                # Options menu
                # This is the main menu of the application.
                menu(session),
                
                # Login Area
                login_area(session),
                
            ),
        )
    )
)

# main-content -> body_content
def body_content():
    # Main Content
    return  \
    Div(cls='col-sm-8 py-5 mx-auto')(
        H1('ACME COMPANY'),
        P(cls='fs-5')(
            'Experts in providing the best service.',
        ),
        P("Our company is a leader in its sector within your community, with 40 years of experience in the industry."),
        P("We use cutting-edge technology and state-of-the-art equipment to deliver exceptional results in every project. Innovation and precision at your home's service."),

        P(
            # Open Modal Form Example
            # This is a simple modal to show how to use it.
            Button('Contact us', type='button', data_bs_toggle='modal', data_bs_target='#exampleModal', cls='btn btn-primary'),
        ),
    )

# main-content
def main_content():
    # Main Content
    return \
    Div(
        id='main-content',
        cls='p-2 rounded',
        style='background-color: gainsboro;'
        )(
        body_content()
    )

# Footer
def footer():
    # Footer
    return Footer(cls="p-1", style=f"position:fixed; left: 0; bottom: 0; width: 100%; text-align: center; background-color: {NAVBAR_BG_COLOR};")(
        Div(cls="d-flex justify-content-around")(
            Span(cls="text-secondary")(f"© 2024 {APP_NAME}. All rights reserved."),
            Button(
                cls="btn btn-danger p-1 m-2",
                onclick=f"scrollToId('main-navbar')")(
                    I(cls="bi-arrow-up-square"), title="Go to top..",
            )
        )
    )

# Home-Page
def home_page(session, body_content: str = ""):
    return Div(cls="")(
        navbar(APP_NAME, session),
        main_content() if not body_content else body_content,
        footer(),
        helper_modal(),
        bootstrap_tooltips_js,
    )

# Since the requests arrive here via an hx-get, the target  
# will be #main-content from home_page, so we need to
# return only the portion for that main-content

# Clients
def clients_page(session):
    ct1 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('CLIENTS'),
        P(cls='fs-5')(
            '40 years by your side, like family',
        ),
        P("For four decades we've grown alongside our clients, delivering tailored solutions with the warmth of a family business. We take pride in earning generation-after-generation trust, always keeping our core values: personalized care, flawless quality and true commitment. Your satisfaction is our greatest endorsement. Discover why so many families choose us day after day."),
    )
    return ct1

# Services
def services_page(session):
    ct1 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('SERVICES'),
        P(cls='fs-5')(
            'We care for every detail of your home',
        ),
        P("We provide comprehensive solutions for your home’s upkeep and enhancement: from professional cleaning and repairs to renovations and gardening. Our skilled team delivers personalized service, using quality materials and meticulous attention. Whether a quick fix or a full project, we adapt to your needs with flexibility and professionalism. Because your home deserves the best care—backed by 30 years of trusted experience."),
    )
    return ct1

# News
def news_page(session):
    ct1 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('NEWS'),
        P(cls='fs-5')(
            'Stay updated with our latest news',
        ),
        P("In this section, you’ll find the latest news, tips, and trends on home care. We share standout projects, special promotions, and insightful articles to keep your home in perfect shape. Subscribe to stay tuned for our updates and discover how we can make your home more functional and welcoming. Every tip we share is backed by 30 years of hands-on experience."),
    )
    return ct1

# Contact
def contact_page(session):
    ct1 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('CONTACT US'),
        P(cls='fs-5')(
            "Let's talk - we're here to help",
        ),
        P("Need advice or want to request our services? Reach us by phone, email, or visit our offices. Our team will address all your inquiries with the personalized attention that defines us. Contact us for free estimates or any questions. For 30 years, we've been close to our clients, and your home will be our priority. We look forward to hearing from you!"),
    )
    return ct1

