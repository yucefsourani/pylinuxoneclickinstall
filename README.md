# pylinuxoneclickinstall

مشروع للتسلية لكنه يعمل بشكل جيد .

عمله ببساطة تشغيل مجموعة من الأوامر مثل أوامر التثبيت بضغطت زر واحدة تحتاج أولا تثبيت سكربت الوسيط على الجهاز وأيضا تثبيت ملف إعدادات يعرف النظام أن scheme معينة يبدأ فيها رابط ما سيتم تمرير لسكربت pylinuxoneclickinstall.py .

التغذية بالمعلومات تتم من خلال الإضافات ويتم التعريف عنها لتظهر في صفحة الويب في مجلد data و ملف أوامر التنفيذ والتراجع عنها في مجلد apps وهم عبارة عن ملفين json ,أما صورة الأيقونة توضع في مجلد icons.

(الملف في مجلد apps ممكن أن يكون ملف بايثون py بشروط معينة لكن لم أنتهي من تجربته بعد ولا يوجد مثال له حاليا في المستودع)

ممكن تحديد معمارية الجهاز  وعلي أي توزيعة أو واجهة يجب أن تعمل الإضافة من خلال تحديد الأمر في ملف json الذي يوضع في مجلد apps وسيقوم السكربت قبل تشغيل الإضافة بقراءة ملف etc/os-release/ للتعرف على إسم التوزيعة أولا يبحث عن سطر يبدأ ب ID_LIKE إذا لم يجده ينقل إلى الذي يبدأ بكلمة ID لهذا مثلا التوزيعات المبنية على فيدورا ولديها سطر ID_LIKE تحتوي كلمة fedora سيتعرف عليها على انها فيدورا كذلك الأمر بالنسبة لرقم إصدار التوزيعة اما الواجهة والمعمارية سيقرأ المعلومات من الجهاز مثل متغير البيئة XDG_CURRENT_DESKTOP للتعرف على إسم الواجهة و...

أما \_\_distro\_\_ في الملفات في data هي فقط لتعرض في صفحة الويب بلون برتقالي حتى يتم تميزهم حتى قبل الضغط  لأن في هذا الوقت لا يمكن التعرف على معلومات النظام الذي يعمل .


صفحة الويب تم إنشائها من خلال gemini مع الكثير من التعديلات اليدوية وهي صفحة ويب ثايتة static تعتمد على html و js و css وتجمع المعلومات من خلال ملف apps.json عن طريق سكربت js يعمل من متصفح المستخدم ,وملف apss.json يتم توليده من خلال github action  لعمل flatten لكل ملفات ال json في مجلد data ودمجهم في ملف واحد هذه ال action تعمل بشكل تلقائي عند أي تغير لأي ملف في مجلد data .


لا يتم بدأ تنفيذ الأوامر قبل عرضها على المستخدم وموافقته عليها بشكل صريح وممكن أيضا الإطلاع على الأوامر من خلال الضغط على Detail في صفحت الويب .


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


# English By DeepL

It's a fun project, but it works well.

It simply runs a set of commands, such as installation commands, with a single click. First, you need to install the intermediary script on the device and also install a settings file that tells the system that a specific scheme starts with a link that will be passed to the pylinuxoneclickinstall.py script.

The information is fed through add-ons and is defined to appear on the web page in the "data" folder and the execution and rollback command files in the "apps" folder, which are two json files. The icon image is placed in the "icons" folder.

(The file in the "apps" folder can be a Python py file under certain conditions, but I have not finished testing it yet and there is currently no example of it in the repository).

You can specify the device architecture and on which distribution or interface the extension should work by specifying the command in the json file placed in the "apps" folder. Before running the extension, the script will read the /etc/os-release file. to identify the name of the distribution. First, it searches for a line that starts with ID_LIKE. If it does not find it, it moves to the one that starts with the word ID. For example, distributions based on Fedora that have a line ID_LIKE containing the word fedora will be recognized as Fedora ,the same applies to the distribution release number. As for the interface and architecture, it will read the information from the device, such as the environment variable XDG_CURRENT_DESKTOP, to identify the name of the interface and...

As for \_\_distro\_\_ in the files in "data", it is only displayed on the web page in orange so that they can be distinguished even before clicking, because at this time it is not possible to recognize the information of the operating system.


The web page was created using Gemini with many manual modifications. It is a static web page based on HTML, JS, and CSS, and it collects information from the apps.json file using a JS script that runs from the user's browser. The apss.json file is generated through GitHub Action to flatten all JSON files in the "data" folder and merge them into a single file. This action runs automatically whenever any file in the "data" folder is changed.


Commands  are not executed before they are presented to the user and explicitly approved by them. Commands can also be viewed by clicking on "Detail" on the web page.


Most, if not all, of what I have written is directed at Fedora Linux 42 because that is what I use and I don't have time to experiment with other distributions.


# Apps Store

https://yucefsourani.github.io/pylinuxoneclickinstall/

