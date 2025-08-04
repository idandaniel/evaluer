def create_app_router():
    from fastapi import APIRouter

    from evaluer.api.routers import course, grades

    router = APIRouter()

    router.include_router(course.router)
    router.include_router(grades.router)

    return router