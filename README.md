# 🖐️ Advanced Sign Language Translator 🚀

**Advanced Sign Language Translator** is a Python desktop application that translates hand gestures into text in real time, with interactive tools for learning sign language.
It works entirely **offline** on your local machine, without relying on cloud services, ensuring your **privacy** and **full control**.

---

## ✨ Features

### 📱 Live Gesture Translation

* Real-time hand gesture recognition via webcam.
* Instant text translation of detected signs.
* Visual hand landmark overlays on the video feed.

### 🎯 Interactive Learning Mode

* Select a specific sign to practice.
* Get immediate feedback on gesture accuracy.

### 🔤 Text-to-Sign Conversion

* Input a word or phrase to receive detailed step-by-step instructions for performing the sign.
* *(Future upgrade)* Show animated GIFs or short video clips for each sign.

### 🌐 Multi-Language Support

* Switch seamlessly between **Arabic** and **English** for both UI and translation output.

### 🎥 Customizable Camera Settings

* Automatically detects all connected webcams.
* Choose your preferred camera from a dropdown list.

### 🖥️ Modern Desktop Interface

* Built with Tkinter and styled with ttk for a clean, professional look.
* Organized into tabs: *Live Translation, Learning Mode, Text-to-Sign*.

---

## 🚀 Getting Started

### 1. Install Requirements

#### Install Python 3.8+

[Download Python](https://www.python.org/downloads/)

#### Install Git (optional)

[Download Git](https://git-scm.com/downloads)

#### Clone the project and set up a virtual environment:

```bash
git clone https://github.com/username/Advanced-Sign-Language-Translator.git
cd Advanced-Sign-Language-Translator
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Run the Application

```bash
python main_translator_app.py
```

📌 The application window will open automatically.

---

## 🎮 How to Use

### 🖐️ Live Translation

1. Open the **Live Translation** tab.
2. Click **Start Camera**.
3. Perform gestures in front of the camera to see instant translations.

### 🎯 Learning Mode

1. Open the **Learning Mode** tab.
2. Select a sign from the dropdown list (e.g., *Hello*, *Thank You*).
3. Click **Start Camera** and begin practicing.

### 🔤 Text-to-Sign

1. Open the **Text-to-Sign** tab.
2. Enter a word or phrase.
3. Click **Translate** to view step-by-step sign instructions.

---

## 🧠 How Gesture Recognition Works

The application uses **MediaPipe** to detect **21 hand landmarks** and analyze their positions.
Instead of a deep learning model, a **rule-based system** is used to match gestures with predefined patterns.

| Gesture     | Rule                              |
| ----------- | --------------------------------- |
| ✋ Open Hand | All fingers extended upward.      |
| ✊ Fist      | All fingers curled into the palm. |
| 👍 Yes      | Fist with thumb extended upward.  |

---

## 📂 Project Structure

```
Advanced-Sign-Language-Translator/
├── main_translator_app.py   # Main application code
├── README.md                # This file
├── LICENSE                  # License information
└── requirements.txt         # Python dependencies
```

---

## 🔮 Future Enhancements

* Integrate AI-based gesture recognition for higher accuracy.
* Show videos or animated images for each sign.
* Support dual-hand sign recognition.
* Optimize performance with GPU acceleration.
* Package as a standalone executable for Windows/Mac/Linux.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes, then commit:

```bash
git commit -m "Add my feature"
git push origin feature/my-feature
```

4. Open a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.
