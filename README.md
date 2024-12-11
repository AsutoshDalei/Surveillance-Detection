# SurveilAI

SurveilAI is a project that leverages local CCTV camera footage for real-time object detection using cutting-edge computer vision and deep learning techniques. By integrating tools such as OpenCV, YOLOv5 (PyTorch), and RTSP streaming, this application is designed to revolutionize the way surveillance footage is monitored, analyzed, and acted upon. The aim is to automate the detection process, enhancing security monitoring with minimal human intervention.

## Idea Behind SurveilAI

The primary goal of SurveilAI is to modernize surveillance systems by adding intelligent object detection capabilities. Traditionally, security personnel or users would have to manually sift through hours of CCTV footage, which is time-consuming and inefficient. SurveilAI addresses this challenge by incorporating AI-driven real-time object detection, enabling automatic identification of objects, people, vehicles, and more in live video streams. This ensures that security teams or individuals can monitor the environment with greater precision, respond quickly to potential threats, and reduce the time spent on manual footage review. 

This system can be used in various environments like residential complexes, commercial spaces, and public areas, providing a scalable solution to security concerns. SurveilAI aims to not only detect objects but also to eventually include features like alerts and detailed analytics for further enhancing decision-making capabilities.

## Technologies Used

### OpenCV
OpenCV (Open Source Computer Vision Library) is utilized for capturing and processing RTSP video feeds. It plays a crucial role in real-time video manipulation and frame extraction, enabling seamless integration with YOLOv5 for object detection.

### YOLOv5
YOLOv5 (You Only Look Once, version 5) is a state-of-the-art, pre-trained deep learning model designed for fast and accurate object detection. YOLOv5 is ideal for real-time applications, detecting multiple objects in a single frame with impressive speed and accuracy. It is implemented in PyTorch, providing a robust platform for deep learning and further model fine-tuning.

### PyTorch
PyTorch is the deep learning framework used for implementing YOLOv5. Its dynamic computation graph allows for flexibility and quick iterations when training or adjusting models. PyTorch's simplicity and efficiency make it the perfect choice for the YOLOv5 implementation.

### RTSP (Real-Time Streaming Protocol)
RTSP is used to stream live video footage from CCTV cameras into the application. OpenCV captures and processes these video feeds in real time, enabling object detection without delay.

### Streamlit
Streamlit is being used to build the user-friendly, interactive interface for SurveilAI. It allows for easy deployment of the object detection system, providing users with real-time video streams, with object annotations, directly in their web browser.

## Future Enhancements

- **Streamlit Interface Development**: Currently under development, the Streamlit app will eventually provide users with an intuitive, interactive dashboard for monitoring live video feeds and viewing detected objects in real-time. The goal is to offer features like user authentication, customizable detection thresholds, and the ability to handle multiple video feeds simultaneously.
  
- **Custom Object Detection**: In the future, SurveilAI will allow users to train YOLOv5 for detecting custom objects. This feature would be particularly useful for specialized use cases, such as detecting specific products, animals, or vehicles.

- **Alert System**: A notification system will be integrated to alert users when certain objects are detected. For example, the system could trigger an alert when a person enters a restricted area or when a vehicle is detected at an unusual hour.

- **Historical Data Analytics**: The project aims to add capabilities for storing and analyzing historical footage. This would allow users to identify trends or patterns in detected objects over time, helping to predict potential security issues or simply analyze traffic and movement within a monitored area.

- **Scalability and Performance Optimization**: Enhancing the performance of object detection, especially when dealing with high-definition, multi-camera setups, will be a key focus. The system will be optimized for scalability, ensuring that it can handle larger surveillance networks efficiently.

With these ongoing and future enhancements, SurveilAI is to transform AI-powered surveillance, making security monitoring more efficient, proactive, and data-driven.
