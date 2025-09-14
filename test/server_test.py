import requests
import time
import sys
import re

def test_flask_app():
    time.sleep(20)
    
    created_task_ids = []
    
    try:
        # בדיקה 1: דף הבית
        home_response = requests.get("http://flask_app:5000/")
        
        if home_response.status_code != 200:
            print(1)
            return False
        
        # בדיקה 2: הוספת משימה ראשונה
        url = "http://flask_app:5000/add"
        data = {"title": "new task"}
        response = requests.post(url, data=data)
        
        # קבלת הדף מחדש כדי לראות את המשימה החדשה
        home_response = requests.get("http://flask_app:5000/")
        if home_response.status_code == 200:
            # חיפוש אחר המשימה החדשה ב-HTML
            task_matches = re.findall(r'(\d+) \| new task', home_response.text)
            if task_matches:
                task_id = int(task_matches[0])
                created_task_ids.append(task_id)
        
        # בדיקה 3: הוספת משימה שנייה
        data2 = {"title": "second task"}
        response2 = requests.post(url, data=data2)
        
        # קבלת הדף מחדש כדי לראות את המשימה השנייה
        home_response = requests.get("http://flask_app:5000/")
        if home_response.status_code == 200:
            # חיפוש אחר המשימה השנייה ב-HTML
            task_matches = re.findall(r'(\d+) \| second task', home_response.text)
            if task_matches:
                task_id = int(task_matches[0])
                created_task_ids.append(task_id)
        
        # בדיקה 4: מחיקת כל המשימות שיצרנו
        for task_id in created_task_ids:
            delete_url = f"http://flask_app:5000/delete/{task_id}"
            delete_response = requests.get(delete_url)
            
            if delete_response.status_code != 200:
                print(1)
                return False
        
        # בדיקה סופית: וידוא שהמשימות נמחקו
        final_response = requests.get("http://flask_app:5000/")
        if final_response.status_code == 200:
            for task_id in created_task_ids:
                if f"{task_id} |" in final_response.text:
                    print(1)
                    return False
        
        print(0)
        return True
        
    except Exception as e:
        # נסיון לנקות משימות שנוצרו גם במקרה של שגיאה
        for task_id in created_task_ids:
            try:
                delete_url = f"http://flask_app:5000/delete/{task_id}"
                requests.get(delete_url)
            except:
                pass
        print(1)
        return False

if __name__ == "__main__":
    success = test_flask_app()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)