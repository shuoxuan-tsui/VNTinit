# Generated by Django 5.2.1 on 2025-06-02 09:41

import django.core.validators
import django.db.models.deletion
import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('employee_id', models.CharField(help_text='员工唯一标识号', max_length=20, unique=True, verbose_name='工号')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1, verbose_name='性别')),
                ('department', models.CharField(max_length=100, verbose_name='部门')),
                ('position', models.CharField(max_length=100, verbose_name='职称/职务')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='请输入有效的手机号码', regex='^1[3-9]\\d{9}$')], verbose_name='电话')),
                ('hire_date', models.DateField(verbose_name='入职日期')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('base_salary', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='基础工资')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['employee_id'], name='api_employe_employe_0a2b07_idx'), models.Index(fields=['department'], name='api_employe_departm_a88d93_idx'), models.Index(fields=['position'], name='api_employe_positio_a8b669_idx'), models.Index(fields=['name'], name='api_employe_name_463c63_idx')],
            },
        ),
        migrations.CreateModel(
            name='SalaryRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('salary_period', models.CharField(help_text='格式：YYYY-MM', max_length=7, verbose_name='薪资期间')),
                ('position_snapshot', models.CharField(help_text='记录计算薪资时的职称', max_length=100, verbose_name='职称快照')),
                ('base_salary_snapshot', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='基础工资快照')),
                ('bonus', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='奖金')),
                ('deductions', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='扣除')),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='应发工资')),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='实发工资')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_records', to='api.employee', verbose_name='员工')),
            ],
            options={
                'verbose_name': '薪资记录',
                'verbose_name_plural': '薪资记录',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['employee', 'salary_period'], name='api_salaryr_employe_46c67d_idx'), models.Index(fields=['salary_period'], name='api_salaryr_salary__23eabd_idx'), models.Index(fields=['created_at'], name='api_salaryr_created_3e5133_idx')],
                'unique_together': {('employee', 'salary_period')},
            },
        ),
    ]
