import uuid 

import streamlit
from streamlit_option_menu import option_menu
from settings import *
import sqlite3
import hashlib
import streamlit.components.v1 as components


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

PAGE_TITLE: str = "Распознавание лиц работников слишком известного центра :)"
PAGE_ICON: str = "🤖"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

with open('data/matrix.js') as f:
    html_string = f.read()
with open('data/matrix2.js') as a:
    html_string2 = a.read()
##components.html(html_string)  # JavaScript 

#st.markdown(html_string, unsafe_allow_html=True)


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3
conn = sqlite3.connect('data')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


user_color = '#2C3333'
text_color = '#CBE4DE'
title_webapp = PAGE_TITLE
html_temp = f"""
            <div id="c"; style="background-color:{user_color};padding:8px">
            </div>
            """

st.markdown(html_temp, unsafe_allow_html=True)
st.markdown(
    f"""
     <style>
     .stApp {{
         background-color: {user_color};
     }}
     </style>
     """,
    unsafe_allow_html=True
)
#components.html(html_string)
st.markdown(
    f"""
     <style>
[data-testid="stHeader"] {{
background: {user_color};
}}
     """,
    unsafe_allow_html=True
)

def main():
    
    menu = ["Инфо", "Авторизация", "Регистрация"]
    choice = st.sidebar.selectbox("Навигация", menu)
    with st.sidebar:
        components.html(html_string2, height=560)
        st.write("Специально для ЦАР")
       
        st.write("Фамилия разработчика слишком известная :)")
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #2e4f4f;
        div.row-widget.stSidebar > div {
        flex-direction: row;
        align-items: stretch;
}
}
        }
    </style>
    """, unsafe_allow_html=True)
    if choice == "Инфо":
        st.markdown("<h5 style='text-align: center'>Распознавание и верификация лиц</h5>", unsafe_allow_html=True)
        st.image('iamges/2.jpg')
        st.markdown("<h6 style='text-align: center'>О проекте</h6>", unsafe_allow_html=True)
        st.write("""Приложение создано не только ради забавы и тестирования в ЦАР, 
но и для возможной реализации в банке""")
       

    elif choice == "Авторизация":
        st.markdown("<h5 style='text-align: center'>Распознавание и верификация лиц</h5>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center'>Авторизация</h3>", unsafe_allow_html=True)

        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        if st.checkbox("Авторизация"):
            
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.markdown('''
                    <style>
                    .st-b7 {
                        color: #cbe4de;
                        background-color: #0e8388;
                        align-text: center;
                    }
                    </style>
                    ''', unsafe_allow_html=True)
                st.markdown("<h5 style='text-align: center'>Авторизация завершена успешно</h5>", unsafe_allow_html=True)
                components.html(html_string)
                selected_menu = option_menu(None,
                                            ['Идентификация', 'История', 'БД', 'Жэстачайшэ удалить'],
                                            icons=['camera', "clock-history", 'person-plus', 'trash'],
                                            ## icons from website: https://icons.getbootstrap.com/
                                            menu_icon="cast", default_index=0, orientation="horizontal",
                                            styles={
                                                "container": {"font-family": "monospace", "background-color": "#2e4f4f",
                                                              "border-radius": "0.5px", "box-sizing": "border-box"},
                                                "nav-link-selected": {"background-color": "#0e8388"},
                                                "nav-link": {"text-align": "center", "margin": "0px",
                                                             "color": '#cbe4de'}
                                            }
                                            )
                if selected_menu == 'Жэстачайшэ удалить':
                    st.markdown('''
                        <style>
                        .st-b7 {
                            color: #cbe4de;
                            background-color: #0e8388;
                            align-text: center;
                        }
                        </style>
                        ''', unsafe_allow_html=True)
                    st.success('Всё удалено к чертям собачим :)')
                    shutil.rmtree(VISITOR_DB, ignore_errors=True)
                    os.mkdir(VISITOR_DB)
                    
                    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
                    os.mkdir(VISITOR_HISTORY)

                if not os.path.exists(VISITOR_DB):
                    os.mkdir(VISITOR_DB)

                if not os.path.exists(VISITOR_HISTORY):
                    os.mkdir(VISITOR_HISTORY)

                if selected_menu == 'Идентификация':
                    
                    visitor_id = uuid.uuid1()
                    st.markdown('''
                        <style>
                        .css - fg4pbf{
                            position: absolute;
                            background:  # 0dcaf0;
                            color: rgb(49, 51, 63);
                            inset: 0
                            px;
                            overflow: hidden;}
                        </style>
                        ''', unsafe_allow_html=True)
                    
                    img_file_buffer = st.camera_input("")

                    if img_file_buffer is not None:
                        bytes_data = img_file_buffer.getvalue()

                        
                        image_array = cv2.imdecode(np.frombuffer(bytes_data,
                                                                 np.uint8),
                                                   cv2.IMREAD_COLOR)
                        image_array_copy = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                       
                        with open(os.path.join(VISITOR_HISTORY,
                                               f'{visitor_id}.jpg'), 'wb') as file:
                            file.write(img_file_buffer.getbuffer())
                            st.markdown('''
                                <style>
                                .st-b7 {
                                    color: #cbe4de;
                                    background-color: #0e8388;
                                    align-text: center;
                                }
                                </style>
                                ''', unsafe_allow_html=True)
                            st.success('Фото успешно сохранено')

                            
                            max_faces = 0
                            rois = []  

                            
                            face_locations = face_recognition.face_locations(image_array)
                            
                            encodesCurFrame = face_recognition.face_encodings(image_array,
                                                                              face_locations)

                            
                            for idx, (top, right, bottom, left) in enumerate(face_locations):
                                
                                rois.append(image_array[top:bottom, left:right].copy())

                                
                                cv2.rectangle(image_array, (left, top), (right, bottom), COLOR_DARK, 2)
                                cv2.rectangle(image_array, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(image_array, f"#{idx}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)

                            
                            st.image(BGR_to_RGB(image_array), width=720)

                            
                            max_faces = len(face_locations)

                            if max_faces > 0:
                                col1, col2 = st.columns(2)

                                
                                face_idxs = col1.multiselect('[Выбрать лицо]', range(max_faces),
                                                             default=range(max_faces))

                                
                                similarity_threshold = col2.slider('[Регулировка порога]',
                                                                   min_value=0.0, max_value=1.0,
                                                                   value=0.5)
                                

                                flag_show = False

                                if ((col1.checkbox('[Верифицировать]')) & (len(face_idxs) > 0)):
                                    dataframe_new = pd.DataFrame()

                                    
                                    for face_idx in face_idxs:
                                        
                                        roi = rois[face_idx]
                                        

                                        
                                        database_data = initialize_data()
                                       
                                        face_encodings = database_data[COLS_ENCODE].values
                                        dataframe = database_data[COLS_INFO]

                                        
                                        faces = face_recognition.face_encodings(roi)
                                        

                                        if len(faces) < 1:
                                            
                                            st.error(f'Попробуй ещё разок#{face_idx}!')
                                        else:
                                            face_to_compare = faces[0]
                                            
                                            dataframe['distance'] = face_recognition.face_distance(face_encodings,
                                                                                                   face_to_compare)
                                            dataframe['distance'] = dataframe['distance'].astype(float)

                                            dataframe['similarity'] = dataframe.distance.apply(
                                                lambda distance: f"{face_distance_to_conf(distance):0.2}")
                                            dataframe['similarity'] = dataframe['similarity'].astype(float)

                                            dataframe_new = dataframe.drop_duplicates(keep='first')
                                            dataframe_new.reset_index(drop=True, inplace=True)
                                            dataframe_new.sort_values(by="similarity", ascending=True)

                                            dataframe_new = dataframe_new[
                                                dataframe_new['similarity'] > similarity_threshold].head(1)
                                            dataframe_new.reset_index(drop=True, inplace=True)

                                            if dataframe_new.shape[0] > 0:
                                                (top, right, bottom, left) = (face_locations[face_idx])

                                                
                                                rois.append(image_array_copy[top:bottom, left:right].copy())

                                                
                                                cv2.rectangle(image_array_copy, (left, top), (right, bottom),
                                                              COLOR_DARK, 2)
                                                cv2.rectangle(image_array_copy, (left, bottom + 35), (right, bottom),
                                                              COLOR_DARK, cv2.FILLED)
                                                font = cv2.FONT_HERSHEY_DUPLEX
                                                cv2.putText(image_array_copy, f"#{dataframe_new.loc[0, 'Name']}",
                                                            (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)

                                                
                                                name_visitor = dataframe_new.loc[0, 'Name']
                                                attendance(visitor_id, name_visitor)

                                                flag_show = True

                                            else:
                                                st.error(
                                                    f'Ничего не найдено В БД#{face_idx}')
                                                st.info('Обновите данные в БД или сделайте новое фото и сохраните в БД')
                                                attendance(visitor_id, 'Аноним Анонимыч')

                                    if flag_show == True:
                                        st.image(BGR_to_RGB(image_array_copy), width=720)

                            else:
                                st.error('Лица не нашёл. А человек ли на фото, а ?')

                if selected_menu == 'История':
                    view_attendace()

                if selected_menu == 'БД':
                    col1, col2, col3 = st.columns(3)

                    face_name = col1.text_input('Name:', '')
                    pic_option = col2.radio('Загрузить фото',
                                            options=["Загрузить фото",
                                                     "Сделать фото"])

                    if pic_option == 'Загрузить фото':
                        img_file_buffer = col3.file_uploader('Загрузить фото',
                                                             type=allowed_image_type)
                        if img_file_buffer is not None:
                            
                            file_bytes = np.asarray(bytearray(img_file_buffer.read()),
                                                    dtype=np.uint8)

                    elif pic_option == 'Сделать фото':
                        img_file_buffer = col3.camera_input("Сделать фото")
                        if img_file_buffer is not None:
                            
                            file_bytes = np.frombuffer(img_file_buffer.getvalue(),
                                                       np.uint8)

                    if ((img_file_buffer is not None) & (len(face_name) > 1) &
                            st.button('Сохранить')):
                       
                        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                        

                        with open(os.path.join(VISITOR_DB,
                                               f'{face_name}.jpg'), 'wb') as file:
                            file.write(img_file_buffer.getbuffer())
                            

                        face_locations = face_recognition.face_locations(image_array)
                        encodesCurFrame = face_recognition.face_encodings(image_array,
                                                                          face_locations)

                        df_new = pd.DataFrame(data=encodesCurFrame,
                                              columns=COLS_ENCODE)
                        df_new[COLS_INFO] = face_name
                        df_new = df_new[COLS_INFO + COLS_ENCODE].copy()

                       
                        DB = initialize_data()
                        add_data_db(df_new)
            else:
                st.warning("Некорректный логин или пароль")
                #"<style='text-align: center'>Incorrect Username/Password<>", unsafe_allow_html=True





    elif choice == "Регистрация":
        st.markdown("<h3 style='text-align: center'>Приложение для распознавания лиц</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center'>Сделать новый аккаунт</h5>", unsafe_allow_html=True)
        new_user = st.text_input("Имя пользователя")
        new_password = st.text_input("Пароль", type='password')

        if st.button("Регистрация"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.markdown('''
                <style>
                .st-b7 {
                    color: #cbe4de;
                    background-color: #0e8388;
                    align-text: center;
                }
                </style>
                ''', unsafe_allow_html=True)
            st.success("Аккаунт успешно создан, пройди авторизацию !")
            st.image("Data/1.jpg")
    ###################################################



#######################################################
if __name__ == "__main__":
    main()
#######################################################
