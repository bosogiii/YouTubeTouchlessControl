import tensorflow as tf
from utils import pose_classification_utils as classifier
from utils import detector_utils as detector
import os


def worker(input_q, output_q, cropped_output_q, inferences_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector.load_inference_graph()
    sess = tf.Session(graph=detection_graph)

    print(">> loading keras model for worker")
    try:
        model, classification_graph, session = classifier.load_KerasGraph("cnn/models/hand_poses_wGarbage_10.h5")
    except Exception as e:
        print(e)

    try:
        while True:
            # print("> ===== in worker loop, frame ", frame_processed)
            frame = input_q.get();
            if (frame is not None):
                # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
                # while scores contains the confidence for each of these boxes.
                # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)
                boxes, scores = detector.detect_objects(frame, detection_graph, sess)

                # get region of interest
                res = detector.get_box_image(cap_params['num_hands_detect'], cap_params["score_thresh"], scores, boxes, cap_params['im_width'], cap_params['im_height'], frame)

                # draw bounding boxes
                # res = detector.draw_box_on_image(cap_params['num_hands_detect'], cap_params["score_thresh"],
                #                                  scores, boxes, cap_params['im_width'], cap_params['im_height'], frame)

                # classify hand pose
                if res is not None:
                    class_res = classifier.classify(model, classification_graph, session, res)
                    inferences_q.put(class_res)

                    # add frame annotated with bounding box to queue
                cropped_output_q.put(res)
                output_q.put(frame)
                frame_processed += 1
            else:
                output_q.put(frame)
    except Exception as e:
        print(e)
        print("error in worker" + os.getpid())
    sess.close()