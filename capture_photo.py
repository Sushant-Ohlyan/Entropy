# elif (osi.conditioner(1, text, "!picture", 1) == "true"):
#             videoCaptureObject = cv2.VideoCapture(0)
#             result = True
#             while(result):
#                 ret, frame = videoCaptureObject.read()
#                 cv2.imwrite("pic.png", frame)
#                 result = False
#             videoCaptureObject.release()
#             cv2.destroyAllWindows()
#             processed_text = "pic.png"
#             return send_file(processed_text, mimetype='image/gif')