#!/usr/bin/env python

'''
Copyright (c) 2016, Nadya Ampilogova
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# Script for simulation
# Launch gazebo world prior to run this script

from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time

listen_status = 1

class TakePhoto:
    def __init__(self):
        global listen_status
        pub.publish("The picture taking program starts to execute !")
        print("Robot: The picture taking program starts to execute !")
        rospy.sleep(2)

        self.bridge = CvBridge()
        self.image_received = False
        
        # Connect image topic
        img_topic = "/camera/rgb/image_raw"
        self.image_sub = rospy.Subscriber(img_topic, Image, self.callback)

        # Allow up to one second to connection
        rospy.sleep(1)

        rospy.Subscriber('/lm_data', String, self.take_photo)
        pub.publish("Waiting for your order...")
        print("Robot: Waiting for your order...")
        rospy.sleep(3)
        while True:
            rospy.wait_for_message('lm_data', String)
            print("You: " + self.order)


	    if self.order == 'INTRODUCE THE DISPLAY AREA':
		pub.publish('Now here we are at the display area. There are some texts on the walls, including system and the theory of software designing. You can help yourself and enjoy watching those interesting items related to software and computer system.')
	    if self.order == 'INTRODUCE THE SYSTEM AREA':
		pub.publish('Now we are at the system area. Here you can see some integrated applications of the computer system. On the walls, showing well-known allumni. JUst help youself and enjoy it!')

            if listen_status == 1:
		
                if self.order == "TAKE A PHOTO" or self.order == "TAKE A PICTURE" or self.order == "PLEASE TAKE A PHOTO" or self.order == "PLEASE TAKE A PICTURE":
                    listen_status = 2
                    cv2.imshow("The picture you took just now" , self.image)
                    cv2.waitKey(25)
                    pub.publish("Picture down ! Save or not ?")
                    print("Robot: Picture down ! Save or not ?")
                    rospy.sleep(4)
                else:
                    #pub.publish("I can't understand what you said just now. Please try it again !")
                    print("Robot: I can't understand what you said just now. Please try it again !")
                    rospy.sleep(6.5)
            else:
                if self.order == "YES" or self.order == "SAVE" or self.order == "SAVE IT" or self.order == "SAVE THE PICTURE" or self.order == "SAVE THE PHOTO" or self.order == "STORE" or self.order == "STORE IT" or self.order == "STORE THE PICTURE" or self.order == "STORE THE PHOTO":
                    listen_status = 1
                    cv2.destroyAllWindows()
                    timestr = time.strftime("%Y%m%d-%H%M%S-")
                    img_title = "/home/zhangshuo/Photos/" + timestr + "photo.jpg"
                    if self.take_picture(img_title):
                        pub.publish("OK, I have saved the picture as " + img_title)
                        print("Robot: OK, I have saved the picture as " + img_title)
                        rospy.sleep(10)
                    else:
                        pub.publish("Sorry, no images received !")
                        print("Robot: Sorry, no images received !")
                        rospy.sleep(3.5)
                elif self.order == "NO" or self.order == "CANCLE" or self.order == "CANCLE IT" or self.order == "CANCLE THE PICTURE" or self.order == "CANCLE THE PHOTO" or self.order == "REMOVE" or self.order == "REMOVE IT" or self.order == "REMOVE THE PICTURE" or self.order == "REMOVE THE PHOTO" or self.order == "DELETE" or self.order == "DELETE IT" or self.order == "DELETE THE PICTURE" or self.order == "DELETE THE PHOTO":
                    listen_status = 1
                    cv2.destroyAllWindows()
                    pub.publish("Cancled !")
                    print("Robot: Cancled!")
                    rospy.sleep(2)
                else:
                    #pub.publish("I can't understand what you said just now. Please try it again !")
                    print("Robot: I can't understand what you said just now. Please try it again !")
                    rospy.sleep(6.5)

    def callback(self, data):

        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image

    def take_picture(self, img_title):
        if self.image_received:
            # Save an image
            cv2.imwrite(img_title, self.image)
            return True
        else:
            return False

    def take_photo(self, msg):
        self.order = msg.data
 
if __name__ == '__main__':

    # Initialize
    pub = rospy.Publisher('answer', String, queue_size=10)
    rospy.init_node('take_photo', anonymous=False)
    TakePhoto()
 
    rospy.spin()
    # Sleep to give the last log messages time to be sent
    #rospy.sleep(1)
