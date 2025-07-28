def create_app_router():
    from fastapi import APIRouter

    from evaluer.api.routers import subjects, modules, students

    router = APIRouter()

    router.include_router(subjects.router)
    router.include_router(modules.router)
    router.include_router(students.router)

    return router


__all__ = ["create_app_router"]
