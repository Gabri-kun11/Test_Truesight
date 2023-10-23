import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from register import fetch_user
#from register import fetch_user, registration
from streamlit_option_menu import option_menu
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
#from pydub.playback import play
#from pydub import AudioSegment
from datetime import timedelta
from googleapiclient.errors import HttpError

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def SignIn():

    def headfolder(head_id):
        try:
            image_files = drive.ListFile({'q': f"'{head_id}' in parents and trashed=false"}).GetList()
            image_files = sorted(image_files, key=lambda x: datetime.datetime.strptime(x['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)
            return image_files
        except HttpError as e:
            return []

    def handfolder(hand_id):
        try:
            image_files = drive.ListFile({'q': f"'{hand_id}' in parents and trashed=false"}).GetList()
            image_files = sorted(image_files, key=lambda x: datetime.datetime.strptime(x['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)
            return image_files
        except HttpError:
            return []

    def soundfolder(sound_id):
        try:
            audio_files = drive.ListFile({'q': f"'{sound_id}' in parents and trashed=false and mimeType contains 'audio/'"}).GetList()
            audio_files = sorted(audio_files, key=lambda x: datetime.datetime.strptime(x['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)
            return audio_files
        except HttpError:
            return []

    def posturefolder(posture_id):
        try:
            posture_files = drive.ListFile({'q': f"'{posture_id}' in parents and trashed=false"}).GetList()
            posture_files = sorted(posture_files, key=lambda x: datetime.datetime.strptime(x['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)
            return posture_files
        except HttpError:
            return []

    def additionalfolder(additional_id):
        try:
            additional_files = drive.ListFile({'q': f"'{additional_id}' in parents and trashed=false"}).GetList()
            additional_files = sorted(additional_files, key=lambda x: datetime.datetime.strptime(x['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)
            return additional_files
        except HttpError:
            return []

    def delete_directories(drive):
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                file.Delete()

    def directory_with_subdirectories(email):
        folder_name = email

        file_list = drive.ListFile({'q': f"title='{folder_name}' and trashed=false"}).GetList()
        if not file_list:
            folder_metadata = {
                'title': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            user_folder = drive.CreateFile(folder_metadata)
            user_folder.Upload()

            subdirectories = ['Head Tracking', 'Hand Tracking', 'Sound Tracking', 'Posture Tracking', 'Additional Student Tracking']
            subfolder_ids = {}

            for subdirectory_name in subdirectories:
                subdirectory_metadata = {
                    'title': subdirectory_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [{'id': user_folder['id']}]
                }
                subdirectory = drive.CreateFile(subdirectory_metadata)
                subdirectory.Upload()
                subfolder_ids[subdirectory_name] = subdirectory['id']

            permission = {
                'type': 'anyone',
                'role': 'reader',
            }

            user_folder.InsertPermission(permission)

            return folder_name, subfolder_ids

        else:
            user_folder = file_list[0]
            subdirectories = drive.ListFile({'q': f"'{user_folder['id']}' in parents and trashed=false"}).GetList()
            subfolder_ids = {}

            for subdirectory in subdirectories:
                subfolder_ids[subdirectory['title']] = subdirectory['id']

            return folder_name, subfolder_ids

    def email_txt_gdrive(drive, email):
        # Check if email.txt already exists
        email_files = drive.ListFile({'q': "title='email.txt' and trashed=false"}).GetList()

        if email_files:
            # update the content if it exist
            email_file = email_files[0]
            email_file.SetContentString(email)
            email_file.Upload()
        else:
            # create email.txt if it does not exist
            email_file = drive.CreateFile({'title': 'email.txt'})
            email_file.SetContentString(email)
            email_file.Upload()

    # st.set_page_config(page_title='Truesight',
    #                    page_icon= "📸",
    #                    initial_sidebar_state='collapsed')

    try:
        users = fetch_user()
        emails = []
        usernames = []
        passwords = []

        for user in users:
            emails.append(user['key'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        credentials = {'usernames': {}}
        for index in range(len(emails)):
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        #if the login form has no display then this line is the main reason
        Authenticator = stauth.Authenticate(credentials,
                                            cookie_name='Streamlit123828450',
                                            key='abcdefg',
                                            cookie_expiry_days=60)

        email, authentication_status, username = Authenticator.login('Login','main')

        email_txt_gdrive(drive, email) # Most important shit DO NOT DELETE THIS EVER

        info, info1 = st.columns(2)

        # if not authentication_status:
        #     registration()

        #Check if the username is in the database
        if username:
            if username in usernames:
                if authentication_status: #if username is on the database then it will sucessfully login to the web app
                    email, subfolder_ids = directory_with_subdirectories(email)

                    head_id = subfolder_ids['Head Tracking']
                    head_image_files = headfolder(head_id)

                    hand_id = subfolder_ids['Hand Tracking']
                    hand_image_files = handfolder(hand_id)

                    posture_id = subfolder_ids['Posture Tracking']
                    posture_image_files = posturefolder(posture_id)

                    additional_id = subfolder_ids['Additional Student Tracking']
                    additional_image_files = additionalfolder(additional_id)

                    sound_id = subfolder_ids['Sound Tracking']
                    sound_image_files = soundfolder(sound_id)

                    st.markdown("---")
                    #Dashboard
                    #st.sidebar.title(f"Welcome {username}")
                    with st.sidebar:
                        selection = option_menu(
                        #menu_title="Dashboard",
                        menu_title=(f"{username}"),
                        options=["Evidence", "Log out"],
                        icons=["person-bounding-box", "bell", "box-arrow-left"],
                        #menu_icon="menu-button-fill",
                        menu_icon = "person-square",
                        default_index=0,
                    )

                    st.info(
                        "Click the 'Click Here' button or click anything to update the Web Application and receive alerts and new evidence.")
                    st.button("Click Here")

                    previous_head_motion_count = st.session_state.get("previous_head_motion_count", 0)
                    previous_hand_gesture_count = st.session_state.get("previous_hand_gesture_count", 0)
                    previous_posture_detection_count = st.session_state.get("previous_posture_detection_count", 0)
                    previous_additional_student_count = st.session_state.get("previous_additional_student_count", 0)
                    previous_sound_detections_count = st.session_state.get("previous_sound_detections_count", 0)

                    new_head_motion_detections = len(head_image_files) - previous_head_motion_count
                    new_hand_gesture_detections = len(hand_image_files) - previous_hand_gesture_count
                    new_posture_detections = len(posture_image_files) - previous_posture_detection_count
                    new_additional_student_detections = len(additional_image_files) - previous_additional_student_count
                    new_sound_detections = len(sound_image_files) - previous_sound_detections_count

                    #Alert System Sound
                    if new_head_motion_detections > 0:
                        #audio = AudioSegment.from_file("Alert/Alert.wav")
                        #play(audio)
                        st.error(
                            f"New Head Motion Cheating Detected! ({new_head_motion_detections} new detections) Check the evidence dashboard for more information.")

                    if new_hand_gesture_detections > 0:
                        #audio = AudioSegment.from_file("Alert/Alert1.wav")
                        #play(audio)
                        st.error(
                            f"New Hand Gesture Cheating Detected! ({new_hand_gesture_detections} new detections) Check the evidence dashboard for more information.")

                    if new_posture_detections > 0:
                        #audio = AudioSegment.from_file("Alert/Alert2.wav")
                        #play(audio)
                        st.error(
                            f"New Student Not Detected! ({new_posture_detections} new detections) Check the evidence dashboard for more information.")

                    if new_additional_student_detections > 0:
                        #audio = AudioSegment.from_file("Alert/Alert3.wav")
                        #play(audio)
                        st.error(
                            f"New Additional student Detected! ({new_additional_student_detections} new detections) Check the evidence dashboard for more information.")

                    if new_sound_detections > 0:
                        #audio = AudioSegment.from_file("Alert/Alert4.wav")
                        #play(audio)
                        st.error(
                            f"New Sound Cheating Detected! ({new_sound_detections} new detections) Check the evidence dashboard for more information.")

                    previous_head_motion_count = len(head_image_files)
                    previous_hand_gesture_count = len(hand_image_files)
                    previous_posture_detection_count = len(posture_image_files)
                    previous_additional_student_count = len(additional_image_files)
                    previous_sound_detections_count = len(sound_image_files)

                    st.session_state["previous_head_motion_count"] = previous_head_motion_count
                    st.session_state["previous_hand_gesture_count"] = previous_hand_gesture_count
                    st.session_state["previous_posture_detection_count"] = previous_posture_detection_count
                    st.session_state["previous_additional_student_count"] = previous_additional_student_count
                    st.session_state["previous_sound_detections_count"] = previous_sound_detections_count

                    # if selection == "Video Stream":
                    #     st.header("Real-time Video Stream")
                    #     st.markdown("---")

                    #     if st.button("Open VideoStream"):
                    #         subprocess.Popen(["streamlit", "run", "videostream.py"])
                    #         st.markdown("---")

                    if selection == "Evidence":
                        st.header("Evidence")

                        st.subheader("Head Motion")
                        head_images_per_page = 5
                        head_num_pages = (len(head_image_files) + head_images_per_page - 1) // head_images_per_page
                        head_page_num = st.number_input("Head Motion Evidence", min_value=1, max_value=head_num_pages,
                                                        value=1)
                        st.markdown(f"Page {head_page_num} out of {head_num_pages}")

                        start_idx = (head_page_num - 1) * head_images_per_page
                        end_idx = min(start_idx + head_images_per_page, len(head_image_files))

                        for i in range(start_idx, end_idx):
                            if i >= len(head_image_files):
                                break

                            head_image_file = head_image_files[i]
                            if head_image_file['mimeType'].startswith('image'):
                                file_name = head_image_file['title'].replace('.png', '')
                                st.image(head_image_file['webContentLink'], caption=file_name, use_column_width=True)

                        st.subheader("Hand Gesture")
                        hand_images_per_page = 5
                        hand_num_pages = (len(hand_image_files) + hand_images_per_page - 1) // hand_images_per_page
                        hand_page_num = st.number_input("Hand Gesture Evidence", min_value=1, max_value=hand_num_pages,
                                                        value=1)
                        st.markdown(f"Page {hand_page_num} out of {hand_num_pages}")

                        start_idx = (hand_page_num - 1) * hand_images_per_page
                        end_idx = min(start_idx + hand_images_per_page, len(hand_image_files))

                        for i in range(start_idx, end_idx):
                            if i >= len(hand_image_files):
                                break

                            hand_image_file = hand_image_files[i]
                            if hand_image_file['mimeType'].startswith('image'):
                                file_name = hand_image_file['title'].replace('.png', '')
                                st.image(hand_image_file['webContentLink'], caption=file_name, use_column_width=True)

                        st.subheader("Posture/Incomplete Student")
                        head_images_per_page = 5
                        head_num_pages = (len(posture_image_files) + head_images_per_page - 1) // head_images_per_page
                        head_page_num = st.number_input("Head Motion Evidence", min_value=1, max_value=head_num_pages,
                                                        value=1)
                        st.markdown(f"Page {head_page_num} out of {head_num_pages}")

                        start_idx = (head_page_num - 1) * head_images_per_page
                        end_idx = min(start_idx + head_images_per_page, len(posture_image_files))

                        for i in range(start_idx, end_idx):
                            if i >= len(posture_image_files):
                                break

                            posture_image_file = posture_image_files[i]
                            if posture_image_file['mimeType'].startswith('image'):
                                file_name = posture_image_file['title'].replace('.png', '')
                                st.image(posture_image_file['webContentLink'], caption=file_name, use_column_width=True)

                        st.subheader("Additional Student")
                        head_images_per_page = 5
                        head_num_pages = (len(additional_image_files) + head_images_per_page - 1) // head_images_per_page
                        head_page_num = st.number_input("Head Motion Evidence", min_value=1, max_value=head_num_pages,
                                                        value=1)
                        st.markdown(f"Page {head_page_num} out of {head_num_pages}")

                        start_idx = (head_page_num - 1) * head_images_per_page
                        end_idx = min(start_idx + head_images_per_page, len(additional_image_files))

                        for i in range(start_idx, end_idx):
                            if i >= len(additional_image_files):
                                break

                            additional_image_file = additional_image_files[i]
                            if additional_image_file['mimeType'].startswith('image'):
                                file_name = additional_image_file['title'].replace('.png', '')
                                st.image(additional_image_file['webContentLink'], caption=file_name, use_column_width=True)

                        st.subheader("Sound")
                        sound_audio_files_per_page = 5
                        sound_num_pages = ( len(sound_image_files) + sound_audio_files_per_page - 1) // sound_audio_files_per_page
                        sound_page_num = st.number_input("Sound Evidence", min_value=1, max_value=sound_num_pages, value=1)
                        st.markdown(f"Page {sound_page_num} out of {sound_num_pages}")

                        start_idx = (sound_page_num - 1) * sound_audio_files_per_page
                        end_idx = min(start_idx + sound_audio_files_per_page, len(sound_image_files))

                        for i in range(start_idx, end_idx):
                            if i >= len(sound_image_files):
                                break

                            audio_file = sound_image_files[i]
                            if audio_file["mimeType"].startswith("audio"):
                                audio_url = f"https://drive.google.com/uc?id={audio_file['id']}"

                                # Extract date and time from Google Drive (Not Accurate)
                                modified_date_time = datetime.datetime.strptime(audio_file['modifiedDate'],
                                                                                "%Y-%m-%dT%H:%M:%S.%fZ")

                                # Subtract 19 hours, 58 minutes, and 5 seconds
                                modified_date_time += timedelta(hours=19, minutes=58, seconds=5)

                                # If AM, moves the day back by one day
                                if modified_date_time.hour < 12:
                                    modified_date_time -= timedelta(days=1)

                                formatted_date = modified_date_time.strftime("Date_%Y-%m-%d")
                                formatted_time = modified_date_time.strftime("Time_%I-%M-%S %p")

                                # Reverse AM and PM
                                formatted_time = formatted_time.replace("AM", "temp_AM").replace("PM", "AM").replace(
                                    "temp_AM", "PM")

                                # Combine date and time
                                formatted_date_time = f"{formatted_date}_{formatted_time}"

                                # Display audio file
                                st.audio(audio_url, format="audio/mp3")

                                # CSS to copy Head and Hand Date and Time
                                formatted_date_time_css = f'<p style="color: gray; font-size: 14px; text-align: center; margin-top: -10px;">{formatted_date_time}</p>'
                                st.markdown(formatted_date_time_css, unsafe_allow_html=True)

                        if st.button("Delete All Evidence"):
                            head_id = subfolder_ids['Head Tracking']
                            hand_id = subfolder_ids['Hand Tracking']
                            posture_id = subfolder_ids['Posture Tracking']
                            additional_id = subfolder_ids['Additional Student Tracking']
                            sound_id = subfolder_ids['Sound Tracking']


                        # New Delete Evidence code so that it will not stop deleting until everything was deleted
                            def delete_files(subfolder_id):
                                try:
                                    file_list = drive.ListFile(
                                        {'q': f"'{subfolder_id}' in parents and trashed=false"}).GetList()
                                    for file in file_list:
                                        file.Trash()
                                except HttpError as e:
                                    pass

                            delete_files(head_id)
                            delete_files(hand_id)
                            delete_files(posture_id)
                            delete_files(additional_id)
                            delete_files(sound_id)

                            st.success("All Evidence have been deleted. Please click the button above.")

                    if selection == "Log out":
                        #st.header("Logout")
                        Authenticator.logout('Logout')
                        #subprocess.Popen(["streamlit", "run", "testnav.py"])
                        #stauth.Authenticate.logout
                    #Authenticator.logout('Log Out', 'main')

                elif not authentication_status:
                    with info:
                        st.error('Incorrect Password or username')
                else:
                    with info:
                        st.warning('Please feed in your credentials')
            else:
                st.warning('Username does not exist, Please Sign up')
    except:
        pass

