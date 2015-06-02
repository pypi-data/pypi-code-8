from lisa_api.lisa.urls import router
from views import ShoppingListViewSet

router.register(r'shopping', ShoppingListViewSet)
