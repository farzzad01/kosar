# راهنمای کامل ساخت Google Form با اتصال به Google Sheets و Drive

## فهرست مطالب
1. [ایجاد Google Form](#مرحله-1-ایجاد-google-form)
2. [اتصال به Google Sheets](#مرحله-2-اتصال-به-google-sheets)
3. [تنظیم Google Drive برای فایل‌ها](#مرحله-3-تنظیم-google-drive)
4. [ساخت فیلدهای فرم](#مرحله-4-ساخت-فیلدهای-فرم)
5. [تنظیم Logic شرطی](#مرحله-5-تنظیم-logic-شرطی)
6. [اتوماسیون لینک‌های Drive](#مرحله-6-اتوماسیون-لینک‌های-drive)
7. [تنظیمات نهایی](#مرحله-7-تنظیمات-نهایی)

---

## مرحله 1: ایجاد Google Form

### 1.1 ساخت فرم جدید
1. به https://forms.google.com بروید
2. روی **+ (Blank Form)** کلیک کنید
3. عنوان فرم: `استمارة التسجيل - الدراسات العليا`
4. توضیحات: `يرجى ملء جميع الحقول المطلوبة بدقة`

### 1.2 تنظیمات ظاهری (Theme)
1. روی آیکون **پالت رنگ** (بالای صفحه) کلیک کنید
2. **رنگ اصلی**: طلایی - از Color picker استفاده کنید و کد `#d4af37` را وارد کنید
3. **پس‌زمینه**: Light Gray یا White
4. **فونت**: Default (Google Forms به طور خودکار عربی را تشخیص می‌دهد)

### 1.3 اضافه کردن لوگو (اختیاری)
1. روی **Add image** کلیک کنید
2. لوگو را آپلود کنید
3. Alignment: Right

---

## مرحله 2: اتصال به Google Sheets

### 2.1 ایجاد Spreadsheet
1. در Google Form، روی تب **Responses** کلیک کنید
2. روی آیکون **Google Sheets** (سبز رنگ) کلیک کنید
3. **Create a new spreadsheet** را انتخاب کنید
4. نام: `Student Registration Data`
5. روی **Create** کلیک کنید

### 2.2 تنظیم Spreadsheet
یک Google Sheet جدید باز می‌شود که به طور خودکار به فرم متصل است.

---

## مرحله 3: تنظیم Google Drive برای فایل‌ها

### 3.1 فعال‌سازی File Upload
برای استفاده از File Upload در Google Forms:
- باید از حساب Google Workspace استفاده کنید، یا
- از حساب Gmail شخصی با فضای کافی Drive

### 3.2 تنظیمات File Upload
وقتی فیلد File Upload اضافه می‌کنید:
1. **Allow specific file types**: Images, PDF
2. **Maximum file size**: 10 MB (یا بیشتر)
3. **Maximum number of files**: 1

### 3.3 پوشه ذخیره‌سازی
Google Forms به طور خودکار یک پوشه در Drive ایجاد می‌کند:
- نام پوشه: `[نام فرم] (File responses)`
- مکان: My Drive
- تمام فایل‌های آپلود شده در این پوشه ذخیره می‌شوند

---

## مرحله 4: ساخت فیلدهای فرم

### بخش 1: المعلومات الشخصية

#### فیلد 1: الاسم الثلاثي حسب جواز السفر
- **Type**: Short answer
- **Required**: ✓
- **Description**: اسم الأب والجد

#### فیلد 2: لقب العائلة حسب جواز السفر
- **Type**: Short answer
- **Required**: ✓
- **Description**: اسم العائلة

#### فیلد 3: الديانة
- **Type**: Multiple choice
- **Required**: ✓
- **Options**:
  - سني
  - شيعي
  - مسيحي
  - سرياني

#### فیلد 4: رقم الهاتف
- **Type**: Short answer
- **Required**: ✓
- **Validation**: 
  - Click on ⋮ (three dots)
  - Response validation
  - Regular expression → Matches
  - Pattern: `^\+?[0-9]{10,15}$`
  - Custom error text: `يرجى إدخال رقم هاتف صحيح`

#### فیلد 5: البريد الإلكتروني
- **Type**: Short answer
- **Required**: ✓
- **Validation**: 
  - Response validation → Email
  - Custom error text: `يرجى إدخال بريد إلكتروني صحيح`

#### فیلد 6: العنوان في العراق
- **Type**: Short answer
- **Required**: ✓
- **Description**: المحافظة والمدينة

#### فیلد 7: الوظيفة
- **Type**: Short answer
- **Required**: ✓
- **Description**: المهنة الحالية

#### فیلد 8: الحالة الاجتماعية
- **Type**: Multiple choice
- **Required**: ✓
- **Options**:
  - أعزب
  - متزوج
- **Important**: این فیلد را بعداً برای Logic شرطی تنظیم می‌کنیم

#### فیلد 9: عدد الأطفال (شرطی)
- **Type**: Short answer
- **Required**: فقط اگر "متزوج" انتخاب شد
- **Validation**: 
  - Number
  - Greater than or equal to → 0

### بخش 2: المعلومات الأكاديمية

**ایجاد Section جدید**:
1. روی آیکون **Add section** کلیک کنید
2. عنوان: `المعلومات الأكاديمية`

#### فیلد 10: نوع الجامعة
- **Type**: Multiple choice
- **Required**: ✓
- **Options**:
  - نفقة خاصة
  - ابتعاث

#### فیلد 11: المقطع الدراسي
- **Type**: Multiple choice
- **Required**: ✓
- **Options**:
  - ماجستير
  - دكتوراه
- **Important**: این فیلد را بعداً برای Logic شرطی تنظیم می‌کنیم

#### فیلد 12: التخصص المطلوب للدراسة
- **Type**: Short answer
- **Required**: ✓
- **Description**: مثال: هندسة الحاسوب، الطب، إدارة الأعمال

#### فیلد 13: اسم الجامعة السابقة (البكالوريوس)
- **Type**: Short answer
- **Required**: ✓
- **Description**: الجامعة التي تخرجت منها

#### فیلد 14: اسم الجامعة السابقة (الماجستير) - شرطی
- **Type**: Short answer
- **Required**: فقط برای دکترا
- **Description**: جامعة الماجستير

#### فیلد 15: معدل البكالوريوس
- **Type**: Short answer
- **Required**: ✓
- **Description**: مثال: 3.5 أو 85%

#### فیلد 16: معدل الماجستير - شرطی
- **Type**: Short answer
- **Required**: فقط برای دکترا
- **Description**: مثال: 3.8 أو 90%

### بخش 3: تحميل المستندات المطلوبة

**ایجاد Section جدید**:
1. روی آیکون **Add section** کلیک کنید
2. عنوان: `تحميل المستندات المطلوبة`
3. توضیحات: `⚠ يرجى تحميل صور واضحة ومقروءة`

#### فیلد 17: صورة جواز السفر
- **Type**: File upload
- **Required**: ✓
- **Description**: يرجى تحميل صورة واضحة ومقروءة لجواز السفر لضمان نجاح التسجيل
- **Settings**:
  - Allow specific file types: ✓
  - Select: Images, PDF
  - Maximum file size: 10 MB
  - Maximum number of files: 1

#### فیلد 18: صورة الشخص
- **Type**: File upload
- **Required**: ✓
- **Settings**:
  - Allow specific file types: Images, PDF
  - Maximum file size: 10 MB
  - Maximum number of files: 1

#### فیلد 19: كشف درجات البكالوريوس
- **Type**: File upload
- **Required**: ✓
- **Settings**:
  - Allow specific file types: Images, PDF
  - Maximum file size: 10 MB
  - Maximum number of files: 1

#### فیلد 20: كشف درجات الماجستير - شرطی
- **Type**: File upload
- **Required**: فقط برای دکترا
- **Settings**:
  - Allow specific file types: Images, PDF
  - Maximum file size: 10 MB
  - Maximum number of files: 1

#### فیلد 21: وثيقة الماجستير
- **Type**: File upload
- **Required**: ✓
- **Settings**:
  - Allow specific file types: Images, PDF
  - Maximum file size: 10 MB
  - Maximum number of files: 1

---

## مرحله 5: تنظیم Logic شرطی

### 5.1 Logic برای "الحالة الاجتماعية"

**هدف**: اگر "متزوج" انتخاب شد، سوال "عدد الأطفال" نمایش داده شود.

**مراحل**:
1. روی سوال **"الحالة الاجتماعية"** کلیک کنید
2. روی **⋮** (three dots) کلیک کنید
3. **"Go to section based on answer"** را انتخاب کنید
4. تنظیمات:
   - **أعزب** → Continue to next section (بخش المعلومات الأكاديمية)
   - **متزوج** → Go to section with "عدد الأطفال"

**نکته مهم**: باید یک Section جداگانه برای "عدد الأطفال" بسازید:
1. قبل از بخش "المعلومات الأكاديمية"، یک Section جدید اضافه کنید
2. فقط سوال "عدد الأطفال" را در آن قرار دهید
3. بعد از این سوال، به بخش "المعلومات الأكاديمية" برود

### 5.2 Logic برای "المقطع الدراسي"

**هدف**: اگر "دكتوراه" انتخاب شد، سوالات مربوط به ماجستیر نمایش داده شوند.

**مراحل**:
1. روی سوال **"المقطع الدراسي"** کلیک کنید
2. روی **⋮** (three dots) کلیک کنید
3. **"Go to section based on answer"** را انتخاب کنید
4. تنظیمات:
   - **ماجستير** → Skip to "تحميل المستندات" (بدون سوالات ماجستیر)
   - **دكتوراه** → Continue to next section (با سوالات ماجستیر)

**ساختار Sections پیشنهادی**:
```
Section 1: المعلومات الشخصية
  ├─ سوالات عمومی
  └─ الحالة الاجتماعية (با Logic)

Section 2: عدد الأطفال (شرطی)
  └─ عدد الأطفال

Section 3: المعلومات الأكاديمية - عمومی
  ├─ نوع الجامعة
  ├─ المقطع الدراسي (با Logic)
  ├─ التخصص
  ├─ الجامعة السابقة (البكالوريوس)
  └─ معدل البكالوريوس

Section 4: معلومات الماجستير (شرطی - فقط دکترا)
  ├─ الجامعة السابقة (الماجستير)
  └─ معدل الماجستير

Section 5: تحميل المستندات - عمومی
  ├─ صورة جواز السفر
  ├─ صورة الشخص
  ├─ كشف درجات البكالوريوس
  └─ وثيقة الماجستير

Section 6: تحميل كشف درجات الماجستير (شرطی - فقط دکترا)
  └─ كشف درجات الماجستير
```

---

## مرحله 6: اتوماسیون لینک‌های Drive در Sheets

### 6.1 مشکل پیش‌فرض
وقتی فایل‌ها آپلود می‌شوند، Google Sheets فقط **لینک مستقیم** فایل را نشان می‌دهد که کلیک روی آن فایل را دانلود می‌کند.

### 6.2 راه‌حل: استفاده از Google Apps Script

**مراحل**:

#### گام 1: باز کردن Script Editor
1. در Google Sheet متصل به فرم، روی **Extensions** کلیک کنید
2. **Apps Script** را انتخاب کنید
3. یک پروژه جدید باز می‌شود

#### گام 2: پاک کردن کد پیش‌فرض
کد موجود (`function myFunction() {}`) را پاک کنید

#### گام 3: کپی کردن کد زیر

```javascript
/**
 * تبدیل لینک‌های مستقیم فایل به لینک‌های قابل مشاهده در Drive
 * این اسکریپت به طور خودکار اجرا می‌شود وقتی فرم ارسال می‌شود
 */

function onFormSubmit(e) {
  var sheet = e.range.getSheet();
  var row = e.range.getRow();
  
  // ستون‌هایی که فایل دارند (شماره ستون‌ها را بر اساس فرم خود تنظیم کنید)
  // مثال: اگر ستون 17 = صورة جواز السفر
  var fileColumns = [17, 18, 19, 20, 21]; // شماره ستون‌های فایل
  
  fileColumns.forEach(function(col) {
    var cell = sheet.getRange(row, col);
    var value = cell.getValue();
    
    if (value && value.toString().indexOf('drive.google.com') > -1) {
      // استخراج File ID از لینک
      var fileId = extractFileId(value);
      
      if (fileId) {
        // ساخت لینک قابل مشاهده
        var viewLink = 'https://drive.google.com/file/d/' + fileId + '/view';
        
        // ساخت فرمول HYPERLINK
        var formula = '=HYPERLINK("' + viewLink + '", "مشاهده فایل")';
        cell.setFormula(formula);
      }
    }
  });
}

/**
 * استخراج File ID از لینک Google Drive
 */
function extractFileId(url) {
  var match = url.match(/[-\w]{25,}/);
  return match ? match[0] : null;
}

/**
 * نصب Trigger برای اجرای خودکار
 */
function setupTrigger() {
  // حذف triggerهای قبلی
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    ScriptApp.deleteTrigger(trigger);
  });
  
  // ایجاد trigger جدید
  ScriptApp.newTrigger('onFormSubmit')
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onFormSubmit()
    .create();
  
  Logger.log('Trigger نصب شد!');
}
```

#### گام 4: تنظیم شماره ستون‌ها

**مهم**: باید شماره ستون‌های فایل را پیدا کنید:

1. به Google Sheet بروید
2. ستون‌هایی که فایل دارند را پیدا کنید
3. شماره ستون را بشمارید (A=1, B=2, C=3, ...)

**مثال**:
```
A = Timestamp (1)
B = Email (2)
C = الاسم الثلاثي (3)
...
Q = صورة جواز السفر (17)
R = صورة الشخص (18)
S = كشف درجات البكالوريوس (19)
T = كشف درجات الماجستير (20)
U = وثيقة الماجستير (21)
```

در کد، خط زیر را تغییر دهید:
```javascript
var fileColumns = [17, 18, 19, 20, 21]; // شماره ستون‌های فایل
```

#### گام 5: ذخیره و اجرای اسکریپت

1. روی **💾 Save** کلیک کنید
2. نام پروژه: `File Link Converter`
3. روی **▶ Run** کلیک کنید
4. تابع را انتخاب کنید: `setupTrigger`
5. روی **Run** کلیک کنید

#### گام 6: دادن مجوزها

اولین بار که اسکریپت را اجرا می‌کنید:
1. پیام "Authorization required" نمایش داده می‌شود
2. روی **Review permissions** کلیک کنید
3. حساب Google خود را انتخاب کنید
4. روی **Advanced** کلیک کنید
5. روی **Go to [Project Name] (unsafe)** کلیک کنید
6. روی **Allow** کلیک کنید

#### گام 7: تست کردن

1. یک فرم تست ارسال کنید (با آپلود فایل)
2. به Google Sheet بروید
3. در ستون‌های فایل، باید "مشاهده فایل" نمایش داده شود
4. کلیک روی آن فایل را در Drive باز می‌کند

---

## نسخه پیشرفته: نمایش نام فایل به جای "مشاهده فایل"

اگر می‌خواهید نام واقعی فایل نمایش داده شود:

```javascript
function onFormSubmit(e) {
  var sheet = e.range.getSheet();
  var row = e.range.getRow();
  
  var fileColumns = [17, 18, 19, 20, 21];
  
  fileColumns.forEach(function(col) {
    var cell = sheet.getRange(row, col);
    var value = cell.getValue();
    
    if (value && value.toString().indexOf('drive.google.com') > -1) {
      var fileId = extractFileId(value);
      
      if (fileId) {
        try {
          // دریافت اطلاعات فایل
          var file = DriveApp.getFileById(fileId);
          var fileName = file.getName();
          var viewLink = 'https://drive.google.com/file/d/' + fileId + '/view';
          
          // نمایش نام فایل به عنوان لینک
          var formula = '=HYPERLINK("' + viewLink + '", "' + fileName + '")';
          cell.setFormula(formula);
        } catch (error) {
          Logger.log('خطا در دریافت فایل: ' + error);
        }
      }
    }
  });
}

function extractFileId(url) {
  var match = url.match(/[-\w]{25,}/);
  return match ? match[0] : null;
}

function setupTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    ScriptApp.deleteTrigger(trigger);
  });
  
  ScriptApp.newTrigger('onFormSubmit')
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onFormSubmit()
    .create();
  
  Logger.log('Trigger نصب شد!');
}
```

---

## مرحله 7: تنظیمات نهایی

### 7.1 تنظیمات فرم

1. روی آیکون **⚙ Settings** کلیک کنید

#### تب General:
- ✓ **Collect email addresses**
- ✓ **Limit to 1 response** (هر نفر فقط یک بار می‌تواند فرم را پر کند)
- ✓ **Respondents can edit after submit**: OFF
- **Response receipts**: Always (ایمیل تأیید برای کاربر ارسال می‌شود)

#### تب Presentation:
- ✓ **Show progress bar** (نمایش پیشرفت فرم)
- ✓ **Shuffle question order**: OFF
- **Confirmation message**: 
  ```
  تم إرسال طلبك بنجاح! ✓
  
  سيتم مراجعة طلبك والتواصل معك قريباً
  شكراً لك
  ```

#### تب Quizzes:
- **Make this a quiz**: OFF (این یک کوییز نیست)

### 7.2 تنظیم Notifications

برای دریافت ایمیل هر بار که فرم پر می‌شود:

1. در Google Sheet، روی **Tools** کلیک کنید
2. **Notification rules** را انتخاب کنید
3. تنظیمات:
   - **Notify me when**: A user submits a form
   - **Notify me with**: Email - daily digest یا Email - right away
4. روی **Save** کلیک کنید

### 7.3 اشتراک‌گذاری فرم

#### روش 1: لینک مستقیم
1. روی **Send** کلیک کنید
2. آیکون **🔗 Link** را انتخاب کنید
3. ✓ **Shorten URL** (لینک کوتاه‌تر)
4. روی **Copy** کلیک کنید
5. این لینک را با دانشجویان به اشتراک بگذارید

#### روش 2: Embed در وب‌سایت
1. روی **Send** کلیک کنید
2. آیکون **<> Embed** را انتخاب کنید
3. کد HTML را کپی کنید
4. در وب‌سایت خود paste کنید

#### روش 3: ایمیل
1. روی **Send** کلیک کنید
2. آیکون **✉ Email** را انتخاب کنید
3. ایمیل‌های دانشجویان را وارد کنید
4. پیام را بنویسید
5. روی **Send** کلیک کنید

---

## نکات مهم و رفع مشکلات

### ❗ مشکلات رایج و راه‌حل‌ها

#### 1. File Upload کار نمی‌کند
**علت**: نیاز به Google Workspace یا فضای کافی Drive
**راه‌حل**: 
- از حساب Google Workspace استفاده کنید، یا
- فضای Drive را افزایش دهید (Google One)

#### 2. لینک‌های فایل به درستی تبدیل نمی‌شوند
**علت**: شماره ستون‌ها اشتباه است
**راه‌حل**:
- شماره ستون‌های فایل را دوباره بررسی کنید
- در کد Apps Script، آرایه `fileColumns` را تصحیح کنید

#### 3. Trigger اجرا نمی‌شود
**علت**: مجوزها داده نشده یا Trigger نصب نشده
**راه‌حل**:
- تابع `setupTrigger()` را دوباره اجرا کنید
- مجوزهای لازم را بدهید
- در **Apps Script > Triggers** بررسی کنید که Trigger وجود دارد

#### 4. Logic شرطی کار نمی‌کند
**علت**: Sections به درستی تنظیم نشده‌اند
**راه‌حل**:
- ساختار Sections را طبق راهنما بسازید
- "Go to section based on answer" را دوباره تنظیم کنید

#### 5. فرم به زبان عربی نمایش داده نمی‌شود
**علت**: Google Forms به طور خودکار زبان را تشخیص می‌دهد
**راه‌حل**:
- متن‌ها را به عربی بنویسید
- مرورگر را به عربی تغییر دهید
- از VPN استفاده کنید (اگر در کشوری هستید که عربی پشتیبانی نمی‌شود)

---

## بهینه‌سازی و نکات پیشرفته

### 1. اضافه کردن شماره ردیف خودکار

در Google Sheet، ستون اول را برای شماره ردیف اختصاص دهید:

```javascript
function onFormSubmit(e) {
  var sheet = e.range.getSheet();
  var row = e.range.getRow();
  
  // اضافه کردن شماره ردیف
  sheet.getRange(row, 1).setValue(row - 1); // ردیف 1 = Header
  
  // بقیه کد برای تبدیل لینک‌ها...
}
```

### 2. ارسال ایمیل تأیید سفارشی

```javascript
function onFormSubmit(e) {
  var sheet = e.range.getSheet();
  var row = e.range.getRow();
  
  // دریافت ایمیل کاربر (فرض: ستون 2)
  var email = sheet.getRange(row, 2).getValue();
  
  // ارسال ایمیل
  MailApp.sendEmail({
    to: email,
    subject: 'تأیید ثبت‌نام - الدراسات العليا',
    body: 'تم إرسال طلبك بنجاح!\n\nسيتم مراجعة طلبك والتواصل معك قريباً.\n\nشكراً لك'
  });
}
```

### 3. رنگ‌بندی خودکار ردیف‌ها

```javascript
function onFormSubmit(e) {
  var sheet = e.range.getSheet();
  var row = e.range.getRow();
  
  // رنگ‌بندی ردیف‌های زوج و فرد
  if (row % 2 === 0) {
    sheet.getRange(row, 1, 1, sheet.getLastColumn()).setBackground('#f0f0f0');
  }
}
```
