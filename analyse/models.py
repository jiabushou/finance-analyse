from django.db import models

# Create your models here.


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.





class OperateRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    ctime = models.DateTimeField(db_comment='创建时间')
    mtime = models.DateTimeField(db_comment='修改时间')
    bargain_time = models.DateTimeField(db_comment='成交时间')
    bond_code = models.CharField(max_length=10, db_comment='证劵代码')
    bond_name = models.CharField(max_length=10, db_comment='证劵名称')
    operate_kind = models.CharField(max_length=10, db_comment='操作类型(in:买入;out:卖出)')
    bargain_number = models.IntegerField(db_comment='成交数量(100的整数倍)')
    bargain_unit_price = models.DecimalField(max_digits=10, decimal_places=3, db_comment='成交均价')
    bargain_amount = models.DecimalField(max_digits=10, decimal_places=3, db_comment='成交金额')
    contract_no = models.CharField(max_length=20, db_comment='合同编号')
    bargain_no = models.CharField(unique=True, max_length=20, db_comment='成交编号')
    fee = models.DecimalField(max_digits=10, decimal_places=3, db_comment='手续费')
    stamp_duty = models.DecimalField(max_digits=10, decimal_places=3, db_comment='印花税')
    other_fee = models.DecimalField(max_digits=10, decimal_places=3, db_comment='其它杂费')
    happen_amount = models.DecimalField(max_digits=10, decimal_places=3, db_comment='发生金额')
    left_amount = models.DecimalField(max_digits=10, decimal_places=3, db_comment='资金余额')
    trade_market = models.CharField(max_length=10, db_comment='交易市场')
    share_holder_account = models.CharField(max_length=10, db_comment='股东账户')
    delivery_date = models.DateTimeField(db_comment='交收日期')
    bond_full_name = models.CharField(max_length=10, db_comment='证劵中文全称')

    class Meta:
        managed = True
        db_table = 'operate_record'


class PurchaseInRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    ctime = models.DateTimeField(db_comment='创建时间')
    mtime = models.DateTimeField(db_comment='修改时间')
    purchase_in_time = models.DateTimeField(blank=True, null=True, db_comment='买入时间')
    purchase_in_count = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入份额')
    purchase_in_single_price = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入单价')
    purchase_fee = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入手续费')
    purchase_in_uniq_no = models.CharField(max_length=255, blank=True, null=True, db_comment='买入唯一编号')
    left_match = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='待匹配份额')
    bond_code = models.CharField(max_length=255, db_comment='基金编码')
    bond_name = models.CharField(max_length=255, db_comment='基金名称')

    class Meta:
        managed = True
        db_table = 'purchase_in_record'


class PurchaseOutRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    ctime = models.DateTimeField(db_comment='创建时间')
    mtime = models.DateTimeField(db_comment='修改时间')
    purchase_out_time = models.DateTimeField(blank=True, null=True, db_comment='买入时间')
    purchase_out_count = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入份额')
    purchase_out_single_price = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入单价')
    purchase_fee = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='买入手续费')
    purchase_out_uniq_no = models.CharField(max_length=255, blank=True, null=True, db_comment='买入唯一编号')
    left_match = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='待匹配份额')
    bond_code = models.CharField(max_length=255, db_comment='基金编码')
    bond_name = models.CharField(max_length=255, db_comment='基金名称')

    class Meta:
        managed = True
        db_table = 'purchase_out_record'


class MatchRelations(models.Model):
    id = models.BigAutoField(primary_key=True)
    ctime = models.DateTimeField(auto_now_add=True, db_comment='创建时间')
    mtime = models.DateTimeField(auto_now=True, db_comment='卖出记录ID')
    in_uniq_id = models.BigIntegerField(db_comment='买入记录ID')
    out_uniq_id = models.BigIntegerField(db_comment='卖出记录ID')
    match_count = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, db_comment='匹配份额')
    bond_code = models.CharField(max_length=255, db_comment='基金编码')

    class Meta:
        managed = True
        db_table = 'match_relations'