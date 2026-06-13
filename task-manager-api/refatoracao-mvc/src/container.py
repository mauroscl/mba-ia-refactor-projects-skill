from dependency_injector import containers, providers
from config.env import Config
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
from src.repositories.category_repository import CategoryRepository
from src.services.user_service import UserService
from src.services.task_service import TaskService
from src.services.category_service import CategoryService
from src.services.report_service import ReportService
from src.services.notification_service import NotificationService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.controllers"])

    config = providers.Object(Config)

    # Repositories
    user_repository = providers.Singleton(UserRepository)
    task_repository = providers.Singleton(TaskRepository)
    category_repository = providers.Singleton(CategoryRepository)

    # Services
    notification_service = providers.Singleton(
        NotificationService,
        config=config
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        task_repository=task_repository
    )

    task_service = providers.Factory(
        TaskService,
        task_repository=task_repository,
        user_repository=user_repository,
        category_repository=category_repository,
        notification_service=notification_service
    )

    category_service = providers.Factory(
        CategoryService,
        category_repository=category_repository
    )

    report_service = providers.Factory(
        ReportService,
        task_repository=task_repository,
        user_repository=user_repository,
        category_repository=category_repository
    )
