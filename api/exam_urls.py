from django.urls import path
from .exam_views import ChatView, ChatUpdateDetailView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat_view'),
    path('chats/<int:chat_id>/', ChatUpdateDetailView.as_view(), name='chat_update_detail'),
]