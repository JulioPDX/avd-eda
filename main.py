from typing import Annotated

import yaml
import json
from fastapi import Body, FastAPI, Form
from pydantic import BaseModel, Field

app = FastAPI()


class Interface(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=30
    )
    vlan: int = Field(gt=1, description="Please enter VLAN number")
    mode: str | None = "access"
    spanning: str | None = "edge"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/nodes/{node}/{stuff}")
def read_item(node: str, stuff: str):
    local_key = stuff
    with open(f"intended/structured_configs/{node}.yml", "r") as file:
        data = yaml.safe_load(file)
    return data[local_key]


# @app.put("/nodes/{node}/custom_interfaces")
# async def update_item(node: str, item: Annotated[Interface, Body(embed=True)]):
#     # results = {"item_id": item_id, "item": item}
#     local_key = "custom_interfaces"
#     with open(f"intended/structured_configs/{node}.yml", "r+") as file:
#         data = yaml.safe_load(file)
#     if data[local_key]:
#         pass

#     return data[local_key]


@app.post("/nodes/custom_interfaces")
async def c_interface(
    node: Annotated[str, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    vlan: Annotated[int, Form()],
    mode: Annotated[str, Form()],
    spanning: Annotated[str, Form()],
):
    local_key = "custom_interfaces"
    with open(f"intended/structured_configs/{node}.yml", "r") as file:
        data = yaml.safe_load(file)
        interface = {name: {description, vlan, mode, spanning}}
        data["custom_interfaces"].update(interface)
    if data:
        with open(f"intended/structured_configs/{node}.yml", "w") as file:
            yaml.safe_dump(data, file)
    return data[local_key]
