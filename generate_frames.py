import os
from utils import VideoHandler
import time

for file_path in os.listdir("peg videos"):
    s = time.time()
    name = os.path.splitext(file_path)[0]
    vid = VideoHandler("./peg videos/"+file_path, name=name)
    save_path = os.path.join("./peg frames", name)
    os.mkdir(save_path)
    vid.sample_from_vid(save_dir=save_path)
    e = time.time()
    print("completed video:", name, "in", e-s, "seconds")
