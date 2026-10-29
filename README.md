# AuraPix — Python + Streamlit

واجهة قريبة من الصور المرجعية، باسم AuraPix، مع البحث عن الصور ووصف الصور وعن المشروع، وعربي/إنجليزي وفاتح/داكن. صورة الشبكة جديدة وليست الصورة الأصلية؛ عناصر رفع الملفات والقوائم تستخدم عناصر Streamlit، لذلك ليست نسخة مطابقة بالبكسل.

## التشغيل على Windows من Visual Studio Code
استخدمي Python 3.11 أو 3.12 بنسخة 64-bit. فكّي الضغط وافتحي مجلد AuraPix ثم افتحي Terminal:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

لا يلزم تفعيل البيئة، فتتفادي مشكلة صلاحيات PowerShell. على macOS/Linux استبدلي `.venv\Scripts\python.exe` بـ `.venv/bin/python`.

## أين أعدل؟
- `styles.py`: ألوان LIGHT/DARK وكل تنسيقات الشكل، بما فيها الشريط العلوي وأيقونات قائمته.
- `app.py`: ترتيب الأقسام، أزرار الصفحات ورفع الصور.
- `i18n.py`: النصوص الإنجليزية والعربية.
- `assets/network.jpg`: الصورة التي تظهر أعلى البحث ووصف الصور.
- `models.py`: تحميل CLIP وBLIP واستدعاؤهما.
- `.streamlit/config.toml`: إعدادات Streamlit الأساسية؛ مفتاح الداكن داخل التطبيق يستخدم styles.py.

## النماذج
عند أول بحث أو وصف يلزم إنترنت لتنزيل openai/clip-vit-base-patch32 وSalesforce/blip-image-captioning-base؛ التنزيلات كبيرة وقد تستغرق وقتًا. بعد تخزين النماذج محليًا يمكن استخدامها دون اتصال إذا اكتمل التخزين. CPU مدعوم؛ GPU اختياري. لا تحتاجين API key أو FastAPI.

لتشغيل نماذجك المدربة، حددي قبل التشغيل في PowerShell:

```powershell
$env:CLIP_MODEL="C:\models\my-clip"
$env:BLIP_MODEL="C:\models\my-blip"
.venv\Scripts\python.exe -m streamlit run app.py
```

المجلدات يجب أن تكون بتنسيق Hugging Face وتحتوي ملفات النموذج والمعالج/tokenizer. الافتراضي يكتب وصف الصور بالإنجليزية، حتى مع الواجهة العربية. وصف البحث بالإنجليزية أفضل للنموذج الافتراضي.

درجة النتائج هي cosine similarity وليست نسبة احتمال أو دقة. البيانات Flickr30K غير مرفقة. الصور المرفوعة لا تُرسل لخدمة استدلال خارجية، لكن تنزيل النماذج والخطوط/المكتبات يتطلب اتصالًا حسب البيئة.

## الاختبارات
```powershell
.venv\Scripts\python.exe -m pip install pytest
.venv\Scripts\python.exe -m pytest tests
```

تم فصل تحميل النماذج عن فتح الواجهة، فيمكن معاينة الصفحات بعد تثبيت Streamlit وPillow فقط. الاستدلال يتطلب كل مكتبات requirements.txt.
