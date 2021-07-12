import os, thycotic

ss = thycotic.Api(
    os.environ.get("THYCOTIC_USER"),
    os.environ.get("THYCOTIC_PASS"),
    os.environ.get("THYCOTIC_URL"),
)
