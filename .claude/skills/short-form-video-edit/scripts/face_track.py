#!/usr/bin/env python3
"""Track the speaker's face in a 1080x1920 video (run it on the video exactly as it will appear under the overlays).
  face_track.py IN.mp4 OUT_faces.js [--fps 5]
Writes window.FACES = {fps, boxes:[[x,y,w,h], ...]}: one PADDED head box per sample (face + hair/headwear + chin),
gaps filled from neighbours, smoothed. The engine uses it to keep every animation off the face.
Detector: OpenCV YuNet (handles 3/4 profiles), falls back to Haar frontal+profile."""
import sys, json, argparse, os, cv2, numpy as np
ap=argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--fps",type=float,default=5)
A=ap.parse_args()
here=os.path.dirname(os.path.abspath(__file__)); model=os.path.join(here,"..","assets","models","face_detection_yunet_2023mar.onnx")
cap=cv2.VideoCapture(A.video); vfps=cap.get(cv2.CAP_PROP_FPS) or 30; W=int(cap.get(3)); H=int(cap.get(4))
SC=0.4  # detect on a downscaled frame for speed
yn=cv2.FaceDetectorYN.create(model,"",(int(W*SC),int(H*SC)),0.6,0.3,50) if os.path.exists(model) else None
haar=[cv2.CascadeClassifier(cv2.data.haarcascades+f) for f in ("haarcascade_frontalface_default.xml","haarcascade_profileface.xml")]
step=max(1,round(vfps/A.fps)); raw=[]; i=0
while True:
    ok=cap.grab()
    if not ok: break
    if i%step==0:
        _,fr=cap.retrieve(); sm=cv2.resize(fr,(int(W*SC),int(H*SC))); best=None
        if yn is not None:
            _,f=yn.detect(sm)
            if f is not None and len(f): b=max(f,key=lambda r:r[2]*r[3]); best=[float(v)/SC for v in b[:4]]
        if best is None:
            g=cv2.cvtColor(sm,cv2.COLOR_BGR2GRAY); c=[]
            for hc in haar: c+=list(hc.detectMultiScale(g,1.1,4))
            c+=[(sm.shape[1]-x-w,y,w,h) for (x,y,w,h) in haar[1].detectMultiScale(cv2.flip(g,1),1.1,4)]
            if c: b=max(c,key=lambda r:r[2]*r[3]); best=[v/SC for v in b]
        raw.append(best)
    i+=1
n=len(raw); found=[k for k in range(n) if raw[k]]
if not found: sys.exit("no face found — check the video")
for k in range(n):  # fill gaps with the nearest detection
    if raw[k] is None: raw[k]=raw[min(found,key=lambda j:abs(j-k))]
arr=np.array(raw); sm=np.array([np.median(arr[max(0,k-2):k+3],axis=0) for k in range(n)])  # median smoothing
boxes=[]
for x,y,w,h in sm:  # pad: headwear/hair above, chin below, a little on the sides
    px,pt,pb=w*.30,h*.55,h*.25; boxes.append([round(max(0,x-px)),round(max(0,y-pt)),round(min(W,x+w+px)-max(0,x-px)),round(min(H,y+h+pb)-max(0,y-pt))])
open(A.out,"w").write("window.FACES="+json.dumps({"fps":A.fps,"boxes":boxes})+";\n")
print(f"{n} samples, detected in {len(found)} ({100*len(found)//n}%), median box {np.median(np.array(boxes),axis=0).astype(int).tolist()}")
