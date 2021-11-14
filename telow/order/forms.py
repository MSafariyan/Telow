from django import forms
from django.contrib.auth import get_user_model
from main_app.models.process_model import process
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class OrderForm(forms.Form):
    LASTMAN_STANDING = "DO OR DIE"
    CRITICAL_PRIORITY = "Critical"
    HIGH_PRIORITY = "High"
    MIDDLE_PRIORITY = "Middle"
    LOW_PRIORITY = "Low"

    INDEED_PRIORITY = [
        (LASTMAN_STANDING, 'Do or die'),
        (CRITICAL_PRIORITY, 'Critical priority'),
        (HIGH_PRIORITY, 'High priority'),
        (MIDDLE_PRIORITY, 'Middle priority'),
        (LOW_PRIORITY, 'Low priority'),
        
    ]
    
    title = forms.CharField(
        label="عنوان سفارش", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    priority = forms.ChoiceField(
        label="اولویت",
        choices=INDEED_PRIORITY,
        widget=forms.Select(attrs={'class':'js-example-basic-single form-control'})
    )
    
    flow = forms.ModelChoiceField(
        required=True,
        queryset=process.objects.filter(isEnable=True).all(),
        label="روند",
        widget=forms.Select(attrs={"class": "js-example-basic-single form-control"}),
    )

    delivery_date = JalaliDateField(# date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget # optional, to use default datepicker
        )

    assignE = forms.ModelChoiceField(
        required=False,
        queryset=get_user_model().objects.filter(is_staff=True).all(),
        label="مشتری",
        widget=forms.Select(attrs={"class": "js-example-basic-single form-control"}),
    )

    order_number = forms.CharField(
        label="شماره سفارش", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    # payment_type = forms.CharField(
    #     label="شیوه تسویه",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "شیوه تسویه"}
    #     ),
    # )

    # outsource_choices = [("True", "دارد"), ("False", "ندارد")]

    # outsource = forms.ChoiceField(
    #     choices=outsource_choices,
    #     label="برون سپاری",
    #     widget=forms.RadioSelect(attrs={"class": "", "style": "display: inline-block"}),
    # )

    # outsource_action = forms.CharField(
    #     label="مرحله عملیاتی:",
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "نام مرحله عملیاتی","required":'false'}
    #     ),
    # )

    # final_circulation = forms.CharField(
    #     label="تیراژ نهایی",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "تیراژ نهایی"}
    #     ),
    # )

    # circulation_type_choices = [("number", "عدد"), ("copy", "جلد"), ("sheet", "شیت")]

    # final_circulation_type = forms.ChoiceField(
    #     choices=circulation_type_choices,
    #     label="",
    #     widget=forms.RadioSelect(),
    # )

    # layers = forms.CharField(
    #     label="تعداد لایه",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "تعداد لایه‌ها"}
    #     ),
    # )
    # layer_circulation = forms.CharField(
    #     label="تیراژ لایه‌ها",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "تیراژ لایه‌ها"}
    #     ),
    # )

    # paper_supplier_choices = [("we", "شرکت"), ("them", "مشتری")]

    # paper_supplier = forms.ChoiceField(
    #     choices=paper_supplier_choices,
    #     label="تامین کننده کاغذ",
    #     widget=forms.RadioSelect(),
    # )

    # paper_type = forms.CharField(
    #     label="نوع کاغذ",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "نوع کاغذ/مقوا"}
    #     ),
    # )

    # paper_weigth = forms.CharField(
    #     label="گرماژ",
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "گرماژ"}),
    # )

    # paper_brand = forms.CharField(
    #     label="برند کاغذ", widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # unknowOption_choices = [("0", "SG"), ("1", "LG")]
    # unknowOption = forms.ChoiceField(
    #     choices=unknowOption_choices, label="", widget=forms.RadioSelect(attrs={})
    # )

    # paper_legit_size = forms.CharField(
    #     label="ابعاد اصلی کاغذ(سانتی متر)",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "dir": "ltr", "placeholder": "20*30"}
    #     ),
    # )
    # paper_work_size = forms.CharField(
    #     label="ابعاد کار کاغذ(سانتی متر)",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "20*30", "dir": "ltr"}
    #     ),
    # )

    # paper_amount = forms.CharField(
    #     label="تعداد کل کاغذ‌ها",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "کل کاغذها"}
    #     ),
    # )

    # paper_waste_amount = forms.CharField(
    #     label="تعداد کاغذ‌های باطله",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "کاغذ باطله"}
    #     ),
    # )

    # paper_used_amount = forms.CharField(
    #     label="تعداد کاغذ مفید",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "کاغذهای مفید"}
    #     ),
    # )

    # papaer_self_provide = forms.CharField(
    #     label="تعداد کاغذ تامین شده توسط شرکت",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "توسط شرکت"}
    #     ),
    # )

    # paper_customer_provide = forms.CharField(
    #     label="تعداد کاغذ تامین شده توسط مشتری",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "توسط مشتری"}
    #     ),
    # )

    # print_plate_provider_choices = [("0", "شرکت"), ("1", "مشتری"), ("2", "آرشیو")]
    # print_plate_provider = forms.ChoiceField(
    #     choices=print_plate_provider_choices,
    #     label="تامین کننده زینک",
    #     widget=forms.RadioSelect(),
    # )

    # print_plate_amount = forms.CharField(
    #     label="تعداد زینک",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "تعداد زینک"}
    #     ),
    # )

    # print_plate_burn = forms.BooleanField(
    #     label="زینک سوزی",
    #     initial=False,
    # )

    ordering_on_print_plate = forms.CharField(
        label="تعداد چیدمان در هر زینک",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "تعداد چیدمان در هر زینک"}
        ),
    )

    print_plate_file = forms.FileField(
        label="آدرس فایل زینک", widget=forms.FileInput(attrs={"class": "form-control"})
    )

    # paper_size_before_cut = forms.CharField(
    #     label="ابعاد اولیه کاغذ (سانتی متر)",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "21*20", "dir": "ltr"}
    #     ),
    # )

    # paper_amount_recived = forms.CharField(
    #     label="تعداد کاغذهای دریافتی از انبار",
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )

    # paper_work_size_after_cut = forms.CharField(
    #     label="ابعاد پس از برش کاغذ (سانتی متر)",
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "20*20", "dir": "ltr"}
    #     ),
    # )

    # paper_amount_after_cut = forms.CharField(
    #     label="تعداد کاغذها بعد از برش",
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )

    # return_wasted_paper = forms.BooleanField(
    #     label="کناره گیری کاغذ تحویل مشتری گردد",
    #     initial=False,
    # )

    # lito_discription = forms.CharField(
    #     label="توضیحات",
    #     widget=forms.Textarea(
    #         attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "2"}
    #     ),
    # )

    # outsource_choices = [("1", "دارد"), ("0", "ندارد")]

    # superviser = forms.ChoiceField(
    #     choices=outsource_choices, label="ناظر", widget=forms.RadioSelect()
    # )

    # sample_view = forms.ChoiceField(
    #     choices=outsource_choices, label="نمونه شاهد", widget=forms.RadioSelect()
    # )

    # qc = forms.BooleanField(
    #     label="تصدیق چاپ توس QC",
    #     initial=False,
    # )

    # color_pallet_range = forms.CharField(
    #     label="تعداد رنگ", widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # color_pallet_choices = [
    #     ("Cyan", "C"),
    #     ("Magenta", "M"),
    #     ("Yellow", "Y"),
    #     ("Black", "K"),
    # ]

    # color_pallet = forms.MultipleChoiceField(
    #     label="تعداد رنگ",
    #     choices=color_pallet_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    # )

    # spot_colors = forms.CharField(
    #     label="رنگ‌های Spot:", widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # pantone_colors = forms.CharField(
    #     label="رنگ‌های Pantone:",
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )

    # parallel_cover_choices = [
    #     ("0", "ورونی براق"),
    #     ("1", "ورونی مات"),
    #     ("2", "واتربیس براق"),
    #     ("3", "واتربیس مات"),
    #     ("4", "یووی"),
    #     ("5", "هیبرید"),
    # ]

    # parallel_cover = forms.ChoiceField(
    #     label="پوشش همزمان",
    #     choices=parallel_cover_choices,
    #     widget=forms.RadioSelect(attrs={"class": ""}),
    # )

    # print_option_choices = [
    #     ("0", "چاپ یک رو"),
    #     ("1", "چاپ دورو"),
    #     ("2", "چاپ دورو سکه‌ای"),
    #     ("3", "چاپ دورو روی خودش"),
    # ]

    # print_option = forms.ChoiceField(
    #     label="چاپ",
    #     choices=print_option_choices,
    #     widget=forms.RadioSelect(attrs={"class": ""}),
    # )

    # print_machines_count = forms.CharField(
    #     label="تعداد دستگاه", widget=forms.TextInput(attrs={"class": "form-control"})
    # )
    # forms_count = forms.CharField(
    #     label="تعداد فرم", widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # # print_graphhical_file = forms.FileField(
    # #     label="پیوست فایل گرافیکی",
    # #     widget=forms.FileInput(attrs={"class": "form-control"}),
    # # )

    # print_discription = forms.CharField(
    #     label="توضیحات",
    #     widget=forms.Textarea(
    #         attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
    #     ),
    # )

    # flat_cover_choices = [
    #     ("shiny veroni", "ورونی براق"),
    #     ("matt veroni", "ورونی مات"),
    #     ("shiny waterbase", "واتربیس براق"),
    #     ("matt waterbase", "واتربیس مات"),
    #     ("UV", "یووی"),
    #     ("UV hybride", "یووی هیبرید"),
    #     ("َUV sandi", "هیبرید شنی"),
    #     ("UV holographic", "یووی هولوگرافیک"),
    #     ("UV cylindrik", "یووی سیلندریک"),
    # ]
    # flat_cover = forms.MultipleChoiceField(
    #     label="پوشش سخت",
    #     choices=flat_cover_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    # )

    # flat_cover_detail_choices = [
    #     ("date and price", "محل درج تاریخ و قیمت"),
    #     ("lab chasb", "لب چسب"),
    # ]

    # flat_cover_detail = forms.MultipleChoiceField(
    #     label="پوشش سخت",
    #     choices=flat_cover_detail_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    # )

    # # flat_cover_file = forms.FileField(
    # #     label="پیوست فایل پوشش", widget=forms.FileInput(attrs={"class": "form-control"})
    # # )

    # plastic_covers_choices = [
    #     ("0", "سلفون حرارتی"),
    #     ("1", "سلفون چسبی"),
    #     ("2", "سلفون براق"),
    #     ("3", "سلفون مات"),
    #     ("4", "سلون مخملی"),
    #     ("5", "یکرو سلفون"),
    #     ("6", "دو رو سلفون"),
    #     ("7", "نور خالی کردن سلون دارد"),
    # ]

    # plastic_covers = forms.MultipleChoiceField(
    #     label="",
    #     choices=plastic_covers_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    # )

    # plastic_discription = forms.CharField(
    #     label="توضیحات",
    #     widget=forms.Textarea(
    #         attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
    #     ),
    # )

    # part_cover_choices = [
    #     ("UV part cover", "پوشش موضعی یووی"),
    #     ("UV sandi part cover", "پوشش موضعی یووی شنی"),
    # ]

    # part_cover = forms.MultipleChoiceField(
    #     label="پوشش موضعی",
    #     choices=part_cover_choices,
    #     widget=forms.CheckboxSelectMultiple(),
    # )

    # part_cover_description = forms.CharField(
    #     label="توضیحات",
    #     widget=forms.Textarea(
    #         attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
    #     ),
    # )

    # # flat_cover_file = forms.FileField(
    # #     label="پیوست فایل پوشش", widget=forms.FileInput(attrs={"class": "form-control"})
    # # )

    # hotstamp_sample = forms.ChoiceField(
    #     choices=outsource_choices, label="نمونه هات اسمپت", widget=forms.RadioSelect()
    # )

    # hotstamp_foil_color = forms.CharField(
    #     label="رنگ فویل", widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # # hotstamp_file = forms.FileField(
    # #     label="پیوست فایل هات استمپ",
    # #     widget=forms.FileInput(attrs={"class": "form-control"}),
    # # )

    # cliche_type_choices = [("babesti", "بابستی"), ("letter presi", "لترپرسی")]
    # cliche_type = forms.ChoiceField(
    #     choices=cliche_type_choices, label="نوع کلیشه", widget=forms.RadioSelect()
    # )

    # cliche_provider_choices = [
    #     ("new cliche hotstamp", "ساخت کلیشه هات استمپ جدید"),
    #     ("by customer", "ارسال کلیشه توسط میشتری"),
    #     ("archive", "استفاده از کلیشه آرشیوی"),
    # ]
    # cliche_provider = forms.ChoiceField(
    #     choices=cliche_provider_choices, label="", widget=forms.RadioSelect()
    # )

    # # hotstamp_description = forms.CharField(
    # #     label="توضیحات", widget=forms.Textarea(attrs={"class": "form-control"})
    # # )

    # sheild_choices = [
    #     ("automatic", "پوشال گیری اتوماتیک"),
    #     ("handy", "پوشال گیری دستی"),
    #     ("do nothing", "با پوشال تحویل مشتری گردد"),
    # ]
    # sheild = forms.ChoiceField(
    #     choices=sheild_choices, label="پوشال", widget=forms.RadioSelect()
    # )

    # window_sticking_choices = [("plastic", "نایلون"), ("glass", "طلق")]
    # window_sticking = forms.ChoiceField(
    #     choices=window_sticking_choices,
    #     label="پنجره چسبانی",
    #     widget=forms.RadioSelect(),
    # )

    # window_width = forms.CharField(
    #     label="عرض نایلون/طلق", widget=forms.TextInput(attrs={"class": "form-control"})
    # )
    # # window_thickness = forms.CharField(
    # #     label="ضخامت نایلون/طلق",
    # #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # # )

    # box_sticking_choices = [
    #     ("regular glue", "چسب معمولی"),
    #     ("plastic glue", "چسب سلفون"),
    #     ("hot glue", "چسب حرارتی"),
    #     ("both side glue", "چسب دو طرفه"),
    #     ("regular edge glue", "لبه چسب معمولی"),
    #     ("bottom luck", "لاک باتم"),
    #     ("4 points", "۴ نقطه"),
    #     ("6 points", "۶ نقطه"),
    #     ("series sticking", "دست چسبانی"),
    #     ("packet sticking", "پاکت چسبانی"),
    #     ("setting in box", "چیدمان داخل جعبه"),
    #     ("setting in basket", "چیدمان داخل سبد"),
    #     (
    #         "setting in plastic and close the top",
    #         "چیدمان داخل نایلون و بستن درب نایلون",
    #     ),
    # ]

    # box_sticking = forms.MultipleChoiceField(
    #     choices=box_sticking_choices,
    #     label="جعبه چسبانی",
    #     widget=forms.CheckboxSelectMultiple(),
    # )

    # bindray_cut = forms.ChoiceField(
    #     choices=outsource_choices, label="برش", widget=forms.RadioSelect()
    # )

    # bindray_size = forms.CharField(
    #     label="ابعاد نهایی برش(سانتی متر)",
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )

    # bindray_detail_choices = [
    #     ("fold", "تاکنی"),
    #     ("order", "ترتیب"),
    #     ("hot glue", "چسب گرم"),
    #     ("staple", "مفتول"),
    #     ("tah dozi", "ته دوزی"),
    #     ("punch and spring", "پانچ و فنر"),
    #     ("glue and sweing", "چسب و دوخت"),
    #     ("loop staple", "مفتول لوپ"),
    #     ("overlab", "اورلب"),
    # ]

    # bindray_detail = forms.MultipleChoiceField(
    #     choices=bindray_detail_choices,
    #     label="صحافی",
    #     widget=forms.CheckboxSelectMultiple(),
    # )

    # bindray_cover_choices = [
    #     ("hard cover", "جلد سخت"),
    #     ("round bottom", "ته گرد"),
    #     ("round edge", "گوشه گرد"),
    #     ("rooban", "روبان"),
    #     ("shirzeh", "شیرازه"),
    #     ("ghondagh", "قنداق"),
    #     ("tanzif", "تنظیف"),
    #     ("plastic cover", "روکش سلفونی"),
    #     ("galingor cover", "روکش گالیگنوری"),
    #     ("leather cover", "روکش چرم"),
    #     ("sticky plastic", "پلاستیک چسبانی"),
    #     ("corol lab", "لب رنگ"),
    #     ("hotstamp cover", "هات استمپ جلد"),
    # ]

    # bindary_cover = forms.MultipleChoiceField(
    #     choices=bindray_cover_choices,
    #     label="جلد صحافی",
    #     widget=forms.CheckboxSelectMultiple,
    # )

    # bindray_cover2_choices = [
    #     ("sar chasb", "سر چسب"),
    #     ("sheets", "اوراق"),
    #     ("chondagh and maftol", "قنداق مفتول"),
    # ]

    # bindary_cover2 = forms.MultipleChoiceField(
    #     choices=bindray_cover2_choices,
    #     label="جلد صحافی",
    #     widget=forms.CheckboxSelectMultiple(),
    # )
    # bindray_serial = forms.BooleanField(
    #     label="سریال",
    #     initial=False,
    # )
    # bindray_serial_number_start = forms.CharField(
    #     label="شروع سریال",
    #     widget=forms.TextInput(
    #         attrs={"class": " form-control", "placeholder": "شروع سریال"}
    #     ),
    # )
    # bindray_serial_number_end = forms.CharField(
    #     label="پایان سریال",
    #     widget=forms.TextInput(
    #         attrs={"class": " form-control", "placeholder": "پایان سریال‌"}
    #     ),
    # )

    # bindary_order = forms.CharField(
    #     label="ترتیب نسخه‌ها", widget=forms.TextInput(attrs={"class": " form-control"})
    # )

    # bindary_description = forms.CharField(
    #     label="توضیحات",
    #     widget=forms.Textarea(
    #         attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"}
    #     ),
    # )

    # customize_choices = [
    #     ("one row customize", "شخصی سازی تک ردیفه"),
    #     ("two row customize", "شخصی سازی دو ردیفه"),
    #     ("barcode", "بارکد"),
    #     ("scrach label", "اسکرچ لبیل"),
    # ]

    # customize = forms.MultipleChoiceField(
    #     choices=customize_choices,
    #     label="شخصی سازی",
    #     widget=forms.CheckboxSelectMultiple()
    # )

    # pin_code = forms.CharField(
    #     label="نحوه تحویل پین/کد/شماره سریال",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )

    # send_type_choices = [
    #     ("kartoni dast chin", "کارتنی دست چین"),
    #     ("kartoni roy pallet", "کارتنی روی پالت"),
    #     ("bedon karton va chideman", "بدون کارتن و چیدمان"),
    # ]

    # send_type = forms.MultipleChoiceField(
    #     choices=send_type_choices,
    #     label="نحوه ارسال به مشتری",
    #     widget=forms.CheckboxSelectMultiple()
    # )

    # # shiring = forms.BooleanField(
    # #     label="شیرینگ",
    # #     initial=False,
    # # )

    # shiring_amount = forms.CharField(
    #     label="شیرینگ در تعداد",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )

    # # lafaf = forms.BooleanField(
    # #     label="لفاف",
    # #     initial=False,
    # # )

    # lafaf_amount = forms.CharField(
    #     label="لفاف در تعداد", widget=forms.TextInput(attrs={"class": " form-control"})
    # )

    # # bandinak = forms.BooleanField(
    # #     label="بندینک",
    # #     initial=False,
    # # )

    # bandinak_amount = forms.CharField(
    #     label="بندینک در تعداد",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )


    # box_amount = forms.CharField(
    #     label="تعداد در کارتن",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )
    
    # basket_amount = forms.CharField(
    #     label="تعداد در سبد",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )
    
    
    # # packing = forms.BooleanField(
    # #     label="کارتن",
    # #     initial=False,
    # # )

    # packing_provider_choices = [("0", "شرکت"), ("1", "مشتری")]

    # packing_provider = forms.ChoiceField(
    #     choices=packing_provider_choices,
    #     label="تامین کننده کارتن",
    #     widget=forms.RadioSelect()
    # )

    # packing_type_choices = [
    #     ("3 layers", "۳ لایه"),
    #     ("5 layers", "۵ لایه"),
    #     ("custome", "سفارشی"),
    # ]

    # packing_type = forms.ChoiceField(
    #     choices=packing_type_choices,
    #     label="کارتن",
    #     widget=forms.RadioSelect()
    # )

    # packing_description = forms.CharField(
    #     label="توضیحات", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    # )

    # basket = forms.BooleanField(
    #     label="سبد",
    #     initial=False,
    # )

    # plastic = forms.BooleanField(
    #     label="نایلون",
    #     initial=False,
    # )

    # basket_provider_choices = [("0", "شرکت"), ("them", "مشتری")]

    # basket_provider = forms.ChoiceField(
    #     choices=basket_provider_choices,
    #     label="تامین کننده سبد",
    #     widget=forms.RadioSelect()
    # )

    # basket_description = forms.CharField(
    #     label="توضیحات", widget=forms.Textarea( attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    # )

    # basket_type_choices = [
    #     ("pallet", "پالت"),
    #     ("sar pallet and tasme-kesh", "استفاده از سر پالت و تسمه کشی"),
    #     ("strach pallet", "استرچ پالت"),
    # ]

    # basket_type = forms.MultipleChoiceField(
    #     choices=basket_type_choices,
    #     label="حمل و نقل",
    #     widget=forms.CheckboxSelectMultiple()
    # )

    # label_type_choise = [
    #     ("label with company name", "لیبل شناسایی عمومی با نام شرکت"),
    #     ("label without company name", "لیبل شناسایی عمومی بدون نام شرکت"),
    #     ("custome label", "لیبل اختصاصی"),
    # ]

    # label_type = forms.ChoiceField(
    #     choices=label_type_choise,
    #     label="لیبل",
    #     widget=forms.RadioSelect()
    # )

    # label_detail = forms.CharField(
    #     label="موارد مندرج در لیبل اختصاصی",
    #     widget=forms.TextInput(attrs={"class": " form-control"}),
    # )

    # other_description = forms.CharField(
    #     label="دیگر توضیحات", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "توضیحات...", "rows": "0"})
    # )
