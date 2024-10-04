from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.cache import cache
from .models import Item
import json

# Create your views here.
def retrieve(self, request, *args, **kwargs):
    item_id = kwargs.get('pk')
    cached_item = cache.get(f'item_{item_id}')
    if cached_item:
        return Response(cached_item)

    instance = self.get_object()
    serializer = self.get_serializer(instance)
    cache.set(f'item_{item_id}', serializer.data, timeout=60*15)  # Cache for 15 minutes
    return Response(serializer.data)

# Create Items
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Check if an item with the same name already exists
            if Item.objects.filter(name=data.get('name')).exists():
                return JsonResponse({"error": "Item already exists"}, status=400)

            # Create the item if it is not exist. 
            item = Item.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                quantity=data.get('quantity'),
                price=data.get('price')
            )
            return JsonResponse({"message": "Item created successfully", "item": item.id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error creating item: {e}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Read Item List
@permission_classes([IsAuthenticated])
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all().values()
        return JsonResponse(list(items), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Update Items
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_item(request, pk):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Item, pk=pk)
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.quantity = data.get('quantity', item.quantity)
            item.price = data.get('price', item.price)
            item.save()
            return JsonResponse({"message": "Item updated successfully"}, status=200)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error updating item: {e}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Delete items
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_item(request, pk):
    if request.method == 'DELETE':
        try:
            item = get_object_or_404(Item, pk=pk)
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error deleting item: {e}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)