# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-07 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('url', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasicSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GalleryPhotographies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modularweb.Gallery')),
            ],
            options={
                'ordering': ('gallery',),
            },
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Photography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=150)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BasePage')),
                ('content', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
            ],
            bases=('modularweb.basepage',),
        ),
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BasePage')),
                ('body', models.TextField(blank=True)),
            ],
            bases=('modularweb.basepage',),
        ),
        migrations.CreateModel(
            name='GalleryPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BasePage')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modularweb.Gallery')),
            ],
            bases=('modularweb.basepage',),
        ),
        migrations.CreateModel(
            name='IconField',
            fields=[
                ('basefield_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BaseField')),
                ('faIcon', models.CharField(max_length=50)),
                ('faIconType', models.CharField(default='fab', max_length=50)),
                ('isVisible', models.BooleanField(default=True)),
            ],
            bases=('modularweb.basefield',),
        ),
        migrations.CreateModel(
            name='LandingPageField',
            fields=[
                ('basefield_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BaseField')),
                ('fieldType', models.CharField(choices=[('MF', 'Main field (h2)'), ('SF', 'Sub field (h3)')], default='MF', max_length=2)),
            ],
            bases=('modularweb.basefield',),
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modularweb.BasePage')),
                ('contentPages', models.ManyToManyField(blank=True, related_name='sub_pages', to='modularweb.ContentPage')),
                ('endBackground', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modularweb.Photography')),
                ('fields', models.ManyToManyField(blank=True, to='modularweb.BaseField')),
            ],
            bases=('modularweb.basepage',),
        ),
        migrations.AddField(
            model_name='pagelink',
            name='basePage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modularweb.BasePage'),
        ),
        migrations.AddField(
            model_name='galleryphotographies',
            name='photography',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modularweb.Photography'),
        ),
        migrations.AddField(
            model_name='basepage',
            name='background',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modularweb.Photography'),
        ),
        migrations.AddField(
            model_name='pagelink',
            name='iconField',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modularweb.IconField'),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='linkedPages',
            field=models.ManyToManyField(blank=True, related_name='linked_pages', to='modularweb.PageLink'),
        ),
    ]