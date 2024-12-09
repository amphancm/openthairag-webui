สวัสดีครับ Project นี้เป็น Project ที่ใช้สำหรับการทำสอบ Model OpenThaiGPT โดยผม ทำการเพิ่ม
- ระบบ WebUI ให้สามารถ
  - เพิ่ม/ลบ/แก้ไข Document ได้เอง โดยที่ไม่ต้องใช้คำสั่ง
  - สามารถตั้งค่า System Prompt ได้โดยไม่ต้องใส่ ใน code
  - ระบบทดสอบ Prompt ในรูป แปป chat ที่สามารถ แก้ไข Prompt ได้
  - ระบบ settting ที่สามารถเชื่อมต่อกับ line ได้ทันที อ่านได้ที่หัวข้อ #Line ChatBot


วิธีการใช้งาน
  1. docker-compose build
  2. docker-compose up
  3. Goto localhost:8080 (Frontend)
  4. Goto localhost:5000 (Backend)
