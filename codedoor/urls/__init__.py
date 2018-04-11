from .applications import urlpatterns as application_urls
from .companies import urlpatterns as company_urls
from .reviews import urlpatterns as review_urls
from .profiles import urlpatterns as profile_urls
from .questions import urlpatterns as question_urls
from .root import urlpatterns as root_urls


app_name = 'codedoor'

urlpatterns = (
    application_urls +
    company_urls +
    profile_urls +
    question_urls +
    review_urls +
    root_urls
)
