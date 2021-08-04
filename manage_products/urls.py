# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.ManageProducts.as_view(), name="ManageProducts"),
path('delete-product/', views.DeleteMultiProducts.as_view(), name="DeleteMultiProducts"),
# ---------------------------------washing method urls----------------------------
path('washing-method/', views.WashingMethod.as_view(), name="WashingMethod"),
path('add-washing-method/', views.AddWashingMethod.as_view(), name="AddWashingMethod"),
path('edit-washing-method/<int:id>', views.EditWashingMethod.as_view(), name="EditWashingMethod"),
path('delete-washing-method/<int:id>', views.DeleteWashingMethod.as_view(), name="DeleteWashingMethod"),
# ----------------------------fabric type urls-------------------------
path('fabric-types/', views.FabricTypes.as_view(), name="FabricTypes"),
path('add-fabric-types/', views.AddFabricTypes.as_view(), name="AddFabricTypes"),
path('edit-fabric-types/<int:id>', views.EditFabricTypes.as_view(), name="EditFabricTypes"),
path('delete-fabric-types/<int:id>', views.DeleteFabricType.as_view(), name="DeleteFabricType"),
# ----------------------------Thread type urls-------------------------
path('thread-types/', views.ThreadTypes.as_view(), name="ThreadTypes"),
path('add-thread-types/', views.AddThreadTypes.as_view(), name="AddThreadTypes"),
path('edit-thread-types/<int:id>', views.EditThreadTypes.as_view(), name="EditThreadTypes"),
path('delete-thread-types/<int:id>', views.DeleteThreadType.as_view(), name="DeleteThreadType"),
# ----------------------------Thread type urls-------------------------
path('button-types/', views.ButtonTypes.as_view(), name="ButtonTypes"),
path('add-button-types/', views.AddButtonTypes.as_view(), name="AddButtonTypes"),
path('edit-button-types/<int:id>', views.EditButtonTypes.as_view(), name="EditButtonTypes"),
path('delete-button-types/<int:id>', views.DeleteButtonType.as_view(), name="DeleteButtonType"),

# ----------------------------Elastic type urls-------------------------
path('elastic-tape-trim-types/', views.ElasticTypes.as_view(), name="ElasticTypes"),
path('add-elastic-tape-trim-types/', views.AddElasticTypes.as_view(), name="AddElasticTypes"),
path('edit-elastic-tape-trim-types/<int:id>', views.EditElasticTypes.as_view(), name="EditElasticTypes"),
path('delete-elastic-tape-trim-types/<int:id>', views.DeleteElasticType.as_view(), name="DeleteElasticType"),

]