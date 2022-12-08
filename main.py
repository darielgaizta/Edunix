from fastapi import FastAPI

import uvicorn

# App routers
from auth import routers as AuthRouter
from user import routers as UserRouter
from note import routers as NoteRouter
from news import routers as NewsRouter
from story import routers as StoryRouter

app = FastAPI()

app.include_router(AuthRouter.router)
app.include_router(UserRouter.router)
app.include_router(NoteRouter.router)
app.include_router(NewsRouter.router)
app.include_router(StoryRouter.router)

if __name__ == '__main__':
	uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)