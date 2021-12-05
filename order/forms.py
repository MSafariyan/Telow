from django import forms
from django.contrib.auth import get_user_model
from main_app.models.process_model import process
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from main_app.models.customer_model import customer


class OrderForm(forms.Form):
    #  Just a fatty form to take orders.

    INDEED_PRIORITY = [
        ("خیلی بالا", 'خیلی بالا'),
        ("بالا", 'بالا'),
        ("متوسط", 'متوسط'),
    ]
    
    title = forms.CharField(required=True,
        label="عنوان سفارش", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    priority = forms.ChoiceField(required=False,
        label="اولویت",
        choices=INDEED_PRIORITY,
        widget=forms.Select(attrs={'class':'js-example-basic-single'})
    )
    
    flow = forms.ModelChoiceField(required=True,
        queryset=process.objects.filter(isEnable=True).all(),
        label="روند",
        widget=forms.Select(attrs={"class": "js-example-basic-single"}),
    )

    delivery_date = JalaliDateField(# date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget, # optional, to use default datepicker
	        required=True,
        )

    assignE = forms.ModelChoiceField(
        required=True,
        queryset=customer.objects.all(),
        label="مشتری",
        widget=forms.Select(attrs={"class": "js-example-basic-single"}),
    )

    order_number = forms.CharField(required=False,
        label="شماره سفارش", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    payment_choices = [("نقدی","نقدی"), ("15 روزه","15 روزه"), ("30 روزه","30 روزه"), ("45 روزه","45 روزه"), ("90 روزه","90 روزه"), ("چک","چک")]
    payment_type = forms.ChoiceField(required=False,
        label="شیوه تسویه",
        choices=payment_choices,
        widget=forms.Select(attrs={'class':'js-example-basic-single'})

    )

    outsource_choices = [("دارد", "دارد"), ("ندارد", "ندارد")]

    outsource = forms.ChoiceField(required=False,
        choices=outsource_choices,
        label="برون سپاری",
        widget=forms.RadioSelect(attrs={"class": "", "style": "display: inline-block"}),
    )

    outsource_action = forms.CharField(
        label="مرحله عملیاتی:",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام مرحله عملیاتی"}
        ),
    )

    final_circulation = forms.CharField(required=False,
        label="تیراژ نهایی",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تیراژ نهایی"}
        ),
    )

    circulation_type_choices = [("عدد", "عدد"), ("جلد", "جلد"), ("شیت", "شیت")]

    final_circulation_type = forms.ChoiceField(required=False,
        choices=circulation_type_choices,
        label="",
        widget=forms.RadioSelect(),
    )

    layers = forms.CharField(required=False,
        label="تعداد لایه",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تعداد لایه‌ها"}
        ),
    )
    layer_circulation = forms.CharField(required=False,
        label="تیراژ لایه‌ها",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تیراژ لایه‌ها"}
        ),
    )

    paper_supplier_choices = [("شرکت", "شرکت"), ("مشتری", "مشتری")]

    paper_supplier = forms.ChoiceField(required=False,
        choices=paper_supplier_choices,
        label="تامین کننده کاغذ",
        widget=forms.RadioSelect(),
    )

    paper_type = forms.CharField(
        required=False,
        label="نوع کاغذ",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نوع کاغذ/مقوا"}
        ),
    )

    paper_weigth = forms.CharField(
	required=False,
        label="گرماژ",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "گرماژ"}),
    )

    paper_brand = forms.CharField(
	required=False,
        label="برند کاغذ", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    unknowOption_choices = [("SG", "SG"), ("LG", "LG")]
    unknowOption = forms.ChoiceField(
	required=False,
        choices=unknowOption_choices, label="", widget=forms.RadioSelect(attrs={})
    )

    paper_legit_size = forms.CharField(
	required=False,
        label="ابعاد اصلی کاغذ(سانتی متر)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "dir": "ltr", "placeholder": "20*30"}
        ),
    )
    paper_work_size = forms.CharField(
	required=False,
        label="ابعاد کار کاغذ(سانتی متر)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "20*30", "dir": "ltr"}
        ),
    )

    paper_amount = forms.CharField(
	required=False,
        label="تعداد کل کاغذ‌ها",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کل کاغذها"}
        ),
    )

    paper_waste_amount = forms.CharField(
	required=False,
        label="تعداد کاغذ‌های باطله",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کاغذ باطله"}
        ),
    )

    paper_used_amount = forms.CharField(
	required=False,
        label="تعداد کاغذ مفید",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کاغذهای مفید"}
        ),
    )

    papaer_self_provide = forms.CharField(
	required=False,
        label="تعداد کاغذ تامین شده توسط شرکت",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "توسط شرکت"}
        ),
    )

    paper_customer_provide = forms.CharField(
	required=False,
        label="تعداد کاغذ تامین شده توسط مشتری",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "توسط مشتری"}
        ),
    )

    print_plate_provider_choices = [("شرکت", "شرکت"), ("مشتری", "مشتری"), ("آرشیو", "آرشیو")]
    print_plate_provider = forms.ChoiceField(
	required=False,
        choices=print_plate_provider_choices,
        label="تامین کننده زینک",
        widget=forms.RadioSelect(),
    )

    print_plate_amount = forms.CharField(
	required=False,
        label="تعداد زینک",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تعداد زینک"}
        ),
    )

    print_plate_burn = forms.BooleanField(
	required=False,
        label="زینک سوزی",
        initial=False,
    )

    ordering_on_print_plate = forms.CharField(
	required=False,
        label="تعداد چیدمان در هر زینک",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تعداد چیدمان در هر زینک"}
        ),
    )

    print_plate_file = forms.FileField(
	required=False,
        label="آدرس فایل زینک", widget=forms.FileInput(attrs={"class": "form-control"})
    )

    paper_size_before_cut = forms.CharField(
	required=False,
        label="ابعاد اولیه کاغذ (سانتی متر)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "21*20", "dir": "ltr"}
        ),
    )

    paper_amount_recived = forms.CharField(
	required=False,
        label="تعداد کاغذهای دریافتی از انبار",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    paper_work_size_after_cut = forms.CharField(
	required=False,
        label="ابعاد پس از برش کاغذ (سانتی متر)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "20*20", "dir": "ltr"}
        ),
    )

    paper_amount_after_cut = forms.CharField(
	required=False,
        label="تعداد کاغذها بعد از برش",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    return_wasted_paper = forms.BooleanField(
	required=False,
        label="کناره گیری کاغذ تحویل مشتری گردد",
        initial=False,
    )

    lito_discription = forms.CharField(
	required=False,
        label="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "2"}
        ),
    )

    outsource_choices = [("دارد", "دارد"), ("ندارد", "ندارد")]

    superviser = forms.ChoiceField(
	required=False,
        choices=outsource_choices, label="ناظر", widget=forms.RadioSelect()
    )

    sample_view = forms.ChoiceField(
	required=False,
        choices=outsource_choices, label="نمونه شاهد", widget=forms.RadioSelect()
    )

    qc = forms.BooleanField(
	required=False,
        label="تصدیق چاپ توس QC",
        initial=False,
    )

    color_pallet_range = forms.CharField(
	required=False,
        label="تعداد رنگ", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    color_pallet_choices = [
        ("C", "C"),
        ("M", "M"),
        ("Y", "Y"),
        ("K", "K"),
    ]

    color_pallet = forms.MultipleChoiceField(
	required=False,
        label="تعداد رنگ",
        choices=color_pallet_choices,
        widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    )

    spot_colors = forms.CharField(
	required=False,
        label="رنگ‌های Spot:", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    pantone_colors = forms.CharField(
	required=False,
        label="رنگ‌های Pantone:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    parallel_cover_choices = [
        ("ورونی براق", "ورونی براق"),
        ("ورونی مات", "ورونی مات"),
        ("واتربیس براق", "واتربیس براق"),
        ("واتربیس مات", "واتربیس مات"),
        ("یووی", "یووی"),
        ("هیبرید", "هیبرید"),
    ]

    parallel_cover = forms.ChoiceField(
	required=False,
        label="پوشش همزمان",
        choices=parallel_cover_choices,
        widget=forms.RadioSelect(attrs={"class": ""}),
    )

    print_option_choices = [
        ("چاپ یک رو", "چاپ یک رو"),
        ("چاپ دورو", "چاپ دورو"),
        ("چاپ دورو سکه‌ای", "چاپ دورو سکه‌ای"),
        ("چاپ دورو روی خودش", "چاپ دورو روی خودش"),
    ]

    print_option = forms.ChoiceField(
	required=False,
        label="چاپ",
        choices=print_option_choices,
        widget=forms.RadioSelect(attrs={"class": ""}),
    )

    print_machines_count = forms.CharField(
	required=False,
        label="تعداد دستگاه", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    forms_count = forms.CharField(
	required=False,
        label="تعداد فرم", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    print_graphhical_file = forms.FileField(
	required=False,
        label="پیوست فایل گرافیکی",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    print_discription = forms.CharField(
	required=False,
        label="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
        ),
    )

    flat_cover_choices = [
        ("ورونی براق", "ورونی براق"),
        ("ورونی مات", "ورونی مات"),
        ("واتربیس براق", "واتربیس براق"),
        ("واتربیس مات", "واتربیس مات"),
        ("یووی", "یووی"),
        ("یووی هیبرید", "یووی هیبرید"),
        ("َهیبرید شنی", "هیبرید شنی"),
        ("یووی هولوگرافیک", "یووی هولوگرافیک"),
        ("یووی سیلندریک", "یووی سیلندریک"),
    ]
    flat_cover = forms.MultipleChoiceField(
	required=False,
        label="پوشش سخت",
        choices=flat_cover_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    flat_cover_detail_choices = [
        ("محل درج تاریخ و قیمت", "محل درج تاریخ و قیمت"),
        ("لب چسب", "لب چسب"),
    ]

    flat_cover_detail = forms.MultipleChoiceField(
	required=False,
        label="پوشش سخت",
        choices=flat_cover_detail_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    flat_cover_file = forms.FileField(
	required=False,
        label="پیوست فایل پوشش", widget=forms.FileInput(attrs={"class": "form-control"})
    )

    plastic_covers_choices = [
        ("سلفون حرارتی", "سلفون حرارتی"),
        ("سلفون چسبی", "سلفون چسبی"),
        ("سلفون براق", "سلفون براق"),
        ("سلفون مات", "سلفون مات"),
        ("سلون مخملی", "سلون مخملی"),
        ("یکرو سلفون", "یکرو سلفون"),
        ("دو رو سلفون", "دو رو سلفون"),
        ("نور خالی کردن سلون دارد", "نور خالی کردن سلون دارد"),
    ]

    plastic_covers = forms.MultipleChoiceField(
	required=False,
        label="",
        choices=plastic_covers_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    plastic_discription = forms.CharField(
	required=False,
        label="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
        ),
    )

    part_cover_choices = [
        ("پوشش موضعی یووی", "پوشش موضعی یووی"),
        ("پوشش موضعی یووی شنی", "پوشش موضعی یووی شنی"),
    ]

    part_cover = forms.MultipleChoiceField(
	required=False,
        label="پوشش موضعی",
        choices=part_cover_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    part_cover_description = forms.CharField(
	required=False,
        label="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
        ),
    )

    flat_cover_file = forms.FileField(
	required=False,
        label="پیوست فایل پوشش", widget=forms.FileInput(attrs={"class": "form-control"})
    )

    part_cover_file = forms.FileField(
	required=False,
        label="پیوست فایل پوشش سخت", widget=forms.FileInput(attrs={"class": "form-control"})
    )
    
    hotstamp_sample = forms.ChoiceField(
	required=False,
        choices=outsource_choices, label="نمونه هات اسمپت", widget=forms.RadioSelect()
    )

    hotstamp_foil_color = forms.CharField(
	required=False,
        label="رنگ فویل", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    hotstamp_file = forms.FileField(
	required=False,
        label="پیوست فایل هات استمپ",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    cliche_type_choices = [("babesti", "بابستی"), ("letter presi", "لترپرسی")]
    cliche_type = forms.ChoiceField(
	required=False,
        choices=cliche_type_choices, label="نوع کلیشه", widget=forms.RadioSelect()
    )

    cliche_provider_choices = [
        ("ساخت کلیشه هات استمپ جدید", "ساخت کلیشه هات استمپ جدید"),
        ("ارسال کلیشه توسط مشتری", "ارسال کلیشه توسط مشتری"),
        ("استفاده از کلیشه آرشیوی", "استفاده از کلیشه آرشیوی"),
    ]
    cliche_provider = forms.ChoiceField(
	required=False,
        choices=cliche_provider_choices, label="", widget=forms.RadioSelect()
    )

    hotstamp_description = forms.CharField(
	required=False,
        label="توضیحات", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    sheild_choices = [
        ("پوشال گیری اتوماتیک", "پوشال گیری اتوماتیک"),
        ("پوشال گیری دستی", "پوشال گیری دستی"),
        ("با پوشال تحویل مشتری گردد", "با پوشال تحویل مشتری گردد"),
    ]
    sheild = forms.ChoiceField(
	required=False,
        choices=sheild_choices, label="پوشال", widget=forms.RadioSelect()
    )

    window_sticking_choices = [("نایلون", "نایلون"), ("طلق", "طلق")]
    window_sticking = forms.ChoiceField(
	required=False,
        choices=window_sticking_choices,
        label="پنجره چسبانی",
        widget=forms.RadioSelect(),
    )

    window_width = forms.CharField(
	required=False,
        label="عرض نایلون/طلق", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    window_thickness = forms.CharField(
	required=False,
        label="ضخامت نایلون/طلق",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    box_sticking_choices = [
        ("چسب معمولی", "چسب معمولی"),
        ("چسب سلفون", "چسب سلفون"),
        ("چسب حرارتی", "چسب حرارتی"),
        ("چسب دو طرفه", "چسب دو طرفه"),
        ("لبه چسب معمولی", "لبه چسب معمولی"),
        ("لاک باتم", "لاک باتم"),
        ("۴ نقطه", "۴ نقطه"),
        ("۶ نقطه", "۶ نقطه"),
        ("دست چسبانی", "دست چسبانی"),
        ("پاکت چسبانی", "پاکت چسبانی"),
        ("چیدمان داخل جعبه", "چیدمان داخل جعبه"),
        ("چیدمان داخل جعبه", "چیدمان داخل سبد"),
        (
            "چیدمان داخل نایلون و بستن درب نایلون",
            "چیدمان داخل نایلون و بستن درب نایلون",
        ),
    ]

    box_sticking = forms.MultipleChoiceField(
	required=False,
        choices=box_sticking_choices,
        label="جعبه چسبانی",
        widget=forms.CheckboxSelectMultiple(),
    )

    bindray_cut = forms.ChoiceField(
	required=False,
        choices=outsource_choices, label="برش", widget=forms.RadioSelect()
    )

    bindray_size = forms.CharField(
	required=False,
        label="ابعاد نهایی برش(سانتی متر)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    bindray_detail_choices = [
        ("تاکنی", "تاکنی"),
        ("ترتیب", "ترتیب"),
        ("چسب گرم", "چسب گرم"),
        ("مفتول", "مفتول"),
        ("ته دوزی", "ته دوزی"),
        ("پانچ و فنر", "پانچ و فنر"),
        ("چسب و دوخت", "چسب و دوخت"),
        ("مفتول لوپ", "مفتول لوپ"),
        ("اورلب", "اورلب"),
    ]

    bindray_detail = forms.MultipleChoiceField(
	required=False,
        choices=bindray_detail_choices,
        label="صحافی",
        widget=forms.CheckboxSelectMultiple(),
    )

    bindray_cover_choices = [
        ("جلد سخت", "جلد سخت"),
        ("ته گرد", "ته گرد"),
        ("گوشه گرد", "گوشه گرد"),
        ("روبان", "روبان"),
        ("شیرازه", "شیرازه"),
        ("قنداق", "قنداق"),
        ("تنظیف", "تنظیف"),
        ("روکش سلفونی", "روکش سلفونی"),
        ("روکش گالیگنوری", "روکش گالیگنوری"),
        ("روکش چرم", "روکش چرم"),
        ("پلاستیک چسبانی", "پلاستیک چسبانی"),
        ("لب رنگ", "لب رنگ"),
        ("هات استمپ جلد", "هات استمپ جلد"),
    ]

    bindary_cover = forms.MultipleChoiceField(
	required=False,
        choices=bindray_cover_choices,
        label="جلد صحافی",
        widget=forms.CheckboxSelectMultiple,
    )

    bindray_cover2_choices = [
        ("سر چسب", "سر چسب"),
        ("اوراق", "اوراق"),
        ("قنداق مفتول", "قنداق مفتول"),
    ]

    bindary_cover2 = forms.MultipleChoiceField(
	required=False,
        choices=bindray_cover2_choices,
        label="جلد صحافی",
        widget=forms.CheckboxSelectMultiple(),
    )
    bindray_serial = forms.BooleanField(
	required=False,
        label="سریال",
        initial=False,
    )
    bindray_serial_number_start = forms.CharField(
	required=False,
        label="شروع سریال",
        widget=forms.TextInput(
            attrs={"class": " form-control", "placeholder": "شروع سریال"}
        ),
    )
    bindray_serial_number_end = forms.CharField(
	required=False,
        label="پایان سریال",
        widget=forms.TextInput(
            attrs={"class": " form-control", "placeholder": "پایان سریال‌"}
        ),
    )

    bindary_order = forms.CharField(
	required=False,
        label="ترتیب نسخه‌ها", widget=forms.TextInput(attrs={"class": " form-control"})
    )

    bindary_description = forms.CharField(
	required=False,
        label="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
        ),
    )

    customize_choices = [
        ("شخصی سازی تک ردیفه", "شخصی سازی تک ردیفه"),
        ("شخصی سازی دو ردیفه", "شخصی سازی دو ردیفه"),
        ("بارکد", "بارکد"),
        ("اسکرچ لبیل", "اسکرچ لبیل"),
    ]

    customize = forms.MultipleChoiceField(
	required=False,
        choices=customize_choices,
        label="شخصی سازی",
        widget=forms.CheckboxSelectMultiple()
    )

    pin_code = forms.CharField(
	required=False,
        label="نحوه تحویل پین/کد/شماره سریال",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )

    send_type_choices = [
        ("کارتنی دست چین", "کارتنی دست چین"),
        ("کارتنی روی پالت", "کارتنی روی پالت"),
        ("بدون کارتن و چیدمان", "بدون کارتن و چیدمان"),
    ]

    send_type = forms.MultipleChoiceField(
	required=False,
        choices=send_type_choices,
        label="نحوه ارسال به مشتری",
        widget=forms.CheckboxSelectMultiple()
    )

    shiring_amount = forms.CharField(
	required=False,
        label="شیرینگ در تعداد",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )

    lafaf_amount = forms.CharField(
	required=False,
        label="لفاف در تعداد", widget=forms.TextInput(attrs={"class": " form-control"})
    )

    bandinak_amount = forms.CharField(
	required=False,
        label="بندینک در تعداد",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )


    box_amount = forms.CharField(
	required=False,
        label="تعداد در کارتن",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )
    
    basket_amount = forms.CharField(
	required=False,
        label="تعداد در سبد",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )
    
    packing_provider_choices = [("شرکت", "شرکت"), ("مشتری", "مشتری")]

    packing_provider = forms.ChoiceField(
	required=False,
        choices=packing_provider_choices,
        label="تامین کننده کارتن",
        widget=forms.RadioSelect()
    )

    packing_type_choices = [
        ("۳ لایه", "۳ لایه"),
        ("۵ لایه", "۵ لایه"),
        ("سفارشی", "سفارشی"),
    ]

    packing_type = forms.ChoiceField(
	required=False,
        choices=packing_type_choices,
        label="کارتن",
        widget=forms.RadioSelect()
    )

    packing_description = forms.CharField(
	required=False,
        label="توضیحات", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    )

    basket = forms.BooleanField(
	required=False,
        label="سبد",
        initial=False,
    )

    plastic = forms.BooleanField(
	required=False,
        label="نایلون",
        initial=False,
    )

    basket_provider_choices = [("شرکت", "شرکت"), ("مشتری", "مشتری")]

    basket_provider = forms.ChoiceField(
	required=False,
        choices=basket_provider_choices,
        label="تامین کننده سبد",
        widget=forms.RadioSelect()
    )

    basket_description = forms.CharField(
	required=False,
        label="توضیحات", widget=forms.Textarea( attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    )

    basket_type_choices = [
        ("پالت", "پالت"),
        ("استفاده از سر پالت و تسمه کشی", "استفاده از سر پالت و تسمه کشی"),
        ("استرچ پالت", "استرچ پالت"),
    ]

    basket_type = forms.MultipleChoiceField(
	required=False,
        choices=basket_type_choices,
        label="حمل و نقل",
        widget=forms.CheckboxSelectMultiple()
    )

    label_type_choise = [
        ("لیبل شناسایی عمومی با نام شرکت", "لیبل شناسایی عمومی با نام شرکت"),
        ("لیبل شناسایی عمومی بدون نام شرکت", "لیبل شناسایی عمومی بدون نام شرکت"),
        ("لیبل اختصاصی", "لیبل اختصاصی"),
    ]

    label_type = forms.ChoiceField(
	required=False,
        choices=label_type_choise,
        label="لیبل",
        widget=forms.RadioSelect()
    )

    label_detail = forms.CharField(
	required=False,
        label="موارد مندرج در لیبل اختصاصی",
        widget=forms.TextInput(attrs={"class": " form-control"}),
    )

    other_description = forms.CharField(
	required=False,
        label="دیگر توضیحات", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    )
