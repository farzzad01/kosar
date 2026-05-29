# 📁 راهنمای تنظیم Google Drive برای آپلود فایل‌ها

## ❌ مشکل:
```
Service Accounts do not have storage quota
```

این یعنی Service Account نمی‌تونه مستقیماً فایل آپلود کنه چون فضای ذخیره‌سازی نداره!

---

## ✅ راه‌حل: استفاده از Shared Folder

### مرحله 1: پیدا کردن Service Account Email

1. فایل `decent-destiny-466517-k1-18a0c65a31ea.json` رو باز کن
2. دنبال `client_email` بگرد
3. چیزی شبیه این پیدا می‌کنی:
   ```json
   "client_email": "decent-destiny-466517-k1@decent-destiny-466517-k1.iam.gserviceaccount.com"
   ```
4. این ایمیل رو کپی کن ✂️

---

### مرحله 2: ساخت فولدر در Google Drive

1. به Google Drive برو: https://drive.google.com
2. روی **+ New** کلیک کن
3. **Folder** رو انتخاب کن
4. اسم فولدر: `Student_Registration_Files`
5. **Create** کن

---

### مرحله 3: به اشتراک گذاشتن فولدر با Service Account

1. روی فولدر راست کلیک کن
2. **Share** (اشتراک‌گذاری) رو انتخاب کن
3. در قسمت "Add people and groups":
   - ایمیل Service Account رو paste کن
   - دسترسی رو **Editor** انتخاب کن
4. ⚠️ **مهم**: تیک "Notify people" رو بردار (چون Service Account ایمیل دریافت نمی‌کنه)
5. **Share** کن

---

### مرحله 4: گرفتن Folder ID

1. فولدر رو باز کن
2. از URL کپی کن:
   ```
   https://drive.google.com/drive/folders/1ABC123XYZ456
                                          ^^^^^^^^^^^^^^^^
                                          این قسمت Folder ID هست
   ```
3. فقط قسمت بعد از `folders/` رو کپی کن

مثال:
- URL: `https://drive.google.com/drive/folders/1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlR`
- Folder ID: `1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlR`

---

### مرحله 5: اضافه کردن به Vercel Environment Variables

1. به Vercel Dashboard برو: https://vercel.com/dashboard
2. پروژه خودت رو انتخاب کن
3. **Settings** > **Environment Variables**
4. این متغیر رو اضافه کن:

```
Name: GOOGLE_DRIVE_FOLDER_ID
Value: 1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlR
```

5. **Save** کن
6. پروژه رو **Redeploy** کن

---

### مرحله 6: تست محلی (اختیاری)

برای تست محلی، فایل `.env` رو ویرایش کن:

```bash
GOOGLE_DRIVE_FOLDER_ID=1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlR
```

---

## 🧪 تست کردن

بعد از انجام مراحل بالا:

1. یه ثبت‌نام تست کن
2. چک کن که فایل‌ها در Google Sheets لینک دارن
3. روی لینک کلیک کن ببین فایل باز میشه

---

## ❓ مشکلات رایج

### خطا: "Permission denied"
**راه‌حل**: مطمئن شو که Service Account رو با دسترسی **Editor** به فولدر اضافه کردی

### خطا: "Folder not found"
**راه‌حل**: Folder ID رو دوباره چک کن، مطمئن شو که درست کپی شده

### فایل‌ها آپلود نمیشن
**راه‌حل**: 
1. لاگ‌های Vercel رو چک کن: `vercel logs`
2. دنبال پیام‌های `[ERROR]` یا `[WARNING]` بگرد

---

## ✅ چک‌لیست

- [ ] Service Account Email رو پیدا کردم
- [ ] فولدر در Google Drive ساختم
- [ ] فولدر رو با Service Account به اشتراک گذاشتم (با دسترسی Editor)
- [ ] Folder ID رو کپی کردم
- [ ] GOOGLE_DRIVE_FOLDER_ID رو در Vercel اضافه کردم
- [ ] پروژه رو Redeploy کردم
- [ ] تست کردم و کار می‌کنه! 🎉

---

## 📸 اسکرین‌شات‌های مفید

### Share Dialog:
```
┌─────────────────────────────────────┐
│ Share "Student_Registration_Files"  │
├─────────────────────────────────────┤
│ Add people and groups:              │
│ [service-account@...com] [Editor ▼] │
│                                     │
│ ☐ Notify people                     │
│                                     │
│              [Cancel]  [Share]      │
└─────────────────────────────────────┘
```

موفق باشید! 🚀
