from lisa_api.lisa.routers import DynamicRouter
from views import ShoppingListViewSet

DynamicRouter().register_endpoint(r'shopping', ShoppingListViewSet)
