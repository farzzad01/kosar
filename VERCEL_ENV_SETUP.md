# إعداد متغيرات البيئة على Vercel

## المشكلة
عند نشر المشروع على Vercel، لا يمكن رفع ملف الاعتماد (credentials file) مباشرة لأسباب أمنية. بدلاً من ذلك، يجب استخدام متغيرات البيئة.

## الحل

### 1. تحويل ملف JSON إلى متغير بيئة

افتح ملف `decent-destiny-466517-k1-18a0c65a31ea.json` وانسخ محتواه بالكامل (يجب أن يكون JSON واحد في سطر واحد أو متعدد الأسطر).

### 2. إضافة المتغير على Vercel

1. اذهب إلى لوحة تحكم Vercel: https://vercel.com/dashboard
2. اختر مشروعك
3. اذهب إلى **Settings** → **Environment Variables**
4. أضف متغير جديد:
   - **Name**: `GOOGLE_CREDENTIALS_JSON`
   - **Value**: الصق محتوى ملف JSON بالكامل
   - **Environment**: اختر جميع البيئات (Production, Preview, Development)
5. اضغط **Save**

### 3. إعادة النشر

بعد إضافة المتغير، يجب إعادة نشر المشروع:

```bash
git add .
git commit -m "Update Google credentials handling"
git push
```

أو من لوحة Vercel:
- اذهب إلى **Deployments**
- اضغط على النقاط الثلاث بجانب آخر deployment
- اختر **Redeploy**

## التحقق من الإعداد

بعد إعادة النشر، جرب تسجيل طالب جديد. يجب أن يعمل رفع الملفات والحفظ في Google Sheets بدون مشاكل.

## ملاحظات مهمة

- **لا ترفع ملف الاعتماد إلى Git**: تأكد من أن الملف موجود في `.gitignore`
- **JSON صحيح**: تأكد من أن JSON صالح (بدون أخطاء في الأقواس أو الفواصل)
- **الأذونات**: تأكد من أن حساب الخدمة له صلاحيات الوصول إلى Google Drive و Google Sheets

## البيئة المحلية

في البيئة المحلية، سيستمر الكود في استخدام ملف JSON مباشرة، لذا لا حاجة لتغيير أي شيء في التطوير المحلي.

## استكشاف الأخطاء

إذا استمرت المشكلة:

1. تحقق من أن المتغير `GOOGLE_CREDENTIALS_JSON` موجود في Vercel
2. تحقق من أن JSON صالح (استخدم أداة JSON validator)
3. تحقق من logs في Vercel Dashboard → Deployments → View Function Logs
4. تأكد من أن حساب الخدمة له الصلاحيات المطلوبة

## مثال على محتوى المتغير

يجب أن يكون المتغير بهذا الشكل (مثال):

```json
{
  "type": "service_account",
  "project_id": "decent-destiny-466517-k1",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```
