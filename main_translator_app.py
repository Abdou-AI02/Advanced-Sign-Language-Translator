import cv2 # مكتبة OpenCV لمعالجة الصور والفيديو
import mediapipe as mp # مكتبة MediaPipe لاكتشاف نقاط اليدين
import tkinter as tk # مكتبة Tkinter لإنشاء الواجهة الرسومية (GUI)
from tkinter import ttk, messagebox # أدوات إضافية لـ Tkinter وصناديق الرسائل
from PIL import Image, ImageTk # مكتبة Pillow للتعامل مع الصور في Tkinter
import threading # مكتبة لتشغيل الكاميرا في خيط منفصل باش الواجهة ما تتجمدش
import time # مكتبة الوقت (للتأخيرات البسيطة إذا لزم الأمر)
import numpy as np # مكتبة للتعامل مع المصفوفات العددية (مفيدة في AI)

# --- قاموس الترجمات ---
# Dictionary for translations
translations = {
    "ar": {
        "app_title": "برنامج ترجمة لغة الإشارة المتقدم",
        "translator_tab": "الترجمة المباشرة",
        "learning_tab": "وضع التعلم",
        "text_to_sign_tab": "نص إلى إشارة",
        "camera_feed": "شاشة الكاميرا",
        "detected_sign": "الإشارة المكتشفة:",
        "translated_word": "الكلمة المترجمة:",
        "no_sign": "لا توجد إشارة",
        "analyzing": "تحليل...",
        "start_camera": "تشغيل الكاميرا",
        "stop_camera": "إيقاف الكاميرا",
        "language_select": "اختر اللغة:",
        "arabic": "العربية",
        "english": "الإنجليزية",
        "camera_error": "خطأ: لا يمكن فتح الكاميرا. تأكد من أنها متصلة وتعمل بشكل صحيح.",
        "hello_gesture": "أهلاً",
        "thank_you_gesture": "شكراً",
        "yes_gesture": "نعم",
        "no_gesture": "لا",
        "open_hand_gesture": "يد مفتوحة",
        "fist_gesture": "قبضة اليد",
        "pointing_gesture": "إشارة بالسبابة",
        "camera_settings": "إعدادات الكاميرا",
        "select_camera": "اختر الكاميرا:",
        "no_cameras_found": "لم يتم العثور على كاميرات.",
        "learn_sign_prompt": "اختر إشارة للتعلم:",
        "perform_sign_instruction": "قم بالإشارة: ",
        "feedback_correct": "أحسنت! الإشارة صحيحة!",
        "feedback_try_again": "حاول مرة أخرى. هذه ليست الإشارة الصحيحة.",
        "enter_text_prompt": "أدخل نصًا للترجمة إلى إشارة:",
        "translate_button": "ترجمة",
        "sign_instruction": "تعليمات الإشارة:",
        "text_to_sign_placeholder": "سيتم عرض تعليمات الإشارة هنا.",
        "text_to_sign_hello": "لإشارة 'أهلاً': افتح يدك بالكامل، اجعل إبهامك ممدودًا للخارج قليلاً.",
        "text_to_sign_thank_you": "لإشارة 'شكراً': ضع يدك المسطحة على ذقنك ثم حركها للأمام قليلاً.",
        "text_to_sign_yes": "لإشارة 'نعم': اجعل يدك قبضة مع رفع الإبهام للأعلى.",
        "text_to_sign_no": "لإشارة 'لا': اجعل أصابع السبابة والوسطى والإبهام متصلة، مع طي الأصابع الأخرى.",
        "text_to_sign_fist": "لإشارة 'قبضة اليد': أغلق جميع أصابعك بإحكام لتشكيل قبضة.",
        "text_to_sign_open_hand": "لإشارة 'يد مفتوحة': افتح جميع أصابعك على نطاق واسع، مع إبقاء راحة اليد مفتوحة.",
        "text_to_sign_pointing": "لإشارة 'إشارة بالسبابة': مد إصبع السبابة فقط بشكل مستقيم، مع طي الأصابع الأخرى."
    },
    "en": {
        "app_title": "Advanced Sign Language Translator",
        "translator_tab": "Live Translation",
        "learning_tab": "Learning Mode",
        "text_to_sign_tab": "Text-to-Sign",
        "camera_feed": "Camera Feed",
        "detected_sign": "Detected Sign:",
        "translated_word": "Translated Word:",
        "no_sign": "No Sign",
        "analyzing": "Analyzing...",
        "start_camera": "Start Camera",
        "stop_camera": "Stop Camera",
        "language_select": "Select Language:",
        "arabic": "Arabic",
        "english": "English",
        "camera_error": "Error: Could not open camera. Make sure it's connected and working correctly.",
        "hello_gesture": "Hello",
        "thank_you_gesture": "Thank You",
        "yes_gesture": "Yes",
        "no_gesture": "No",
        "open_hand_gesture": "Open Hand",
        "fist_gesture": "Fist",
        "pointing_gesture": "Pointing Finger",
        "camera_settings": "Camera Settings",
        "select_camera": "Select Camera:",
        "no_cameras_found": "No cameras found.",
        "learn_sign_prompt": "Select a sign to learn:",
        "perform_sign_instruction": "Perform the sign for: ",
        "feedback_correct": "Excellent! Correct sign!",
        "feedback_try_again": "Try again. This is not the correct sign.",
        "enter_text_prompt": "Enter text to translate to sign:",
        "translate_button": "Translate",
        "sign_instruction": "Sign Instruction:",
        "text_to_sign_placeholder": "Sign instructions will be displayed here.",
        "text_to_sign_hello": "For 'Hello': Open your hand fully, with your thumb slightly extended outwards.",
        "text_to_sign_thank_you": "For 'Thank You': Place your flat hand on your chin, then move it slightly forward.",
        "text_to_sign_yes": "For 'Yes': Form a fist with your thumb pointing upwards.",
        "text_to_sign_no": "For 'No': Bring your index, middle, and thumb fingers together, while folding the other fingers.",
        "text_to_sign_fist": "For 'Fist': Tightly close all your fingers to form a fist.",
        "text_to_sign_open_hand": "For 'Open Hand': Spread all your fingers wide, keeping the palm open.",
        "text_to_sign_pointing": "For 'Pointing Finger': Extend only your index finger straight, while folding the other fingers."
    }
}

# --- تهيئة MediaPipe Hands (للكشف عن نقاط اليدين) ---
# Initialize MediaPipe Hands (for hand landmark detection)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- متغيرات عالمية للتحكم في الكاميرا والخيط ---
# Global variables for camera and thread control
cap = None # كائن الكاميرا
is_camera_running = False # حالة تشغيل الكاميرا
camera_thread = None # خيط تشغيل الكاميرا
current_language = tk.StringVar() # متغير Tkinter لتخزين اللغة المختارة
camera_index = tk.IntVar() # متغير Tkinter لتخزين رقم الكاميرا المحددة

# --- متغيرات وضع التعلم ---
# Learning mode variables
learning_mode_active = False
target_sign = tk.StringVar() # الإشارة المستهدفة في وضع التعلم
feedback_label = None # لتحديث رسالة التغذية الراجعة

# --- دالة التعرف على الإشارة (محاكاة لموديل AI متقدم) ---
# Gesture Recognition Function (simulation of an advanced AI model)
# هذه الدالة تحلل نقاط اليدين وتحدد الإشارة بناءً على قواعد أكثر تعقيدًا
# This function analyzes hand landmarks and determines the sign based on more complex rules
def detect_gesture(hand_landmarks):
    landmark = hand_landmarks.landmark

    # Helper function to calculate distance between two landmarks
    # دالة مساعدة لحساب المسافة بين نقطتين
    def dist(p1, p2):
        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

    # Get coordinates of finger tips and their bases (MCP - Metacarpophalangeal Joint)
    # الحصول على إحداثيات أطراف الأصابع وقواعدها
    thumb_tip = landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_mcp = landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Check finger extension (fingertip is above its base for vertical extension)
    # التحقق من تمدد الأصابع (طرف الإصبع أعلى من قاعدته للتمدد العمودي)
    is_index_extended = index_tip.y < index_mcp.y
    is_middle_extended = middle_tip.y < middle_mcp.y
    is_ring_extended = ring_tip.y < ring_mcp.y
    is_pinky_extended = pinky_tip.y < pinky_mcp.y

    # Check thumb extension (simplified, more complex for real ASL)
    # التحقق من تمدد الإبهام (مبسط، أكثر تعقيدًا للغة الإشارة الأمريكية الحقيقية)
    # Thumb tip should be significantly away from the palm base
    thumb_ip = landmark[mp_hands.HandLandmark.THUMB_IP] # Interphalangeal joint of thumb
    thumb_cmc = landmark[mp_hands.HandLandmark.THUMB_CMC] # Carpometacarpal joint of thumb
    is_thumb_extended = dist(thumb_tip, thumb_ip) > dist(thumb_ip, thumb_cmc) * 0.8 # Check if thumb is relatively straight

    # --- قواعد التعرف على الإشارات (محاكاة لموديل AI) ---
    # --- Sign Recognition Rules (AI Model Simulation) ---

    # "Hello" (ASL-like: Open hand, thumb extended, fingers slightly bent, palm facing out)
    # "أهلاً" (شبيهة بـ ASL: يد مفتوحة، إبهام ممدود، أصابع منحنية قليلاً، راحة اليد للخارج)
    if is_index_extended and is_middle_extended and is_ring_extended and is_pinky_extended and is_thumb_extended:
        # Check if fingers are not perfectly straight (slight bend)
        # التحقق مما إذا كانت الأصابع ليست مستقيمة تمامًا (انحناء طفيف)
        if (index_tip.y - index_mcp.y) < -0.05 and (middle_tip.y - middle_mcp.y) < -0.05: # Small negative value means slightly bent
            return "hello_gesture"

    # "Thank You" (ASL-like: Flat hand, touching chin then moving forward)
    # (Simplified to a flat hand gesture for static detection)
    # "شكراً" (شبيهة بـ ASL: يد مسطحة، تلمس الذقن ثم تتحرك للأمام)
    # (مبسطة إلى إشارة يد مسطحة للكشف الثابت)
    if is_index_extended and is_middle_extended and is_ring_extended and is_pinky_extended and not is_thumb_extended:
        # Check if thumb is tucked in
        # التحقق مما إذا كان الإبهام مطويًا
        if dist(thumb_tip, landmark[mp_hands.HandLandmark.WRIST]) < dist(index_tip, landmark[mp_hands.HandLandmark.WRIST]) * 0.5:
            return "thank_you_gesture"

    # "Yes" (ASL-like: Fist with thumb up)
    # "نعم" (شبيهة بـ ASL: قبضة مع إبهام مرفوع)
    if not is_index_extended and not is_middle_extended and not is_ring_extended and not is_pinky_extended and is_thumb_extended:
        # Check if thumb is clearly pointing up
        # التحقق مما إذا كان الإبهام يشير بوضوح إلى الأعلى
        if thumb_tip.y < landmark[mp_hands.HandLandmark.THUMB_CMC].y:
            return "yes_gesture"

    # "No" (ASL-like: Three fingers (index, middle, thumb) together, ring and pinky down)
    # "لا" (شبيهة بـ ASL: ثلاثة أصابع (السبابة، الوسطى، الإبهام) معًا، البنصر والخنصر مطويان)
    # Simplified: Index, middle, and thumb are extended, others are not
    # مبسطة: السبابة والوسطى والإبهام ممدودة، والباقي لا
    if is_index_extended and is_middle_extended and is_thumb_extended and not is_ring_extended and not is_pinky_extended:
        # Check if ring and pinky are clearly folded
        # التحقق مما إذا كان البنصر والخنصر مطويين بوضوح
        if ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
            return "no_gesture"

    # "Fist" (قبضة اليد)
    # "Fist"
    if not is_index_extended and not is_middle_extended and not is_ring_extended and not is_pinky_extended and not is_thumb_extended:
        return "fist_gesture"

    # "Open Hand" (يد مفتوحة - عامة)
    # "Open Hand" (general)
    if is_index_extended and is_middle_extended and is_ring_extended and is_pinky_extended and is_thumb_extended:
        return "open_hand_gesture"

    # "Pointing Finger" (إشارة بالسبابة)
    # "Pointing Finger"
    if is_index_extended and not is_middle_extended and not is_ring_extended and not is_pinky_extended and not is_thumb_extended:
        return "pointing_gesture"

    # If no specific sign is recognized
    # إذا لم يتم التعرف على إشارة محددة
    return None

# --- دالة تحديث إطار الكاميرا والتعرف على الإشارة ---
# Function to update camera frame and recognize sign
def update_frame():
    global cap, is_camera_running, learning_mode_active, feedback_label
    if not is_camera_running:
        return

    ret, frame = cap.read()
    if not ret:
        messagebox.showerror(translations[current_language.get()]["app_title"], translations[current_language.get()]["camera_error"])
        stop_camera()
        return

    # قلب الإطار أفقيا
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    # تحويل الإطار من BGR إلى RGB
    # Convert frame from BGR to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # معالجة الإطار لاكتشاف اليدين
    # Process the frame to detect hands
    results = hands.process(img_rgb)

    detected_sign_key = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # رسم نقاط اليد والوصلات
            # Draw hand landmarks and connections
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            detected_sign_key = detect_gesture(hand_landmarks)
            break # نكتفي باليد الأولى المكتشفة

    # تحديث النصوص في الواجهة الرسومية (لتبويب الترجمة المباشرة)
    # Update texts in the GUI (for Live Translation tab)
    lang = current_language.get()
    if detected_sign_key:
        detected_sign_label.config(text=f"{translations[lang]['detected_sign']} {translations[lang][detected_sign_key]}")
        translated_word_label.config(text=f"{translations[lang]['translated_word']} {translations[lang][detected_sign_key]}")
    else:
        detected_sign_label.config(text=f"{translations[lang]['detected_sign']} {translations[lang]['no_sign']}")
        translated_word_label.config(text=f"{translations[lang]['translated_word']} {translations[lang]['analyzing']}")

    # منطق وضع التعلم
    # Learning mode logic
    if learning_mode_active and feedback_label:
        if detected_sign_key == target_sign.get():
            feedback_label.config(text=translations[lang]["feedback_correct"], foreground="green")
        else:
            feedback_label.config(text=translations[lang]["feedback_try_again"], foreground="red")


    # تحويل إطار OpenCV إلى صورة Tkinter
    # Convert OpenCV frame to Tkinter image
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.config(image=imgtk)

    # إعادة تشغيل الدالة بعد 10 ميلي ثانية
    # Rerun the function after 10 milliseconds
    video_label.after(10, update_frame)

# --- دالة تشغيل الكاميرا ---
# Function to start the camera
def start_camera():
    global cap, is_camera_running, camera_thread
    if not is_camera_running:
        selected_cam_idx = camera_index.get()
        cap = cv2.VideoCapture(selected_cam_idx) # فتح الكاميرا المختارة
        if not cap.isOpened():
            messagebox.showerror(translations[current_language.get()]["app_title"], translations[current_language.get()]["camera_error"])
            return

        is_camera_running = True
        # تشغيل دالة تحديث الإطار في خيط منفصل
        # Run update_frame function in a separate thread
        camera_thread = threading.Thread(target=update_frame)
        camera_thread.daemon = True # يجعل الخيط يتوقف عند إغلاق البرنامج الرئيسي
        camera_thread.start()
        start_button.config(state=tk.DISABLED) # تعطيل زر التشغيل
        stop_button.config(state=tk.NORMAL) # تفعيل زر الإيقاف
        camera_dropdown.config(state=tk.DISABLED) # تعطيل قائمة الكاميرات

# --- دالة إيقاف الكاميرا ---
# Function to stop the camera
def stop_camera():
    global cap, is_camera_running
    is_camera_running = False
    if cap:
        cap.release() # تحرير موارد الكاميرا
    video_label.config(image='') # مسح الصورة من شاشة العرض
    detected_sign_label.config(text=f"{translations[current_language.get()]['detected_sign']} {translations[current_language.get()]['no_sign']}")
    translated_word_label.config(text=f"{translations[current_language.get()]['translated_word']} {translations[current_language.get()]['no_sign']}")
    start_button.config(state=tk.NORMAL) # تفعيل زر التشغيل
    stop_button.config(state=tk.DISABLED) # تعطيل زر الإيقاف
    camera_dropdown.config(state=tk.NORMAL) # تفعيل قائمة الكاميرات

# --- دالة تحديث نصوص الواجهة عند تغيير اللغة ---
# Function to update GUI texts when language changes
def update_gui_texts():
    lang = current_language.get()
    root.title(translations[lang]["app_title"])
    notebook.tab(0, text=translations[lang]["translator_tab"])
    notebook.tab(1, text=translations[lang]["learning_tab"])
    notebook.tab(2, text=translations[lang]["text_to_sign_tab"])

    camera_frame_label.config(text=translations[lang]["camera_feed"])
    start_button.config(text=translations[lang]["start_camera"])
    stop_button.config(text=translations[lang]["stop_camera"])
    lang_label.config(text=translations[lang]["language_select"])
    arabic_radio.config(text=translations[lang]["arabic"])
    english_radio.config(text=translations[lang]["english"])

    camera_settings_label.config(text=translations[lang]["camera_settings"])
    select_camera_label.config(text=translations[lang]["select_camera"])

    learn_sign_prompt_label.config(text=translations[lang]["learn_sign_prompt"])
    perform_sign_instruction_label.config(text=f"{translations[lang]['perform_sign_instruction']} {translations[lang][target_sign.get()] if target_sign.get() else ''}")

    enter_text_prompt_label.config(text=translations[lang]["enter_text_prompt"])
    translate_button.config(text=translations[lang]["translate_button"])
    sign_instruction_label.config(text=translations[lang]["sign_instruction"])
    text_to_sign_output_label.config(text=translations[lang]["text_to_sign_placeholder"])

    # تحديث حالة النصوص المكتشفة أيضًا
    # Update the detected texts as well
    if not is_camera_running:
        detected_sign_label.config(text=f"{translations[lang]['detected_sign']} {translations[lang]['no_sign']}")
        translated_word_label.config(text=f"{translations[lang]['translated_word']} {translations[lang]['no_sign']}")
    else:
        # إذا كانت الكاميرا شغالة، نتركها تحدث نفسها في الخيط
        # If camera is running, let it update itself in the thread
        pass

# --- دالة جلب الكاميرات المتاحة ---
# Function to get available cameras
def get_available_cameras():
    available_cameras = []
    for i in range(10): # جرب أول 10 كاميرات
        cap_test = cv2.VideoCapture(i)
        if cap_test.isOpened():
            available_cameras.append(str(i))
            cap_test.release()
        else:
            cap_test.release() # تأكد من إغلاقها حتى لو لم تفتح
            # If a camera index fails, subsequent ones might also fail, so break
            # if i > 0 and not available_cameras: # Optimization: if first camera fails, break
            #     break
    return available_cameras

# --- دالة تشغيل وضع التعلم ---
# Function to activate learning mode
def activate_learning_mode():
    global learning_mode_active, feedback_label
    learning_mode_active = True
    lang = current_language.get()
    perform_sign_instruction_label.config(text=f"{translations[lang]['perform_sign_instruction']} {translations[lang][target_sign.get()]}")
    feedback_label.config(text="") # مسح التغذية الراجعة السابقة

# --- دالة إيقاف وضع التعلم ---
# Function to deactivate learning mode
def deactivate_learning_mode():
    global learning_mode_active
    learning_mode_active = False
    feedback_label.config(text="") # مسح التغذية الراجعة

# --- دالة الترجمة من نص إلى إشارة ---
# Function for Text-to-Sign translation
def translate_text_to_sign():
    text = text_input_entry.get().strip().lower()
    lang = current_language.get()
    instruction = translations[lang]["text_to_sign_placeholder"]

    # ربط الكلمات بالإشارات المحاكية
    # Map words to simulated signs
    if "hello" in text or "أهلاً" in text or "مرحبا" in text:
        instruction = translations[lang]["text_to_sign_hello"]
    elif "thank you" in text or "شكرا" in text:
        instruction = translations[lang]["text_to_sign_thank_you"]
    elif "yes" in text or "نعم" in text:
        instruction = translations[lang]["text_to_sign_yes"]
    elif "no" in text or "لا" in text:
        instruction = translations[lang]["text_to_sign_no"]
    elif "fist" in text or "قبضة" in text:
        instruction = translations[lang]["text_to_sign_fist"]
    elif "open hand" in text or "يد مفتوحة" in text:
        instruction = translations[lang]["text_to_sign_open_hand"]
    elif "point" in text or "إشارة" in text:
        instruction = translations[lang]["text_to_sign_pointing"]
    
    text_to_sign_output_label.config(text=instruction)

# --- إعداد الواجهة الرسومية (Tkinter) ---
# GUI Setup (Tkinter)
root = tk.Tk()
root.title(translations["ar"]["app_title"]) # العنوان الأولي بالعربية
root.geometry("1000x800") # حجم النافذة
root.resizable(False, False) # منع تغيير حجم النافذة

# ضبط الثيم (Theme) لـ ttk
# Set ttk theme
style = ttk.Style()
style.theme_use("clam") # "clam", "alt", "default", "classic"
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)
style.map("TButton",
    foreground=[('active', 'white')],
    background=[('active', '#4CAF50')]
)
style.configure("TLabelframe", background="#e0e0e0", font=("Helvetica", 14, "bold"))
style.configure("TLabelframe.Label", background="#e0e0e0")
style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))
style.map("TNotebook.Tab",
    background=[('selected', '#4CAF50')],
    foreground=[('selected', 'white')]
)

# Notebook (الألسنة)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- تبويب الترجمة المباشرة (Live Translation Tab) ---
translator_tab = ttk.Frame(notebook)
notebook.add(translator_tab, text=translations["ar"]["translator_tab"])

# إطار للكاميرا
camera_frame_label = ttk.LabelFrame(translator_tab, text=translations["ar"]["camera_feed"], padding="10 10 10 10")
camera_frame_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

video_label = ttk.Label(camera_frame_label)
video_label.pack(fill=tk.BOTH, expand=True)

# إطار للتحكم والنتائج
control_result_frame = ttk.Frame(translator_tab, padding="10 10 10 10")
control_result_frame.pack(pady=10, padx=10, fill=tk.X)
control_result_frame.columnconfigure(0, weight=1)
control_result_frame.columnconfigure(1, weight=1)

# أزرار التحكم
control_buttons_frame = ttk.Frame(control_result_frame)
control_buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

start_button = ttk.Button(control_buttons_frame, text=translations["ar"]["start_camera"], command=start_camera)
start_button.pack(pady=5, fill=tk.X)

stop_button = ttk.Button(control_buttons_frame, text=translations["ar"]["stop_camera"], command=stop_camera, state=tk.DISABLED)
stop_button.pack(pady=5, fill=tk.X)

# إطار للنتائج
result_display_frame = ttk.Frame(control_result_frame)
result_display_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

detected_sign_label = ttk.Label(result_display_frame, text=f"{translations['ar']['detected_sign']} {translations['ar']['no_sign']}", font=("Helvetica", 14, "bold"))
detected_sign_label.pack(pady=5, anchor=tk.W)

translated_word_label = ttk.Label(result_display_frame, text=f"{translations['ar']['translated_word']} {translations['ar']['no_sign']}", font=("Helvetica", 14, "bold"))
translated_word_label.pack(pady=5, anchor=tk.W)

# إعدادات الكاميرا
camera_settings_frame = ttk.LabelFrame(translator_tab, text=translations["ar"]["camera_settings"], padding="10 10 10 10")
camera_settings_frame.pack(pady=10, padx=10, fill=tk.X)

select_camera_label = ttk.Label(camera_settings_frame, text=translations["ar"]["select_camera"])
select_camera_label.pack(side=tk.LEFT, padx=5)

available_cameras = get_available_cameras()
if not available_cameras:
    available_cameras = [translations["ar"]["no_cameras_found"]]
    camera_index.set(-1) # No camera selected
else:
    camera_index.set(int(available_cameras[0])) # Select the first camera by default

camera_dropdown = ttk.Combobox(camera_settings_frame, textvariable=camera_index, values=available_cameras, state="readonly")
camera_dropdown.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
if not available_cameras or available_cameras[0] == translations["ar"]["no_cameras_found"]:
    camera_dropdown.config(state=tk.DISABLED)

# --- تبويب وضع التعلم (Learning Mode Tab) ---
learning_tab = ttk.Frame(notebook)
notebook.add(learning_tab, text=translations["ar"]["learning_tab"])

learning_controls_frame = ttk.LabelFrame(learning_tab, text=translations["ar"]["learn_sign_prompt"], padding="10 10 10 10")
learning_controls_frame.pack(pady=10, padx=10, fill=tk.X)

learnable_signs = [
    "hello_gesture", "thank_you_gesture", "yes_gesture", "no_gesture",
    "open_hand_gesture", "fist_gesture", "pointing_gesture"
]
# تهيئة قائمة الإشارات للواجهة
# Initialize sign list for GUI
translated_learnable_signs = [translations["ar"][s] for s in learnable_signs]

target_sign_dropdown = ttk.Combobox(learning_controls_frame, values=translated_learnable_signs, state="readonly")
target_sign_dropdown.pack(pady=5, fill=tk.X)
target_sign_dropdown.bind("<<ComboboxSelected>>", lambda event: target_sign.set(learnable_signs[translated_learnable_signs.index(target_sign_dropdown.get())]))

# ربط متغير target_sign بـ target_sign_dropdown
# Link target_sign variable to target_sign_dropdown
target_sign.trace_add("write", lambda *args: perform_sign_instruction_label.config(text=f"{translations[current_language.get()]['perform_sign_instruction']} {translations[current_language.get()][target_sign.get()]}"))


start_learning_button = ttk.Button(learning_controls_frame, text=translations["ar"]["start_camera"], command=lambda: (start_camera(), activate_learning_mode()))
start_learning_button.pack(pady=5, fill=tk.X)

stop_learning_button = ttk.Button(learning_controls_frame, text=translations["ar"]["stop_camera"], command=lambda: (stop_camera(), deactivate_learning_mode()), state=tk.DISABLED)
stop_learning_button.pack(pady=5, fill=tk.X)

# ربط حالة أزرار التعلم بحالة الكاميرا
# Link learning button states to camera state
start_button.config(command=lambda: (start_camera(), deactivate_learning_mode())) # عند تشغيل الكاميرا في تبويب الترجمة، نوقف وضع التعلم
stop_button.config(command=lambda: (stop_camera(), deactivate_learning_mode()))

# تحديث حالة أزرار التعلم
def update_learning_buttons_state():
    if is_camera_running:
        start_learning_button.config(state=tk.DISABLED)
        stop_learning_button.config(state=tk.NORMAL)
    else:
        start_learning_button.config(state=tk.NORMAL)
        stop_learning_button.config(state=tk.DISABLED)
root.after(100, update_learning_buttons_state) # تحديث أولي

# مكان لعرض تعليمات الإشارة والتغذية الراجعة
perform_sign_instruction_label = ttk.Label(learning_tab, text="", font=("Helvetica", 16, "bold"), foreground="blue")
perform_sign_instruction_label.pack(pady=20)

feedback_label = ttk.Label(learning_tab, text="", font=("Helvetica", 18, "bold"))
feedback_label.pack(pady=10)

# --- تبويب الترجمة من نص إلى إشارة (Text-to-Sign Tab) ---
text_to_sign_tab = ttk.Frame(notebook)
notebook.add(text_to_sign_tab, text=translations["ar"]["text_to_sign_tab"])

text_input_frame = ttk.LabelFrame(text_to_sign_tab, text=translations["ar"]["enter_text_prompt"], padding="10 10 10 10")
text_input_frame.pack(pady=10, padx=10, fill=tk.X)

text_input_entry = ttk.Entry(text_input_frame, font=("Helvetica", 14))
text_input_entry.pack(pady=5, fill=tk.X)

translate_button = ttk.Button(text_input_frame, text=translations["ar"]["translate_button"], command=translate_text_to_sign)
translate_button.pack(pady=5)

sign_instruction_label = ttk.Label(text_to_sign_tab, text=translations["ar"]["sign_instruction"], font=("Helvetica", 14, "bold"))
sign_instruction_label.pack(pady=10, anchor=tk.W)

text_to_sign_output_label = ttk.Label(text_to_sign_tab, text=translations["ar"]["text_to_sign_placeholder"], font=("Helvetica", 12), wraplength=700, justify=tk.LEFT)
text_to_sign_output_label.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

# --- إطار لاختيار اللغة (Language Selection Frame) ---
lang_frame = ttk.LabelFrame(root, text=translations["ar"]["language_select"], padding="10 10 10 10")
lang_frame.pack(pady=10, padx=10, fill=tk.X)

current_language.set("ar") # اللغة الافتراضية هي العربية
current_language.trace_add("write", lambda *args: update_gui_texts()) # تحديث الواجهة عند تغيير اللغة

lang_label = ttk.Label(lang_frame, text=translations["ar"]["language_select"])
lang_label.pack(side=tk.LEFT, padx=5)

arabic_radio = ttk.Radiobutton(lang_frame, text=translations["ar"]["arabic"], variable=current_language, value="ar")
arabic_radio.pack(side=tk.LEFT, padx=10)

english_radio = ttk.Radiobutton(lang_frame, text=translations["ar"]["english"], variable=current_language, value="en")
english_radio.pack(side=tk.LEFT, padx=10)


# عند إغلاق النافذة، نوقف الكاميرا
# When closing the window, stop the camera
root.protocol("WM_DELETE_WINDOW", lambda: (stop_camera(), root.destroy()))

# تشغيل حلقة Tkinter الرئيسية
# Run the main Tkinter loop
root.mainloop()
