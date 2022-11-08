from django.contrib import admin
from django.urls import path
from a1 import views as a1_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rm_aaa/', a1_views.Rm_Aaa, name='rm_aaa'),
    path('rst_cfg_ise/', a1_views.Reset_config_ISE_page, name='rst_cfg_ise'),
    path('success/', a1_views.SuccessPage, name='success'),
    path('sgt/', a1_views.SGTPage, name='sgt'),
    path('tacacs/', a1_views.TacacsPage, name='tacacs'),
    path('radius/', a1_views.RadiusPage, name='radius'),
    path('home/', a1_views.HomePage, name='home'),
    path('', a1_views.BasePage, name='base'),
]
