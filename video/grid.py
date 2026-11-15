import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]; items = sys.argv[2:]; ins = []
for i, it in enumerate(items):
    f, t = it.rsplit("@", 1); p = f"{H}/check/_{i}.jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", f"{H}/{f}", "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "4", p], check=True); ins += ["-i", p]
n = len(items); lay = "|".join(f"{(i%2)*960}_{(i//2)*540}" for i in range(n))
subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", f"xstack=inputs={n}:layout={lay}:fill=black", "-q:v", "3", f"{H}/check/{out}"], check=True)
