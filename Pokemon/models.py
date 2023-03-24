# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Blindbox(models.Model):
    boxid = models.AutoField(db_column='boxID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=50)
    b_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    box_pic = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'BlindBox'


class Boxorder(models.Model):
    b_orderid = models.AutoField(db_column='b_orderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, models.DO_NOTHING, db_column='boxID')  # Field name made lowercase.
    pay_datetime = models.CharField(max_length=50)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'BoxOrder'


class Card(models.Model):
    cardno = models.AutoField(db_column='cardNO', primary_key=True)  # Field name made lowercase.
    rarity = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    img = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'Card'


class Contain(models.Model):
    cardno = models.OneToOneField(Card, models.DO_NOTHING, db_column='cardNO', primary_key=True)  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, models.DO_NOTHING, db_column='boxID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Contain'
        unique_together = (('cardno', 'boxid'),)


class Ownedcard(models.Model):
    cardid = models.AutoField(db_column='cardID', primary_key=True)  # Field name made lowercase.
    cardno = models.ForeignKey(Card, models.DO_NOTHING, db_column='cardNO')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    status = models.CharField(max_length=50)
    c_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'OwnedCard'


class Probability(models.Model):
    ruleno = models.AutoField(db_column='ruleNO', primary_key=True)  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, models.DO_NOTHING, db_column='boxID')  # Field name made lowercase.
    rarity = models.CharField(max_length=50)
    prob = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        managed = True
        db_table = 'Probability'


class Resaleorder(models.Model):
    r_orderid = models.AutoField(db_column='r_orderID', primary_key=True)  # Field name made lowercase.
    sellerid = models.ForeignKey('User', related_name='sellerid',on_delete=models.CASCADE, db_column='sellerID')  # Field name made lowercase.
    buyerid = models.ForeignKey('User', related_name='buyerid',on_delete=models.CASCADE, db_column='buyerID')  # Field name made lowercase.
    cardid = models.ForeignKey(Ownedcard, models.DO_NOTHING, db_column='cardID')  # Field name made lowercase.
    trade_amount = models.DecimalField(max_digits=10, decimal_places=2)
    trade_datetime = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'ResaleOrder'


class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=50)
    u_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'User'
