from utils import detector_utils as detector
from utils import pose_classification_utils as classifier
import Worker
import cv2
from multiprocessing import Queue, Pool, Process
from utils.detector_utils import WebcamVideoStream
import datetime
import gui;
from ServerRequester import ServerRequester as Requester
import numpy as np

frame_processed = 0
score_thresh = 0.18
video_source = 0
num_hands = 1;
width = 300
height = 200;
display = 1
num_worker = 5
queue_size = 15

if __name__ == '__main__':
    #making queues for process
    input_q = Queue(maxsize=queue_size)
    output_q = Queue(maxsize=queue_size)
    boxes_q = Queue(maxsize=queue_size)
    inferences_q = Queue(maxsize=queue_size)

    #camera initialization
    cap = WebcamVideoStream(src=video_source, width=width, height=height).start()

    # cap = cv2.VideoCapture(video_source)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = cap.size()
    # cap_params['im_width'] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # cap_params['im_height'] = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_params['score_thresh'] = score_thresh
    cap_params['num_hands_detect'] = num_hands
    print(cap_params)

    #initialize server requester
    requester = Requester(width=cap_params['im_width'], height=cap_params['im_height'])

    #Set poses for inference
    poses = []
    with open('poses.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if(line != ''):
                poses.append(line)
    print(poses)

    try:
        #making thread Pool for image process
        pool = Pool(num_worker, Worker.worker, (
            input_q, output_q, boxes_q, inferences_q, cap_params, frame_processed))

        pool.close()
        start_time = datetime.datetime.now()
        num_frames = 0
        fps = 0
        index = 0
        output_frame = None
        cropped_frame = None
        inferences = None
        #start process
        while True:
            #ret, frame = cap.read()
            frame = cap.read()
            frame = cv2.flip(frame, 1)
            index += 1

            if(not input_q.full() and frame is not None):
                input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                continue

            cv2.namedWindow('Hand Result', cv2.WINDOW_NORMAL)
            #cv2.namedWindow('Cropped', cv2.WINDOW_NORMAL)

            try:
                output_frame = output_q.get(timeout=1)
                box = boxes_q.get(timeout=1)
            except Exception as e:
                pass

            try:
                inferences = inferences_q.get_nowait()
            except Exception as e:
                pass

            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            num_frames += 1
            fps = num_frames / elapsed_time
            #print(fps)

            if (inferences is not None):
                gui.drawInferences(inferences, poses)
                max_idx = np.argmax(inferences)
                requester.setStatus(box, poses[max_idx])

            if (output_frame is not None):
                output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
                if (display):
                    detector.draw_fps_on_image("FPS : " + str(int(fps)), output_frame)
                    cv2.imshow('Hand Result', output_frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break


    except Exception as e:
        print('imhere')
        print(str(e))

    pool.terminate()
    #cap.stop()
    cv2.destroyAllWindows()



