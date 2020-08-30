import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

# ref
# https://github.com/basler/pypylon/issues/72
# https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
# https://stackoverflow.com/questions/25359288/how-to-know-total-number-of-frame-in-a-file-with-cv2-in-python
# https://stackoverflow.com/questions/10475198/retrieving-the-current-frame-number-in-opencv

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.my_cap = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.my_cap.width, height = self.my_cap.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_stop_start=tkinter.Button(window, text="stop/start", width=50, command=self.stop_start)
        self.btn_stop_start.pack(anchor=tkinter.CENTER, expand=True)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15

        self.total_frame_num = self.my_cap.get_total_frame_num()
        self.w2 = tkinter.Scale(window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tkinter.HORIZONTAL)
        
        print(self.w2.get())
        self.w2.pack()
        self.count = 0
        self.count10 = 0
        self.start = 1
        self.fix_num = 0
        self.update()

        self.window.mainloop()

    def stop_start(self):
        self.my_cap.get_frame_num()
        if(self.start == 1):
            self.start = 0
            return
        if(self.start == 0):
            self.start = 1
            return

    # def snapshot(self):
    #     # Get a frame from the video source
    #     ret, frame = self.my_cap.get_frame()
 
    #     if ret:
    #         cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.my_cap.get_frame()

        if ret:
            self.count10 +=1
            if(self.start == 1):
                self.count += 1
            if(self.count10 % 10 == 0):
                self.count = self.w2.get()
            self.w2.set(self.count)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.my_cap.set_frame_in_video(self.count)
        self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        video_source = 'your_video_file_name.avi'
        self.vid = cv2.VideoCapture(video_source)
        frame_num = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        print('frame_num', frame_num)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            #self.vid.set(1,300)
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def get_frame_num(self):
        print(int(self.vid.get(cv2.CAP_PROP_POS_FRAMES)))
    def get_total_frame_num(self):
        return int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
    def set_frame_in_video(self, number):
        self.vid.set(1, number)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")


