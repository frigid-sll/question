from rest_framework.routers import DefaultRouter
from myapp import views

router = DefaultRouter()
router.register('user',views.Manage_User,basename='user')
router.register('acquire',views.Acquire,basename='acquire')
router.register('handle',views.Handle,basename='handle')
router.register('download',views.Download,basename='download')

urlpatterns = router.urls