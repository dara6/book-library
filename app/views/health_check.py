from fastapi import APIRouter

router = APIRouter(tags=['health-check'])


@router.get('/ping')
def ping():
    return 'pong'
