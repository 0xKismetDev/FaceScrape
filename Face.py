import face_recognition # main lib
import glob # glob for all images in path
import cv2 # for drawing rectangle around target
import os # for removing image
import argparse # for arguments
import time # for logging 
from PIL import Image # for drawing rectangle around target


# argument parser
parser = argparse.ArgumentParser(
    description='Find a target face in scraped images.',
    epilog='Example: python main.py -t target.jpg -p "pics/*.jpg" -v true'
)
parser.add_argument('-t', '--target', help='Target face to find', required=True)
parser.add_argument('-p', '--path', help='Path to images', required=True)
parser.add_argument('-v', '--verbose', help='Verbose output')
args = parser.parse_args()

target = face_recognition.load_image_file(args.target)
target_encoding = face_recognition.face_encodings(target)[0]

# print log
def printlog(text):
    print("[" + time.strftime("%H:%M:%S") + "] " + text)

# find target
def find_target():
    # loop through all images in path
    for file in glob.glob(args.path):
        # load image
        unknown_image = face_recognition.load_image_file(file)
        if args.verbose not in ("false", "False", "FALSE", "f", "F"):
            printlog(file)
        try:
            # get encoding
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            # if no face found, continue
            continue
        # get face locations
        results = face_recognition.compare_faces([target_encoding], unknown_encoding)
        face_locations = face_recognition.face_locations(unknown_image)
        # if face found in image:
        if results[0] == True:
            printlog("Found Target! " + file)
            # draw image with rectangle around target with cv2
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(unknown_image, (left, top),
                              (right, bottom), (255, 0, 0), 2)
                pil_image = Image.fromarray(unknown_image)
                pil_image.save("target.jpg")
                # display image in cv2 window
                cv2.imshow("target", cv2.imread("target.jpg"))
                # destroy on keypress
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # remove image
                os.remove("target.jpg")
                break

                

if __name__ == "__main__":
    find_target()
    printlog("Done!")

