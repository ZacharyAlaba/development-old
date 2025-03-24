# exam_views.py

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.views import View
import json
from .exam_models import Chat

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    def get(self, request):
        chats = Chat.objects.all()
        chat_data = [
            {
                "username": chat.username,
                "chat_message": chat.chat_message,
                "date": chat.date.isoformat(),
            }
            for chat in chats
        ]
        return JsonResponse(chat_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            chat_message = data.get('chat_message')

            if not username or not chat_message:
                return JsonResponse({"error": "Username and message are required."}, status=400)

            new_chat = Chat.objects.create(username=username, chat_message=chat_message)
            return JsonResponse({
                "username": new_chat.username,
                "chat_message": new_chat.chat_message,
                "date": new_chat.date.isoformat(),
            }, status=201)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format.", "details": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ChatUpdateDetailView(View):
    # Helper method to get a chat object by ID
    def get_object(self, chat_id):
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            raise Http404("Chat not found")

    # DELETE: Delete a chat by ID
    def delete(self, request, chat_id, *args, **kwargs):
        chat = self.get_object(chat_id)
        chat.delete()
        return JsonResponse({"message": "Chat successfully deleted"}, status=200)

    # PUT: Update a chat by ID
    def put(self, request, chat_id, *args, **kwargs):
        chat = self.get_object(chat_id)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

        # Update chat fields if provided
        chat.username = data.get('username', chat.username)
        chat.chat_message = data.get('chat_message', chat.chat_message)
        chat.save()

        return JsonResponse({
            "id": chat.id,
            "username": chat.username,
            "chat_message": chat.chat_message,
            "date": chat.date.isoformat(),
        }, status=200)

    # GET: Retrieve chat details by ID
    def get(self, request, chat_id, *args, **kwargs):
        chat = self.get_object(chat_id)
        return JsonResponse({
            "id": chat.id,
            "username": chat.username,
            "chat_message": chat.chat_message,
            "date": chat.date.isoformat(),
        }, status=200)
