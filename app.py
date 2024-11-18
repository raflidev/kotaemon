import os
import sys
import gradio as gr

from theflow.settings import settings as flowsettings

KH_APP_DATA_DIR = getattr(flowsettings, "KH_APP_DATA_DIR", ".")
GRADIO_TEMP_DIR = os.getenv("GRADIO_TEMP_DIR", None)
# override GRADIO_TEMP_DIR if it's not set
if GRADIO_TEMP_DIR is None:
    GRADIO_TEMP_DIR = os.path.join(KH_APP_DATA_DIR, "gradio_tmp")
    os.environ["GRADIO_TEMP_DIR"] = GRADIO_TEMP_DIR


from ktem.main import App  # noqa

deploy = App()
demo = deploy.make()
# demo.queue().launch(
#     favicon_path=deploy._favicon,
#     inbrowser=True,
#     allowed_paths=[
#         "libs/ktem/ktem/assets",
#         GRADIO_TEMP_DIR,
#     ],
# )

import uvicorn
from fastapi import FastAPI


app = FastAPI()
# app.include_router(whoami_router.router)

app = gr.mount_gradio_app(app, demo.queue(), path="/")

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=8080)
