from imutils.video import VideoStream
from imutils.video import FPS
import argparse,imutils,time, cv2

ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",type=str,
	help="path to input video file")

ap.add_argument("-t","--tracker",type=str,default="kcf",
	help="path to input video file")

args= vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS={
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers= cv2.MultiTracker_create()

if not args.get("video",False):
	print("[INFO] starting video stream...")
	vs=VideoStream(src=0).start()
	time.sleep(1.0)

else:
	vs=cv2.VideoCapture(args["video"])


while True:
	frame= vs.read()
	frame= frame[1] if args.get("video",False) else frame

	if frame is None:
		break

	frame= imutils.resize(frame, width=600)

	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked

	(success,boxes) = trackers.update(frame)

	for box in boxes:
		(x,y,w,h)=[int(v) for v in box]
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

	cv2.imshow("Frame",frame)
	key=cv2.waitKey(1) & 0xFF

	if key== ord("s"):

# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)

		box= cv2.selectROI("Frame",frame,fromCenter=False,
			showCrosshair= True)

		tracker= OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		tracker.add(tracker,frame,box)

	elif key== ord("q"):
		break

if not args.get("video", False):
	vs.stop()
# otherwise, release the file pointer
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()















	
