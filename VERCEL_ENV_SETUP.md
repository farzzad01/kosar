# تنظیم Environment Variables در Vercel

برای اینکه سیستم در Vercel کار کند، باید این متغیرها را در تنظیمات Vercel اضافه کنید:

## مراحل تنظیم:

### 1. رفتن به تنظیمات Vercel
1. به پروژه خود در Vercel بروید
2. روی **Settings** کلیک کنید
3. از منوی سمت چپ **Environment Variables** را انتخاب کنید

### 2. اضافه کردن متغیرها

#### GOOGLE_CREDENTIALS_JSON (مهم!)
این متغیر باید محتوای کامل فایل `decent-destiny-466517-k1-18a0c65a31ea.json` را داشته باشد.

**مراحل:**
1. فایل `decent-destiny-466517-k1-18a0c65a31ea.json` را باز کنید
2. تمام محتوای آن را کپی کنید (باید یک JSON کامل باشد)
3. در Vercel:
   - Name: `GOOGLE_CREDENTIALS_JSON`
   - Value: محتوای کامل فایل JSON را paste کنید
   - Environment: Production, Preview, Development (هر سه را انتخاب کنید)

#### GOOGLE_SHEET_ID (اختیاری)
- Name: `GOOGLE_SHEET_ID`
- Value: `1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlRSXC79iz-8dc`
- Environment: Production, Preview, Development

#### SECRET_KEY (توصیه می‌شود)
- Name: `SECRET_KEY`
- Value: یک کلید تصادفی و امن (می‌توانید از [این سایت](https://djecrety.ir/) استفاده کنید)
- Environment: Production, Preview, Development

#### DEBUG (اختیاری)
- Name: `DEBUG`
- Value: `False`
- Environment: Production

### 3. Redeploy کردن
بعد از اضافه کردن متغیرها:
1. به تب **Deployments** بروید
2. آخرین deployment را پیدا کنید
3. روی دکمه **...** کلیک کنید
4. **Redeploy** را انتخاب کنید

## نکات مهم:

- محتوای `GOOGLE_CREDENTIALS_JSON` باید یک JSON معتبر باشد
- مطمئن شوید که فاصله یا کاراکتر اضافی در ابتدا یا انتهای JSON نباشد
- اگر خطای "Invalid JSON" گرفتید، محتوای JSON را در یک JSON validator بررسی کنید

## تست کردن:

بعد از redeploy، فرم را دوباره تست کنید. اگر همه چیز درست باشد، داده‌ها باید در Google Sheets ظاهر شوند.
