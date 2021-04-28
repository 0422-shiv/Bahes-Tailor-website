"""bahes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
   path('superadmin/', admin.site.urls),
            ######## User urls start #############
    path('logout', auth_login.LogoutView.as_view(), name="logout"),
    path('', include(('homepage.urls', 'homepage'), namespace='homepage')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('survey/', include(('survey.urls', 'survey'), namespace='survey')),
    # =====================================
    # forgot pasword url
    # path('password-reset/', auth_login.PasswordResetView.as_view(template_name='account/forgot-password.html'),
    #                        name="PasswordReset"),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #                       template_name='account/password_reset_done.html'), name='password_reset_done'),
    #  path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
    #                        name='password_reset_confirm'),
    # path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
    #                        name='password_reset_complete'),
    # ======================================
    path('my-services/', include(('services.urls', 'services'), namespace='services')),
    path('contact-us/', include(('contactus.urls', 'contactus'), namespace='contactus')),
    path('find-products/', include(('findproducts.urls', 'findproducts'), namespace='findproducts')),
    path('find-supplier/', include(('findsupplier.urls', 'findsupplier'), namespace='findsupplier')),
    path('find-services/', include(('findservices.urls', 'findservices'), namespace='findservices')),
    path('custom/', include(('custom_app.urls', 'custom_app'), namespace='custom_app')),
    path('my-products/', include(('products.urls', 'products'), namespace='products')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
            ############ User urls end ##########


            ############## Admin urls start #############
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login/index.html'),name="admin_login"),
    path('admin/dashboard/', include(('admin_dashboard.urls', 'admin_dashboard'), namespace='admin_dashboard')),
    path('admin/manage-member/', include(('manage_member.urls', 'manage_member'), namespace='manage_member')),
    path('admin/manage-cms/', include(('manage_cms.urls', 'manage_cms'), namespace='manage_cms')),
    path('admin/manage-chat/', include(('manage_chat.urls', 'manage_chat'), namespace='manage_chat')),
    path('admin/manage-questions/', include(('manage_questions.urls', 'manage_questions'), namespace='manage_questions')),
    path('admin/manage-services/', include(('manage_services.urls', 'manage_services'), namespace='manage_services')),
    path('admin/manage-products/', include(('manage_products.urls', 'manage_products'), namespace='manage_products')),
    path('admin/manage-payments/', include(('manage_payments.urls', 'manage_payments'), namespace='manage_payments')),
    path('admin/manage-admin-settings/', include(('manage_admin_settings.urls', 'manage_admin_settings'), namespace='manage_admin_settings')),
     path('admin/manage-user-answers/', include(('manage_user_answers.urls', 'manage_user_answers'), namespace='manage_user_answers')),
            ############# Admin urls end ################


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
