from picamzero import Camera

cam = Camera()
cam.start_preview()
cam.take_photo("~/Desktop/new_image.jpg")
cam.stop_preview()