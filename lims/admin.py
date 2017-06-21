from django.contrib import admin
from .models import SampleInfo, QcTask, ExtTask, LibTask
from pm.models import Project
from django import forms
from django.contrib import messages
from datetime import date, timedelta, datetime
from django.utils.html import format_html
from notification.signals import notify
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

def add_business_days(from_date, number_of_days):
    to_date = from_date
    if number_of_days >= 0:
        while number_of_days:
            to_date += timedelta(1)
            if to_date.weekday() < 5:
                number_of_days -= 1
    else:
        while number_of_days:
            to_date -= timedelta(1)
            if to_date.weekday() < 5:
                number_of_days += 1
    return to_date


class SampleInfoResource(resources.ModelResource):
    def get_export_headers(self):
        return ["id","��Ŀ","��Ʒ����","����","��Ʒ����","���uL","Ũ��ng/uL","��������","��Ʒ�˶�","��ע"]
    def get_diff_headers(self):
        return ["id","��Ŀ","��Ʒ����","����","��Ʒ����","���uL","Ũ��ng/uL","��������","��Ʒ�˶�","��ע"]
    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = self._meta.model()
        for attr, value in row.items():
            setattr(instance, attr, value)
        instance.project = Project.objects.get(id=row['��Ŀ'])
        instance.type = row['��Ʒ����']
        instance.species = row['����']
        instance.name = row['��Ʒ����']
        instance.volume = row['���uL']
        instance.concentration = row['Ũ��ng/uL']
        instance.receive_date = datetime.strptime(row['��������'],'%Y-%m-%d')
        instance.check = row['��Ʒ�˶�']
        instance.note = row['��ע']
        return instance
    class Meta:
        model = SampleInfo
        skip_unchanged = True
        fields = ('id','project__contract__name','type','species','name','volume','concentration',
                  'receive_date','check','note')
        export_order = ('id','project__contract__name','type','species','name','volume','concentration',
                  'receive_date','check','note')

class SampleInfoForm(forms.ModelForm):
    def clean_note(self):
        if self.cleaned_data['check'] is False and not self.cleaned_data['note']:
            raise forms.ValidationError('δͨ���������Ʒ�豸ע')
        return self.cleaned_data['note']


class SampleInfoAdmin(ImportExportActionModelAdmin):
    resource_class = SampleInfoResource
    form = SampleInfoForm
    list_display = ['contract', 'project', 'type', 'species', 'name', 'volume', 'concentration', 'receive_date',
                    'check', 'note']
    list_display_links = ['name']
    list_filter = ['check']
    actions = ['make_pass']
    fields = (('contract', 'contract_name', 'project', 'customer'), ('name', 'receive_date'), 'type', 'species',
              'volume', 'concentration', 'check', 'note')
    raw_id_fields = ['project']

    def contract(self, obj):
        return obj.project.contract
    contract.short_description = '��ͬ'

    def contract_name(self, obj):
        return obj.project.contract.name
    contract_name.short_description = '��ͬ��'

    def customer(self, obj):
        return obj.project.customer
    customer.short_description = '�ͻ�'

    def make_pass(self, request, queryset):
        rows_updated = queryset.update(check=True)
        if rows_updated:
            self.message_user(request, '%s ����Ʒ����ͨ��' % rows_updated)
            #��Ʒ��Ϣ�˶ԣ�������Ӧ������Ա
            notify.send(request.user, recipient=queryset[0].project.contract.salesman, verb='�˶�����Ʒ��Ϣ',description="��Ŀ���ƣ�%s �˴κ˶Ե���Ʒ������%s"%(queryset[0].project.name,rows_updated))
        else:
            self.message_user(request, '%s δ�ɹ�������Ǻ���ͨ��' % rows_updated, level=messages.ERROR)
    make_pass.short_description = '�����ѡ��Ʒ����ͨ��'

    def save_model(self, request, obj, form, change):
        if obj.check is False and not obj.note:
            messages.set_level(request, messages.ERROR)
            self.message_user(request, '��ͨ������ʱ��Ҫ���б�ע', level=messages.ERROR)
        else:
            obj.save()
            #��Ʒ��Ϣ�˶ԣ�������Ӧ������Ա
            notify.send(request.user, recipient=obj.project.contract.salesman, verb='�˶�����Ʒ��Ϣ',description="��Ŀ���ƣ�%s ��Ʒ���ƣ�%s"%(obj.project.name,obj.project.contract.name))

    def get_queryset(self, request):
        qs = super(SampleInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('lims.add_sampleinfo'):
            return qs
        return qs.filter(project__contract__salesman=request.user)

    def get_actions(self, request):
        actions = super(SampleInfoAdmin, self).get_actions(request)
        if not request.user.has_perm('lims.delete_sampleinfo'):
            actions = None
        return actions

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('lims.delete_sampleinfo'):
            return ['contract', 'contract_name', 'project', 'customer', 'name', 'receive_date', 'type', 'species',
                    'volume', 'concentration', 'check', 'note']
        return ['contract', 'contract_name', 'customer']


class ExtTaskForm(forms.ModelForm):
    def clean_note(self):
        if self.cleaned_data['result'] is False and not self.cleaned_data['note']:
            raise forms.ValidationError('��ȡʧ�ܵ���Ʒ�豸ע')
        return self.cleaned_data['note']


class ExtTaskAdmin(admin.ModelAdmin):
    form = ExtTaskForm
    list_display = ['contract', 'project', 'sample_name', 'receive_date', 'left_days', 'date', 'operator', 'result',
                    'note']
    list_display_links = ['sample_name']
    list_filter = ['result']
    actions = ['make_pass']
    fields = (('contract', 'contract_name', 'project', 'customer'), ('sample_name', 'receive_date'), 'result', 'note')

    def contract(self, obj):
        return obj.sample.project.contract
    contract.short_description = '��ͬ'

    def contract_name(self, obj):
        return obj.sample.project.contract.name
    contract_name.short_description = '��ͬ��'

    def customer(self, obj):
        return obj.sample.project.customer
    customer.short_description = '�ͻ�'

    def project(self, obj):
        return obj.sample.project
    project.short_description = '��Ŀ'

    def sample_name(self, obj):
        return obj.sample.name
    sample_name.short_description = '��Ʒ'

    def receive_date(self, obj):
        return obj.sample.receive_date
    receive_date.short_description = '��������'

    def left_days(self, obj):
        if obj.date:
            return '���'
        due_date = add_business_days(obj.sub_date, obj.sample.project.ext_cycle)
        left = (due_date - date.today()).days
        if left >= 0:
            return '��%s��' % left
        else:
            return format_html('<span style="color:{};">{}</span>', 'red', '��%s��' % -left)
    left_days.short_description = 'ʣ������'

    def operator(self, obj):
        if obj.staff:
            name = obj.staff.last_name + obj.staff.first_name
            if name:
                return name
            return obj.staff
        return ''
    operator.short_description = 'ʵ��Ա'

    def make_pass(self, request, queryset):
        rows_updated = queryset.update(result=True, date=date.today(), staff=request.user)
        if rows_updated:
            self.message_user(request, '%s ����Ʒ��ȡ�ɹ�' % rows_updated)
            #��Ʒ��ȡ�ɣ�������Ӧ������Ա
            notify.send(request.user, recipient=queryset[0].project.contract.salesman, verb='��ȡ��Ʒ�ɹ�',description="��Ŀ���ƣ�%s �˴κ˶Ե���Ʒ������%s"%(queryset[0].project.name,rows_updated))
        else:
            self.message_user(request, '%s δ�ܲ������Ϊ��ȡ�ɹ�' % rows_updated, level=messages.ERROR)
    make_pass.short_description = '�����ѡ��Ʒ��ȡ�ɹ�'

    def save_model(self, request, obj, form, change):
        if obj.result is None:
            obj.date = None
            obj.staff = None
        else:
            obj.date = date.today()
            obj.staff = request.user
        obj.save()
        #��Ʒ��ȡ�ɹ���������Ӧ������Ա
        notify.send(request.user, recipient=obj.project.contract.salesman, verb='�˶�����Ʒ��Ϣ',description="��Ŀ���ƣ�%s ��Ʒ���ƣ�%s"%(obj.project.name,obj.project.contract.name))

    def get_queryset(self, request):
        qs = super(ExtTaskAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('lims.add_exttask'):
            return qs
        return qs.filter(sample__project__contract__salesman=request.user)

    def get_actions(self, request):
        actions = super(ExtTaskAdmin, self).get_actions(request)
        if not request.user.has_perm('lims.delete_exttask'):
            actions = None
        return actions

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('lims.delete_exttask'):
            return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date', 'result', 'note']
        return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date']


class QcTaskForm(forms.ModelForm):
    def clean_note(self):
        if self.cleaned_data['result'] in [2, 3] and not self.cleaned_data['note']:
            raise forms.ValidationError('�ʼ첻�ϸ����Ʒ�豸ע')
        return self.cleaned_data['note']


class QcTaskAdmin(admin.ModelAdmin):
    form = QcTaskForm
    list_display = ['contract', 'project', 'sample_name', 'receive_date', 'left_days', 'date', 'volume', 'concentration',
                    'total', 'operator', 'result', 'note']
    list_display_links = ['sample_name']
    list_filter = ['result']
    actions = ['make_pass']
    fields = (('contract', 'contract_name', 'project', 'customer'), ('sample_name', 'receive_date'), 'volume',
              'concentration', 'total', 'result', 'note')

    def contract(self, obj):
        return obj.sample.project.contract
    contract.short_description = '��ͬ'

    def contract_name(self, obj):
        return obj.sample.project.contract.name
    contract_name.short_description = '��ͬ��'

    def customer(self, obj):
        return obj.sample.project.customer
    customer.short_description = '�ͻ�'

    def project(self, obj):
        return obj.sample.project
    project.short_description = '��Ŀ'

    def sample_name(self, obj):
        return obj.sample.name
    sample_name.short_description = '��Ʒ'

    def receive_date(self, obj):
        return obj.sample.receive_date
    receive_date.short_description = '��������'

    def left_days(self, obj):
        if obj.date:
            return '���'
        due_date = add_business_days(obj.sub_date, obj.sample.project.qc_cycle)
        left = (due_date - date.today()).days
        if left >= 0:
            return '��%s��' % left
        else:
            return format_html('<span style="color:{};">{}</span>', 'red', '��%s��' % -left)
    left_days.short_description = 'ʣ������'

    def operator(self, obj):
        if obj.staff:
            name = obj.staff.last_name + obj.staff.first_name
            if name:
                return name
            return obj.staff
        return ''
    operator.short_description = 'ʵ��Ա'

    def make_pass(self, request, queryset):
        rows_updated = queryset.update(result=1, date=date.today(), staff=request.user)
        if rows_updated:
            self.message_user(request, '%s ����Ʒ�ʼ�ϸ�' % rows_updated)
            #��Ʒ�ʼ�ϸ�������Ӧ������Ա
            notify.send(request.user, recipient=queryset[0].project.contract.salesman, verb='��Ʒ�ʼ�ϸ�',description="��Ŀ���ƣ�%s �˴κ˶Ե���Ʒ������%s"%(queryset[0].project.name,rows_updated))
        else:
            self.message_user(request, '%s δ�ܲ������Ϊ�ʼ�ϸ�' % rows_updated, level=messages.ERROR)
    make_pass.short_description = '�����ѡ��Ʒ�ʼ�ϸ�'

    def save_model(self, request, obj, form, change):
        if obj.result == 0:
            obj.volume = None
            obj.concentration = None
            obj.total = None
            obj.note = None
            obj.date = None
            obj.staff = None
        else:
            obj.date = date.today()
            obj.staff = request.user
        obj.save()
        #��Ʒ�ʼ�ϸ�������Ӧ������Ա
        notify.send(request.user, recipient=obj.project.contract.salesman, verb='��Ʒ�ʼ�ϸ�',description="��Ŀ���ƣ�%s ��Ʒ���ƣ�%s"%(obj.project.name,obj.project.contract.name))

    def get_queryset(self, request):
        qs = super(QcTaskAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('lims.add_qctask'):
            return qs
        return qs.filter(sample__project__contract__salesman=request.user)

    def get_actions(self, request):
        actions = super(QcTaskAdmin, self).get_actions(request)
        if not request.user.has_perm('lims.delete_qctask'):
            actions = None
        return actions

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('lims.delete_qctask'):
            return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date', 'volume',
                    'concentration', 'total', 'result', 'note']
        return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date']


class LibTaskForm(forms.ModelForm):
    def clean_note(self):
        if self.cleaned_data['result'] is False and not self.cleaned_data['note']:
            raise forms.ValidationError('���ⲻ�ϸ����Ʒ�豸ע')
        return self.cleaned_data['note']


class LibTaskAdmin(admin.ModelAdmin):
    form = LibTaskForm
    list_display = ['contract', 'project', 'sample_name', 'receive_date', 'left_days', 'date', 'type', 'sample_code',
                    'lib_code', 'index', 'length', 'volume', 'concentration', 'total', 'operator', 'result', 'note']
    list_display_links = ['sample_name']
    list_filter = ['result']
    actions = ['make_pass']
    fields = (('contract', 'contract_name', 'project', 'customer'), ('sample_name', 'receive_date'), 'type',
              'sample_code', 'lib_code', 'index', 'length', 'volume', 'concentration', 'total', 'result', 'note')

    def contract(self, obj):
        return obj.sample.project.contract
    contract.short_description = '��ͬ'

    def contract_name(self, obj):
        return obj.sample.project.contract.name
    contract_name.short_description = '��ͬ��'

    def customer(self, obj):
        return obj.sample.project.customer
    customer.short_description = '�ͻ�'

    def project(self, obj):
        return obj.sample.project
    project.short_description = '��Ŀ'

    def sample_name(self, obj):
        return obj.sample.name
    sample_name.short_description = '��Ʒ'

    def receive_date(self, obj):
        return obj.sample.receive_date
    receive_date.short_description = '��������'

    def left_days(self, obj):
        if obj.date:
            return '���'
        due_date = add_business_days(obj.sub_date, obj.sample.project.lib_cycle)
        left = (due_date - date.today()).days
        if left >= 0:
            return '��%s��' % left
        else:
            return format_html('<span style="color:{};">{}</span>', 'red', '��%s��' % -left)
    left_days.short_description = 'ʣ������'

    def operator(self, obj):
        if obj.staff:
            name = obj.staff.last_name + obj.staff.first_name
            if name:
                return name
            return obj.staff
        return ''
    operator.short_description = 'ʵ��Ա'

    def make_pass(self, request, queryset):
        rows_updated = queryset.update(result=True, date=date.today(), staff=request.user)
        if rows_updated:
            self.message_user(request, '%s ����Ʒ����ϸ�' % rows_updated)
            #��Ʒ����ϸ�������Ӧ������Ա
            notify.send(request.user, recipient=queryset[0].project.contract.salesman, verb='��Ʒ����ϸ�',description="��Ŀ���ƣ�%s �˴κ˶Ե���Ʒ������%s"%(queryset[0].project.name,rows_updated))
        else:
            self.message_user(request, '%s δ�ܲ������Ϊ����ϸ�' % rows_updated, level=messages.ERROR)
    make_pass.short_description = '�����ѡ��Ʒ����ϸ�'

    def save_model(self, request, obj, form, change):
        if obj.result is None:
            obj.date = None
            obj.staff = None
            obj.type = None
            obj.sample_code = None
            obj.lib_code = None
            obj.index = None
            obj.length = None
            obj.volume = None
            obj.concentration = None
            obj.total = None
            obj.note = None
        else:
            obj.date = date.today()
            obj.staff = request.user
        obj.save()
        #��Ʒ����ϸ�������Ӧ������Ա
        notify.send(request.user, recipient=obj.project.contract.salesman, verb='��Ʒ����ϸ�',description="��Ŀ���ƣ�%s ��Ʒ���ƣ�%s"%(obj.project.name,obj.project.contract.name))
    def get_queryset(self, request):
        qs = super(LibTaskAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('lims.add_libtask'):
            return qs
        return qs.filter(sample__project__contract__salesman=request.user)

    def get_actions(self, request):
        actions = super(LibTaskAdmin, self).get_actions(request)
        if not request.user.has_perm('lims.delete_libtask'):
            actions = None
        return actions

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('lims.delete_libtask'):
            return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date', 'type',
                    'sample_code', 'lib_code', 'index', 'length', 'volume', 'concentration', 'total', 'result', 'note']
        return ['contract', 'contract_name', 'project', 'customer', 'sample_name', 'receive_date']

admin.site.register(SampleInfo, SampleInfoAdmin)
admin.site.register(ExtTask, ExtTaskAdmin)
admin.site.register(QcTask, QcTaskAdmin)
admin.site.register(LibTask, LibTaskAdmin)
