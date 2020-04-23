


from imutils.video import VideoStream
from imutils.video import FPS
import argparse,imutils,time, cv2

ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",type=str,
	help="path to input video file")

ap.add_argument("-t","--tracker",type=str,default="kcf",
	help="path to input video file")

#KCF Tracker: Kernelized Correlation Filters.

args= vars(ap.parse_args())

(major,minor)= cv2.__version__.split(".")[:2]

if int(major)==3 and int(minor)<3:
	tracker= cv2.Tracker_create(args["tracker"].upper())

else:
	OPENCV_OBJECT_TRACKERS={
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
	
	}

	tracker= OPENCV_OBJECT_TRACKERS[args["tracker"]]()


# initialize the bounding box coordinates of the object
# we are going to track

initBB= None

if not args.get("video",False):
	print("[INFO] starting video stream...")
	vs=VideoStream(src=0).start()

else:
	vs=cv2.VideoCapture(args["video"])

fps=None

while True:
	frame= vs.read()
	frame= frame[1] if args.get("video",False) else frame

	if frame is None:
		break

	frame= imutils.resize(frame, width=500)
	(H,W)= frame.shape[:2]

# check to see if we are currently tracking an object
	if initBB is not None:
		(success,box) = tracker.update(frame)

		if success:
			(x,y,w,h)=[int(v) for v in box]

			cv2.rectangle(frame,(x,y),(x+w,y+h),
				(0,255,0),2)

		fps.update()
		fps.stop()

# initialize the set of information we'll be displaying on
		# the frame

		info=[
			("Tracker",args["tracker"]),
			("Success","YES" if success else "No"),
			("FPS","{:.2f}".format(fps.fps())),

		]

		for(i,(k,v)) in enumerate(info):
			text="{}:{}".format(k,v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


	cv2.imshow("Frame",frame)
	key= cv2.waitKey(1) & 0xFF

# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key== ord("s"):
# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)

		initBB= cv2.selectROI("Frame",frame,fromCenter=False,
			showCrosshair= True)

		tracker.init(frame,initBB)
		fps=FPS().start()

	elif key == ord("q"):
		break

if not args.get("video",False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()































