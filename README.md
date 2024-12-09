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
  1. เปิดหน้า system prompt ขึ้นมา และกรอกข้อมูล
     
    1.1 Temperature (ความซื่อตรงของข้อมูล มีค่า 0.1-1.0 ยิ่งเลขเยอะความคิดสร้างสรรค์เยอะ ยิ่งเลขน้อยยิ่งซื่อตรง )
    1.2 System Prompt (ตัวตนของ AI ที่เราอยากให้เป็น เช่น ตอนนี้คุณคือ AI เลขาที่ช่วย ตอบคำถามลูกค้า ที่ติดต่อเข้ามาเพื่อสอบถาม Promotion ของสินค้า. เป็นต้น โดยยิ่งข้อมูลละเอียด AI ยิ่งตอบตรงคำถามขึ้น)
    
  1. เปิดหน้า settings ขึ้นมา และนำข้อมูลจาก Line Developer มาใส่ให้ถูกต้อง
  2. นำ Channel Key มาใส่ในช่อง Line Secret Channel Key 
  3. generate Channel access token และนำ มาใส่ในช่อง Line Issue Key
  4. ทำการกดบันทึก Save
  5. ทำการ link webhook ของ Line กับ ตัว webui โดยใช้ url ของ คุณ และ Path : /line_callback เช่น https://example.com/line_callback (ถ้าใคร ไม่มี server สามารถ ใช้ function port ใน vscode ได้ https://code.visualstudio.com/docs/editor/port-forwarding)
  6. ทำการ verify และทดสอบใช้งาน

การแก้ปัญหาเบื้องต้น
  - ถ้าใช้งานไม่ได้ ให้ทำการปิด docker-compose down และ docker-compose down อีกครั้ง
