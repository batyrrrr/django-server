from core.repository.viewsets import RepositoryViewSet
from rest_framework.routers import SimpleRouter
from core.user.viewsets import UserViewSet
from core.auth.viewsets import (
    LoginViewSet,
    LogoutViewSet,
    RefreshViewSet,
    RegisterViewSet,
)

router = SimpleRouter(trailing_slash=False)
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/logout", LogoutViewSet, basename="auth-logout")
router.register(r"auth/user/profile", UserViewSet, basename="auth-user")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(f"repositories", RepositoryViewSet, basename="repositories")
urlpatterns = router.urls
