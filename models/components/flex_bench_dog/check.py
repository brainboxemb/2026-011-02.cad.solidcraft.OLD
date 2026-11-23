"""Native snapshot settings owned by the FlexBenchDog model."""

SNAPSHOT_CAMERA = {
    "target": [0, 0, 0],
    "yaw": -0.40,
    "pitch": 0.25,
    "distance": 90,
    "fov": 0,
}

EXTRA_SNAPSHOTS = (
    {
        "name": "underside.png",
        "camera": {
            "target": [0, 0, -12],
            "yaw": -0.55,
            "pitch": -1.20,
            "distance": 70,
            "fov": 0,
        },
    },
)
