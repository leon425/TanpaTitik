# Generated by Django 4.0.4 on 2024-03-10 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FAQs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('current', models.BooleanField(default=True)),
                ('cancel', models.BooleanField(default=False)),
                ('payment_method', models.CharField(max_length=200, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('terms', models.BooleanField(default=False)),
                ('shipping_cost', models.IntegerField(default=0)),
                ('delivery_time', models.CharField(max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('product_index', models.IntegerField(default=0)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('color_circle', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('offer', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('overview', models.CharField(blank=True, max_length=200, null=True)),
                ('material', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('size', models.CharField(blank=True, max_length=200, null=True)),
                ('color', models.CharField(blank=True, max_length=200, null=True)),
                ('color_hex', models.CharField(blank=True, max_length=200, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('status', models.CharField(max_length=200)),
                ('ig_link', models.CharField(max_length=200)),
                ('fb_link', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Products_offer',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mainPage.products')),
                ('name', models.CharField(max_length=200)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('final_price', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainPage.customer')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainPage.products')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('district', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('province', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('service', models.CharField(max_length=200, null=True)),
                ('customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Products_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.FloatField(blank=True, null=True)),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('helpful', models.IntegerField(blank=True, null=True)),
                ('unhelpful', models.IntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainPage.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainPage.products')),
            ],
        ),
        migrations.CreateModel(
            name='Products_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainPage.products')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=200, null=True)),
                ('payment_timestamp', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('payment_evidence', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainPage.products')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainPage.orderstatus'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.IntegerField()),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainPage.province')),
            ],
        ),
    ]
