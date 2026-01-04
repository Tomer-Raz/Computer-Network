import socket
import threading

# --- הגדרות השרת ---
SERVER_IP = '127.0.0.1'  # מאזין רק למחשב המקומי (לצורך הפרויקט)
SERVER_PORT = 5555       # פורט שרירותי (גדול מ-1024)
MAX_CLIENTS = 10         # מקסימום לקוחות להאזנה

# מילון לשמירת הלקוחות המחוברים: { "שם_לקוח": socket_object }
connected_clients = {} 

def handle_client(client_socket, client_address):
    """
    פונקציה זו רצה ב-Thread נפרד עבור כל לקוח.
    היא מטפלת בניתוב ההודעות בין לקוחות.
    """
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    current_username = None
    
    try:
        # שלב 1: רישום
        client_socket.send("ENTER_NAME".encode('utf-8'))
        current_username = client_socket.recv(1024).decode('utf-8')
        
        # בדיקה שהשם לא תפוס כבר
        if current_username in connected_clients:
            client_socket.send("Name already taken. Reconnect with a different name.".encode('utf-8'))
            client_socket.close()
            return

        connected_clients[current_username] = client_socket
        print(f"[REGISTERED] User '{current_username}' added to directory.")
        
        # שליחת הודעת ברוכים הבאים עם הוראות
        welcome_msg = f"Welcome {current_username}!\nTo send a message, type: @Username YourMessage\nExample: @Bob Hi there!"
        client_socket.send(welcome_msg.encode('utf-8'))

        # שלב 2: לולאת הניתוב
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break 
            
            print(f"[{current_username}] sent: {msg}")
            
            # --- לוגיקת הניתוב (Routing Logic) ---
            if msg.startswith('@'):
                # פירמוט: @TargetName Message...
                try:
                    # פיצול ההודעה במרווח הראשון בלבד
                    target_name, content = msg.split(' ', 1)
                    target_name = target_name[1:] # הורדת ה-@ מהשם
                    
                    if target_name in connected_clients:
                        target_socket = connected_clients[target_name]
                        # בניית ההודעה הסופית
                        final_msg = f"[From {current_username}]: {content}"
                        target_socket.send(final_msg.encode('utf-8'))
                    else:
                        error_msg = f"[SERVER]: User '{target_name}' not found."
                        client_socket.send(error_msg.encode('utf-8'))
                        
                except ValueError:
                    # מקרה שבו המשתמש כתב רק @Name בלי הודעה
                    client_socket.send("[SERVER]: Message format error. Use: @Name Message".encode('utf-8'))
            
            elif msg.lower() == 'list':
                # פיצ'ר בונוס: הצגת רשימת מחוברים
                online_users = ", ".join(connected_clients.keys())
                client_socket.send(f"[SERVER] Online users: {online_users}".encode('utf-8'))
                
            else:
                client_socket.send("[SERVER]: Invalid format. Please use '@TargetName Message'".encode('utf-8'))
            
    except Exception as e:
        print(f"[ERROR] with user {current_username}: {e}")
        
    finally:
        if current_username and current_username in connected_clients:
            del connected_clients[current_username]
        client_socket.close()
        print(f"[DISCONNECT] {client_address} disconnected.")

def start_server():
    """
    הפונקציה הראשית שמקימה את השרת ומאזינה לחיבורים נכנסים
    """
    # 1. יצירת סוקט מסוג TCP (SOCK_STREAM) ו-IPv4 (AF_INET)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. קישור הסוקט לכתובת ולפורט (Binding)
    server.bind((SERVER_IP, SERVER_PORT))
    
    # 3. התחלת האזנה
    server.listen(MAX_CLIENTS)
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        # 4. קבלת חיבור חדש (פעולה חוסמת - מחכה עד שמישהו מתחבר)
        client_sock, addr = server.accept()
        
        # 5. יצירת Thread חדש לטיפול בלקוח, כדי שהשרת יהיה פנוי לקבל עוד לקוחות
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()
        
        # הדפסה כמה תהליכונים פעילים (מינוס 1 שהוא הראשי) = מספר הלקוחות
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()