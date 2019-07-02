from .common import GraphHopperServer


gh_server = GraphHopperServer(
    default_params=[
        ("locale", "ru"),
        ("points_encoded", False),
        ("instructions", False)],
    host="http://127.0.0.1",
    port=8989
)

API_KEY = "t5tydKgF5Iy3JTyzQgVmOFwuKz80lB7H0iNeYpGxQUcsfpSzweUIeH6ZFPBIBq"