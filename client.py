import socket
import threading
import sys

# --- הגדרות חיבור ---
# חייב להיות זהה למה שהגדרנו בשרת
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

def receive_messages(sock):
    """
    פונקציה שרצה ברקע ומאזינה להודעות מהשרת.
    היא מדפיסה כל מה שמגיע למסך.
    """
    while True:
        try:
            # קבלת הודעה (עד 1024 בייטים)
            message = sock.recv(1024).decode('utf-8')
            
            if not message:
                # אם קיבלנו הודעה ריקה, סימן שהשרת סגר את החיבור
                print("\n[DISCONNECTED] Server closed the connection.")
                sock.close()
                sys.exit() # סגירת התוכנה
            
            # הדפסת ההודעה שהתקבלה
            # אם ההודעה היא "ENTER_NAME", נדפיס הוראה ברורה
            if message == "ENTER_NAME":
                print(">>> Please enter your username to login:")
            else:
                print(f"\n{message}")
                
        except Exception as e:
            print(f"\n[ERROR] Connection lost: {e}")
            sock.close()
            break

def start_client():
    # 1. יצירת סוקט TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. התחברות לשרת
        client.connect((SERVER_IP, SERVER_PORT))
    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
        return

    # 3. הפעלת ת'רד להאזנה (כדי שנוכל לקבל הודעות בזמן שאנחנו מקלידים)
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    # daemon=True אומר שהת'רד ימות ברגע שהתוכנית הראשית נסגרת
    receive_thread.daemon = True 
    receive_thread.start()

    # 4. הלולאה הראשית - שליחת הודעות
    while True:
        try:
            msg = input() # מחכה לקלט מהמשתמש
            
            if msg.lower() == 'quit':
                break
                
            client.send(msg.encode('utf-8'))
            
        except KeyboardInterrupt:
            # טיפול ביציאה עם Ctrl+C
            break
            
    client.close()
    print("Goodbye!")

if __name__ == "__main__":
    start_client()