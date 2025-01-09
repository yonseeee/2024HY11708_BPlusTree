import pymysql
from datetime import datetime, timedelta


#db에 연결
def connect_to_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="musicapp",
        charset="utf8mb4"
    )

# Main Menu
def main_menu():
    while True:
        print("\n\nWelcome to our Music App!")
        print("0. Exit")
        print("1. Admin mode")#관리자 모드
        print("2. User mode")#사용자 모드
        choice = input("\nEnter your choice: ")

        if choice == "0":
            print("\nExiting the program. Goodbye!")
            break
        elif choice == "1":
            admin_menu()
        elif choice== "2":
            user_menu()
        else:
            print("\nInvalid choice. Please try again.")

# 관리자 모드
def admin_menu():
    while True:
        print("\n\n----Admin Mode----")
        print("0. Return to previous menu")
        print("1. Sign up")
        print("2. Login")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            admin_sign_up()
        elif choice == "2":
            admin_login()
        else:
            print("\nInvalid choice. Please try again.")

#관리자 회원 가입
def admin_sign_up():
    connection = connect_to_db()
    cursor = connection.cursor()
    
    print("\n\n----Admin Sign up----")

    try:
        admin_id = input("Enter you admin ID(only number): ")
        pw=input("Enter your password: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")

    
        query = "INSERT INTO Admins (admin_id, name, email, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (admin_id, name, email, phone, pw))
        connection.commit()
        print("\nAdmin signed up successfully!")
    except pymysql.IntegrityError:
            print("\nFailed to sign up. This ID is already in the Admins.")
    finally:
        cursor.close()
        connection.close()

#관리자 로그인
def admin_login():
    connection = connect_to_db()
    cursor = connection.cursor() 

    print("\n\n----Admin Login----")
    admin_id = input("Enter you admin ID(only number): ")
    password = input("Enter your password: ")

    try:
        query = "SELECT * FROM Admins WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, password))
        admin = cursor.fetchone()

        if admin:
            print(f"\nLogin Successful! Welcome, {admin[1]}")
            admin_dashboard(admin[0])
        else:
            print("\nInvalid user ID or password. Please try again.")

    finally:
        cursor.close()
        connection.close()

#관리자 메뉴
def admin_dashboard(admin_id):
    while True:
        print("\n\n----Admin Menu----")
        print("0. Logout")
        print("1. Manage Music")
        print("2. View Playlists")
        print("3. View Subscription list")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            print("\nLogged out successfully.")
            break
        elif choice == "1":
            manage_music(admin_id)
        elif choice == "2":
            playlists_admin()
        elif choice=="3":
            subscription_list()
        else:
            print("\nInvalid choice. Please try again.")

#관리자-음악 관리
def manage_music(admin_id):
    while True:
        print("\n\n----Manage Music----")
        print("0. Return to previous menu")
        print("1. View music lists")
        print("2. Register a new music")
        print("3. Edit a music")
        print("4. Delete a music")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            show_music()
        elif choice == "2":
            register_music(admin_id)
        elif choice == "3":
            edit_music()
        elif choice == "4":
            delete_music()
        else:
            print("\nInvalid choice. Please try again.")

#관리자-음악관리-음악 목록 보기
def show_music():
    connection=connect_to_db()
    cursor=connection.cursor()

    try:
        query = "SELECT * FROM Music"
        cursor.execute(query)
        music_list = cursor.fetchall()

        print("\n<Music List>")
        for music in music_list:
            print(f"ID: {music[0]}, Title: {music[2]}, Artist: {music[1]}, Genre: {music[5]}, Release Date: {music[6]}")
    finally:
        cursor.close()
        connection.close()

#관리자-음악관리-음악 등록
def register_music(admin_id):
    connection=connect_to_db()
    cursor=connection.cursor()

    print("\n\n----Register New Music----")
    title = input("Enter the title: ")
    artist = input("Enter the artist name: ")
    lyricist = input("Enter the lyricist: ")
    composer = input("Enter the composer: ")
    genre = input("Enter the genre: ")
    release_date = input("Enter the release date (YYYY-MM-DD): ")

    try:
        query = "INSERT INTO Music (artist, title, lyricist, composer, genre, release_date) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (artist, title, lyricist, composer, genre, release_date))
        connection.commit()

        music_id = cursor.lastrowid

        query = "INSERT INTO MusicManagement (admin_id, music_id) VALUES (%s, %s)"
        cursor.execute(query, (admin_id, music_id))
        connection.commit()

        print("\nMusic registered successfully and assigned to the logged-in admin.")

    finally:
        cursor.close()
        connection.close()

#관리자-음악 관리-음악 수정
def edit_music():
    connection=connect_to_db()
    cursor=connection.cursor()

    print("\n\n----Update Music----")
    music_id = input("Enter the Music ID to edit: ")
    print("What would you like to edit?")
    print("1. Title")
    print("2. Artist")
    print("3. Lyricist")
    print("4. Composer")
    print("5. Genre")
    choice = input("\nEnter your choice: ")

    column_map = {
        "1": "title",
        "2": "artist",
        "3": "lyricist",
        "4": "composer",
        "5": "genre"
    }
    try:
        if choice in column_map:
            new_value = input(f"Enter new {column_map[choice]}: ")
            query = f"UPDATE Music SET {column_map[choice]} = %s WHERE music_id = %s"
            cursor.execute(query, (new_value, music_id))
            connection.commit()
            print("\nMusic edited successfully.")
        else:
            print("\nInvalid choice.")
    finally:
        cursor.close()
        connection.close()

#관리자-음악관리- 음악 삭제
def delete_music():
    connection=connect_to_db()
    cursor=connection.cursor()
    
    print("\n\n----Delete Music----")
    music_id = input("Enter the music ID to delete: ")

    try:   
        query = "DELETE FROM Music WHERE music_id = %s"
        cursor.execute(query, (music_id))
        connection.commit()
        

        query = "DELETE FROM MusicManagement WHERE music_id = %s"
        cursor.execute(query, (music_id))
        connection.commit()

        print("\nMusic deleted successfully.")


    finally:
        cursor.close()
        connection.close()
    

#관리자-플레이리스트 목록 보기
def playlists_admin():
    connection=connect_to_db()
    cursor=connection.cursor()

    try:
        query = "SELECT * FROM Playlists"
        cursor.execute(query)
        playlists = cursor.fetchall()

        print("\n<All playlists and their songs>")
        for playlist in playlists:
            print(f"Title: {playlist[1]}, Created At: {playlist[3]}, Created By: {playlist[4]}")

            query = """
                SELECT Music.title, Music.artist, Music.lyricist, Music.composer, Music.genre, Music.release_date
                FROM PlaylistMusic 
                JOIN Music ON PlaylistMusic.music_id = Music.music_id 
                WHERE PlaylistMusic.playlist_id = %s
            """
            cursor.execute(query, (playlist[0],))
            songs = cursor.fetchall()

            if songs:
                print("  Music:")
                for song in songs:
                    print(f"    - Title: {song[0]}, Artist: {song[1]}, Lyricist: {song[2]}, Composer: {song[3]}, Genre: {song[4]}, Release Date: {song[5]}")
            else:
                print("  No songs in this playlist.")
    finally:
        cursor.close()
        connection.close()


#관리자-구독 목록 보기
def subscription_list():
    connection=connect_to_db()
    cursor=connection.cursor()

    try:
        query="SELECT * FROM PremiumSubscriptions ORDER BY start_date"
        cursor.execute(query)
        results=cursor.fetchall()

        print("\n\n<Subscription list order by start date>")
        for result in results:
            print(f"User ID: {result[3]}, Start date: {result[1]}, End date: {result[2]}")

    finally:
        cursor.close()
        connection.close()







#사용자 모드
def user_menu():
    while True:
        print("\n\n----User Mode----")
        print("0. Return to previous menu")
        print("1. Sign up")
        print("2. Login")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            user_sign_up()
        elif choice == "2":
            user_login()
        else:
            print("\nInvalid choice. Please try again.")

#사용자 회원가입
def user_sign_up():
    connection = connect_to_db()
    cursor = connection.cursor()

    print("\n\n----User Sign Up----")
    try:
        user_id = input("Enter your user ID: ")
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        email = input("Enter your email: ")
        birth_date = input("Enter your birth date (YYYY-MM-DD): ")


        query = " Users (user_id, name, password, email, birth_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, name, password, email, birth_date))
        connection.commit()
        print("\nUser signed up successfully!")
    except pymysql.IntegrityError:
            print("\nFailed to sign up. This ID is already in the Users.")
    finally:
        cursor.close()
        connection.close()

#사용자 로그인
def user_login():
    connection = connect_to_db()
    cursor = connection.cursor()

    print("\n\n----User Login----")
    user_id = input("Enter your user ID: ")
    password = input("Enter your password: ")

    try:
        query = "SELECT * FROM Users WHERE user_id = %s AND password = %s"
        cursor.execute(query, (user_id, password))
        user = cursor.fetchone()

        if user:
            print(f"\nLogin successful! Welcome, {user[1]}.")
            user_dashboard(user[0])
        else:
            print("\nInvalid user ID or password. Please try again.")

    finally:
        cursor.close()
        connection.close()


#사용자 메뉴
def user_dashboard(user_id):
    while True:
        print("\n\n----User Menu----")
        print("0. Logout")
        print("1. View all playlists which are public")
        print("2. Manage Likes")
        print("3. Manage Playlists")
        print("4. Subscribe Premium Service")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            print("\nLogged out successfully.")
            break
        elif choice == "1":
            show_playlists_with_songs()
        elif choice == "2":
            manage_likes(user_id)
        elif choice == "3":
            manage_playlist(user_id)
        elif choice == "4":
            subscribe_premium(user_id)
        else:
            print("\nInvalid choice. Please try again.")

#사용자-플레이리스트 목록 보기
def show_playlists_with_songs():
    connection=connect_to_db()
    cursor=connection.cursor()

    try:
        # Fetch all playlists
        query = "SELECT * FROM Playlists WHERE is_public = TRUE"
        cursor.execute(query)
        playlists = cursor.fetchall()

        print("\n<All public Playlists and Their Songs>")
        for playlist in playlists:
            print(f"Title: {playlist[1]}, Created At: {playlist[3]}")

            # Fetch songs in the current playlist
            query = """
                SELECT Music.title, Music.artist, Music.lyricist, Music.composer, Music.genre, Music.release_date
                FROM PlaylistMusic 
                JOIN Music ON PlaylistMusic.music_id = Music.music_id 
                WHERE PlaylistMusic.playlist_id = %s
            """
            cursor.execute(query, (playlist[0],))
            songs = cursor.fetchall()

            if songs:
                print("  Music:")
                for song in songs:
                    print(f"    - Title: {song[0]}, Artist: {song[1]}, Lyricist: {song[2]}, Composer: {song[3]}, Genre: {song[4]}, Release Date: {song[5]}")
            else:
                print("  No songs in this playlist.")
    finally:
        cursor.close()
        connection.close()

#사용자-좋아요 관리
def manage_likes(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        while True:
            print("\n\n----Manage Likes----")
            print("\n<Your Likes list>")

            query = """
                SELECT Music.music_id, Music.title
                FROM Music, Likes
                WHERE Music.music_id = Likes.music_id AND Likes.user_id=%s
            """
            cursor.execute(query, user_id)
            results = cursor.fetchall()

            for result in results:
                print(f"Music ID: {result[0]}, title: {result[1]}")

            
            print("\n0. Return to previous menu")
            print("1. Add a like")
            print("2. Remove a like")
            choice = input("\nEnter your choice: ")

            if choice == "0":
                break
            elif choice == "1":
                query="SELECT * FROM Music"
                cursor.execute(query)
                results=cursor.fetchall()


                print("\n<Entire Music List>")
                for result in results:
                    print(f"Music ID: {result[0]}, Title: {result[2]}")
                
                music_id = input("\nEnter the Music ID to like: ")
                query = "INSERT INTO Likes (user_id, music_id) VALUES (%s, %s)"
                cursor.execute(query, (user_id, music_id))
                connection.commit()
                print("\nLiked the song successfully!")
            elif choice == "2":
                music_id = input("\nEnter the music ID to unlike: ")
                query = "DELETE FROM Likes WHERE user_id = %s AND music_id = %s"
                cursor.execute(query, (user_id, music_id))
                connection.commit()
                print("\nRemoved the like successfully!")
            else:
                print("\nInvalid choice. Please try again.")
    finally:
        cursor.close()
        connection.close()

#사용자-플레이리스트 관리
def manage_playlist(user_id):
    while True:
        print("\n\n----Manage Playlists----")
        print("0. Return to previous menu")
        print("1. Show my playlists")
        print("2. Add music to my Playlist")
        print("3. Create a new playlist")
        print("4. Edit a playlist info")
        print("5. Delete a playlist")
        choice = input("\nEnter your choice: ")

        if choice == "0":
            break
        elif choice=="1":
            show_my_playlists(user_id)
        elif choice == "2":
            update_playlist(user_id)
        elif choice == "3":
            create_playlist(user_id)
        elif choice == "4":
            edit_playlist(user_id)
        elif choice == "5":
            delete_playlist(user_id)
        else:
            print("\nInvalid choice. Please try again.")

#사용자-플레이리스트 관리-내가 만든 플리 목록 보기
def show_my_playlists(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM Playlists WHERE created_by = %s"
        cursor.execute(query, (user_id,))
        playlists = cursor.fetchall()

        print("\n<Your Playlists and Their Songs>")
        for playlist in playlists:
            print(f"Playlist ID: {playlist[0]}, Title: {playlist[1]}, Public: {playlist[2]}, Created At: {playlist[3]}")

            query = """
                SELECT Music.title, Music.artist, Music.lyricist, Music.composer, Music.genre, Music.release_date
                FROM PlaylistMusic 
                JOIN Music ON PlaylistMusic.music_id = Music.music_id 
                WHERE PlaylistMusic.playlist_id = %s
            """
            cursor.execute(query, (playlist[0],))
            songs = cursor.fetchall()

            if songs:
                print("  Music:")
                for song in songs:
                    print(f"    - Title: {song[0]}, Artist: {song[1]}, Lyricist: {song[2]}, Composer: {song[3]}, Genre: {song[4]}, Release Date: {song[5]}")
            else:
                print("  No songs in this playlist.")
    finally:
        cursor.close()
        connection.close()

#사용자-플레이리스트 관리-플리에 음악 추가
def update_playlist(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        print("\n\n----Add music to your playlist----")
        playlist_id = input("Enter the playlist ID to update: ")

        query = "SELECT * FROM Playlists WHERE playlist_id = %s AND created_by = %s"
        cursor.execute(query, (playlist_id, user_id))
        playlist = cursor.fetchone()

        if not playlist:
            print("\nYou do not have permission to update this playlist or it does not exist.")
            return

        while True:
            query = "SELECT * FROM Music"
            cursor.execute(query)
            music_list = cursor.fetchall()

            print("\n<Music list>")
            for music in music_list:
                print(f"Music ID: {music[0]}, Title: {music[2]}, Artist: {music[1]}")

            music_id = input("\nEnter the music ID to add to the playlist (or type 'exit' to stop): ")
            if music_id.lower() == 'exit':
                print("\nExiting music addition.")
                break

            try:
                query = "INSERT INTO PlaylistMusic (playlist_id, music_id) VALUES (%s, %s)"
                cursor.execute(query, (playlist_id, music_id))
                connection.commit()

                print("\nMusic added to the playlist successfully!")
            except pymysql.IntegrityError:
                print("\nThis music is already in the playlist.")
    finally:
        cursor.close()
        connection.close()

#사용자-플레이리스트 관리-플리 생성
def create_playlist(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    print("\n\n----Create a new playlist----")
    title = input("Enter the title of the playlist: ")

    try:
        query = "INSERT INTO Playlists (title, created_by) VALUES (%s, %s)"
        cursor.execute(query, (title, user_id))
        connection.commit()
        print("\nPlaylist created successfully!")

    finally:
        cursor.close()
        connection.close()


#사용자-플레이리스트 관리-플리 정보 수정
def edit_playlist(user_id):

    connection = connect_to_db()
    cursor = connection.cursor()

    print("\n\n----Edit a playlist----")
    playlist_id = input("Enter the playlist ID to edit: ")


    try:
        query = "SELECT * FROM Playlists WHERE playlist_id = %s AND created_by = %s"
        cursor.execute(query, (playlist_id, user_id))
        playlist = cursor.fetchone()


        if not playlist:
            print("\nYou do not have permission to delete this playlist or it does not exist.")
            return

        print("\nWhat would you like to update?")
        print("1.Title")
        print("2.Public or Private")

        choice=input("\nEnter your choice: ")

        column_map={
            "1":"title",
            "2":"is_public"
        }

   
        if choice in column_map:

            if choice=="1":
                new_value = input(f"Enter new title: ")
                query = f"UPDATE Playlists SET title = %s WHERE playlist_id = %s"
            elif choice =="2":
                new_value=input(f"Make the playlist public or private(public:1, private:0):")
                query = f"UPDATE Playlists SET is_public = %s WHERE playlist_id = %s"
                
            cursor.execute(query, (new_value, playlist_id))
            connection.commit()
            print("\nPlaylist updated successfully!")
        else:
            print("\nInvalid choice.")
    finally:
        cursor.close()
        connection.close()


#사용자-플레이리스트 관리-플리 삭제
def delete_playlist(user_id):  
    connection = connect_to_db()
    cursor = connection.cursor()

    print("\n\n----Delete a playlist----")
    playlist_id = input("Enter the playlist ID to delete: ")

    try:
        query = "SELECT * FROM Playlists WHERE playlist_id = %s AND created_by = %s"
        cursor.execute(query, (playlist_id, user_id))
        playlist = cursor.fetchone()

        if not playlist:
            print("You do not have permission to delete this playlist or it does not exist.")
            return

        query = "DELETE FROM Playlists WHERE playlist_id = %s"
        cursor.execute(query, (playlist_id,))
        connection.commit()

        print("\nPlaylist deleted successfully!")
    finally:
        cursor.close()
        connection.close()

#사용자-프리미엄 구독
def subscribe_premium(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM PremiumSubscriptions WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        subscription = cursor.fetchone()

        if subscription:
            print("\nYou are already subscribed to the premium service.")
        else:
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=365)
            query = "INSERT INTO PremiumSubscriptions (start_date, end_date, user_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (start_date, end_date, user_id))
            connection.commit()
            print("\nPremium subscription added successfully! Valid for 1 year.")
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    main_menu()