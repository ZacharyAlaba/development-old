from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactListView, ContactUpdateDetailView
from .product_views import ProductViewSet, CartViewSet, CheckoutViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'checkout', CheckoutViewSet)


urlpatterns = [
    #path('students/', Students.as_view(), name='list_student'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    path('exam/', include('api.exam_urls')),
    path('', include(router.urls)),

]

