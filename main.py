from typing import Annotated

import yaml
import requests
from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/nodes/{node}/{stuff}")
def read_item(node: str, stuff: str):
    local_key = stuff
    with open(f"intended/structured_configs/{node}.yml", "r") as file:
        data = yaml.safe_load(file)
    return data[local_key]


@app.post("/custom/custom_interfaces")
async def c_interface(
    node: Annotated[str, Form()],
    interface_name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    vlan: Annotated[int, Form()],
    mode: Annotated[str, Form()],
    spanning: Annotated[str, Form()],
):
    with open(f"custom_interfaces/{node}.yml", "r") as file:
        data = yaml.safe_load(file)
        interface = {
            interface_name: {
                "description": description,
                "vlan": vlan,
                "mode": mode,
                "spanning": spanning,
            }
        }
        data.update(interface)
    if data:
        with open(f"custom_interfaces/{node}.yml", "w") as stuff:
            yaml.safe_dump(data, stuff)

    updates = {
        node: {
            interface_name: {
                "description": description,
                "vlan": vlan,
                "mode": mode,
                "spanning": spanning,
            }
        }
    }

    requests.post(
        "http://127.0.0.1:5000/endpoint",
        json={
            "message": f"Configure interfaces on {node}",
        },
    )

    return updates
