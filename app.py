import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Face Attendance System", page_icon=":camera:", layout="wide")

# --- Title and Description ---
st.title(":camera: Face Detection Attendance System")
st.write("<center><h4><b>Live Attendance Marking using Webcam & Face Recognition.</b></h4></center>",unsafe_allow_html=True)
st.write("---")

# --- Setup Directories ---
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "Attendance_Record.xlsx"

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# --- Load Known Faces ---
known_face_encodings = []
known_face_names = []

for person_name in os.listdir(KNOWN_FACES_DIR):
    person_folder = os.path.join(KNOWN_FACES_DIR, person_name)
    if os.path.isdir(person_folder):
        for filename in os.listdir(person_folder):
            img_path = os.path.join(person_folder, filename)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)

# --- Load or Create Attendance File ---
if os.path.exists(ATTENDANCE_FILE):
    # If the file exists, load the existing attendance data
    attendance_df = pd.read_excel(ATTENDANCE_FILE)
else:
    # If the file doesn't exist, create an empty DataFrame and save it
    attendance_df = pd.DataFrame(columns=["Name", "Time", "Date"])
    attendance_df.to_excel(ATTENDANCE_FILE, index=False)

# --- Sidebar Controls ---
st.sidebar.header("Manage Attendance")
start = st.sidebar.button("Activate Attendance")
stop = st.sidebar.button("Deactivate Attendance")
capture_new_face = st.sidebar.checkbox("Capture New Face")
show_attendance = st.sidebar.button("View Attendance")

# --- New Face Capture ---
if capture_new_face:
    st.sidebar.subheader("Add New Face")
    new_name = st.sidebar.text_input("Enter Name:")
    open_camera = st.sidebar.button("Capture and Save Face")

    if open_camera and new_name:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera not found.")
        else:
            ret, frame = cap.read()
            if ret:
                # Save the frame immediately
                path = os.path.join(KNOWN_FACES_DIR, new_name)
                os.makedirs(path, exist_ok=True)
                img_name = f"{new_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                img_path = os.path.join(path, img_name)
                cv2.imwrite(img_path, frame)

                # Show captured image and success message
                st.image(frame, channels="BGR", caption="Captured Face", use_column_width=True)
                st.success(f"Face captured and saved successfully for {new_name}!")

            else:
                st.error("Failed to capture image.")

            cap.release()
            cv2.destroyAllWindows()

        # After saving and showing success, wait for 2 seconds then refresh page
        import time
        time.sleep(2)
        st.experimental_rerun()

# --- Main Camera Section ---

if start:
    video_capture = cv2.VideoCapture(0)
    stframe = st.empty()
    marked_names=set()

    st.success("Camera Started. Press STOP to save attendance.")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Camera not working!")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if name != "Unknown" and name not in marked_names:
                # Add new attendance record
                new_attendance = {
                    "Name": name,
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Date": datetime.now().strftime("%Y-%m-%d")
                }
                # Append to the DataFrame
                attendance_df = attendance_df.append(new_attendance, ignore_index=True)

                # Save the updated DataFrame back to Excel
                attendance_df.to_excel(ATTENDANCE_FILE, index=False)
                marked_names.add(name)

        stframe.image(frame, channels="BGR")

        # Stop if button pressed
        if stop:
            break

    # Release
    video_capture.release()
    cv2.destroyAllWindows()

# --- Show Attendance Section ---
if show_attendance:
    st.subheader("Attendance Record")
    st.dataframe(attendance_df)

# --- Footer ---
st.write("---")

