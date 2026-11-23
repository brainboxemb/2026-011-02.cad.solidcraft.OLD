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
            "target": [0, 0, -18],
            "yaw": -0.45,
            "pitch": -1.35,
            "distance": 42,
            "fov": 0,
        },
    },
)
