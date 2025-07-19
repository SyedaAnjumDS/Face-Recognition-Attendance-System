# Face-Recognition-Attendance-System

A real-time face recognition-based attendance system built with Python, Streamlit, OpenCV, face_recognition, and Pandas, which uses a webcam to detect and recognize faces and automatically logs attendance into an Excel file.
This app provides a user-friendly web interface to manage attendance, add new faces, view records, and control when attendance is captured.

**Key Features:**

Real-time face detection and recognition via webcam.

Attendance marking on button press: attendance is only recorded while "Activate Attendance" is enabled.

Automatic attendance logging into an Excel file (Attendance_Record.xlsx) with name, date, and time.

Capture new faces directly from webcam and save them for future recognition.

Web interface using Streamlit for easy interaction without command-line operations.

Prevents duplicate attendance in a single session.

View attendance records inside the app or export the Excel file.


**How it Works:**

1. Load Known Faces:
Known face images are stored inside the known_faces/ folder, organized by folder name (person’s name).
The system loads and encodes all faces at startup.

2. Capture New Faces:
Use the "Capture New Face" checkbox in the sidebar.
Enter the person’s name and click "Capture and Save Face" to take a photo using the webcam.
The image is saved into a folder under known_faces/Name/ and will be included in future recognitions.

3. Taking attendance:
Click "Activate Attendance" in the sidebar to start the camera.
The system scans faces in real-time.
When a known face is recognized, attendance is marked once per session (avoiding duplicates), recording name, date, and time into Attendance_Record.xlsx.
Press "Deactivate Attendance" to stop the camera.

4. Viewing attendance:
Click "View Attendance" in the sidebar to display the Excel attendance log inside the app.



**Technology Used:**

--Python 3.x

--Streamlit – UI framework

--OpenCV – webcam and image processing

--face_recognition – face detection & encoding

--Pandas – Excel file handling

--NumPy

--datetime – timestamp management


**Sample screenshots of the app:**
<img width="1920" height="1080" alt="Screenshot (42)" src="https://github.com/user-attachments/assets/81cd3024-a409-4ab7-9df3-8ac5bafc92a0" />
<img width="1920" height="1080" alt="Screenshot (43)" src="https://github.com/user-attachments/assets/96a6719f-4a52-4590-a909-65a2cdcd5ef8" />
<img width="1920" height="1080" alt="Screenshot (43)" src="https://github.com/user-attachments/assets/678f9db4-3a92-428a-8a24-7356a6e92f38" />



