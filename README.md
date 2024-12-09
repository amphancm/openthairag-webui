สวัสดีครับ Project นี้เป็น Project ที่ใช้สำหรับการทำสอบ Model OpenThaiGPT โดยผม ทำการเพิ่ม
- ระบบ WebUI ให้สามารถ
  - เพิ่ม/ลบ/แก้ไข Document ได้เอง โดยที่ไม่ต้องใช้คำสั่ง
  - สามารถตั้งค่า System Prompt ได้โดยไม่ต้องใส่ ใน code
  - ระบบทดสอบ Prompt ในรูป แปป chat ที่สามารถ แก้ไข Prompt ได้
  - ระบบ settting ที่สามารถเชื่อมต่อกับ line ได้ทันที อ่านได้ที่หัวข้อ #Line ChatBot

#วิธีการใช้งาน
  1. docker-compose build
  2. docker-compose up
  3. Goto localhost:8080 (Frontend)
  4. Goto localhost:5000 (Backend)

#Line ChatBot
  1. เปิดหน้า settings ขึ้นมา และนำข้อมูลจาก Line Developer มาใส่ให้ถูกต้อง
  2. นำ Channel Key มาใส่ในช่อง Line Secret Channel Key 
  3. generate Channel access token และนำ มาใส่ในช่อง Line Issue Key
  4. ทำการกดบันทึก Save
  5. ทำการ link webhook ของ Line กับ ตัว webui (ถ้าใคร ไม่มี server สามารถ ใช้ function port ใน vscode ได้ https://code.visualstudio.com/docs/editor/port-forwarding)
  6. ทำการ verify และทดสอบใช้งาน
