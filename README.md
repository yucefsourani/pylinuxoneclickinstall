# pylinuxoneclickinstall

مشروع للتسلية لكنه يعمل بشكل جيد .

عمله ببساطة تشغيل مجموعة من الأوامر مثل أوامر التثبيت بضغطت زر واحدة تحتاج أولا تثبيت سكربت الوسيط على الجهاز وأيضا تثبيت ملف إعدادات يعرف النظام أن scheme معينة يبدأ فيها رابط ما سيتم تمرير لسكربت pylinuxoneclickinstall.py .

التغذية بالمعلومات تتم من خلال الإضافات ويتم التعريف عنها لتظهر في صفحة الويب في مجلد data و ملف أوامر التنفيذ والتراجع عنها في مجلد apps وهم عبارة عن ملفين json ,أما صورة الأيقونة توضع في مجلد icons.

(الملف في مجلد apps ممكن أن يكون ملف بايثون py بشروط معينة لكن لم أنتهي من تجربته بعد ولا يوجد مثال له حاليا في المستودع)

ممكن تحديد معمارية الجهاز  وعلي أي توزيعة أو واجهة يجب أن تعمل الإضافة من خلال تحديد الأمر في ملف json الذي يوضع في مجلد apps وسيقوم السكربت قبل تشغيل الإضافة بقراءة ملف etc/os-release/ للتعرف على إسم التوزيعة أولا يبحث عن سطر يبدأ ب ID_LIKE إذا لم يجده ينقل إلى الذي يبدأ بكلمة ID لهذا مثلا التوزيعات المبنية على فيدورا ولديها سطر ID_LIKE تحتوي كلمة fedora سيتعرف عليها على انها فيدورا اما الواجهة والمعمارية سيقرأ المعلومات من الجهاز مثل متغير البيئة XDG_CURRENT_DESKTOP للتعرف على إسم الواجهة و...

أما __distro__ في الملفات في data هي فقط لتعرض في صفحة الويب بلون برتقالي حتى يتم تميزهم حتى قبل الضغط  لأن في هذا الوقت لا يمكن التعرف على معلومات النظام الذي يعمل .


صفحة الويب تم إنشائها من خلال gemini مع الكثير من التعديلات اليدوية وهي صفحة ويب ثايتة static تعتمد على html و js و css وتجمع المعلومات من خلال ملف apps.json عن طريق سكربت js يعمل من متصفح المستخدم ,وملف apss.json يتم توليده من خلال github action  لعمل flatten لكل ملفات ال json في مجلد data ودمجهم في ملف واحد هذه ال action تعمل بشكل تلقائي عند أي تغير لأي ملف في مجلد data .


أغلب إن لم نقل كل ماكتبته انا موجه لفيدورا لينكس 42 لأني أستخدمها وليس لدي وقت للتجربة على توزيعات أخرى.


# Apps Store

https://yucefsourani.github.io/pylinuxoneclickinstall/




# to install (Beta)

cd ~/ && git clone https://github.com/yucefsourani/pylinuxoneclickinstall

cd ~/pylinuxoneclickinstall

sudo cp pylinuxoneclickinstall.py /usr/bin

sudo chmod 755 /usr/bin/pylinuxoneclickinstall.py

sudo cp pylinuxoneclickinstallurl.desktop /usr/share/applications/

sudo update-desktop-database

# Requires 

 * xterm
 
 * python3

 * xdg-utils



