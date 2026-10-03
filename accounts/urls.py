<<<<<<< HEAD
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",register_view,name="register"),
    path("login/",login_view,name="login"),
    path("dashboard/",dashboard,name="dashboard"),
    path("logout/",logout_view,name="logout"),

=======
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",register_view,name="register"),
    path("login/",login_view,name="login"),
    path("dashboard/",dashboard,name="dashboard"),
    path("logout/",logout_view,name="logout"),

>>>>>>> 7159795b6044deffa8701f4b9b7a29f57ca8987b
]