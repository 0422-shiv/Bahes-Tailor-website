# Import some useful packages.
from django.urls import path
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

# Define urls for User Application function.
urlpatterns = [
# path('change-password', views.ChangePassword.as_view(), name="ChangePassword"),
 path('',
         auth_view.PasswordChangeView.as_view(template_name='admin/manage-admin-settings/change-password.html',
                                              success_url=reverse_lazy('manage_admin_settings:ChangePassword')),
         name="ChangePassword"),
path('email-settings', views.EmailSettings.as_view(), name="EmailSettings"),
path('enquiries', views.ManageEnquiries.as_view(), name="ManageEnquiries"),
path('reply/<int:id>', views.EnquiryReply.as_view(), name="EnquiryReply"),
path('delete-enquiries/', views.DeleteMultiEnquiries.as_view(), name="DeleteMultiEnquiries"),
]