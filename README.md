# 👁️ Eye Tracking System for Parkinson’s Detection

This project is a wearable system that tracks eye movement in real time to detect key Parkinson's symptoms like abnormal saccades and blinking patterns. It uses an infrared camera, a Raspberry Pi Zero 2 W, and a custom Python-based feature extraction pipeline.

---

## 🧠 What It Does

- Detects pupil position (x, y)
- Calculates pupil area and axes
- Tracks blink rate
- Identifies saccades (fast eye movements)
- Sends data wirelessly to laptop
- Ready for AI model integration

---

## 🔧 Hardware Used

- Raspberry Pi Zero 2 W
- Raspberry Pi Camera Module 3 NoIR Wide)
- 2x IR LEDs
- MicroSD card (32GB Class 10)
- Micro USB cable + power supply
- 3D printed PLA/ABS frame

---

## 💻 Software Used

- Raspberry Pi OS Lite
- Python 3
- OpenCV
- NumPy
- SciPy
- TensorFlow (on laptop side)

---

## 📝 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

✅ You are free to use, modify, and share this project — just **give credit to the original author**.

---

## 🙋‍♂️ Author

**Ujjwal Aggarwal**  
📧 uaggarwal1_be23@thapar.edu  
🔗 [github.com/ujjwx1](https://github.com/ujjwx1)

---

## 🔄 Future Work

- Add head movement tracking  
- Build on-device AI classification  
- Extend to full clinical testing
