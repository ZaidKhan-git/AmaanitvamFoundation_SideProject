# Generated migration for adding email fields to Donation model

from django.db import migrations, models


def clear_donations(apps, schema_editor):
    """Clear all existing donations before schema change."""
    Donation = apps.get_model('core', 'Donation')
    Donation.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_donation_options_and_more'),
    ]

    operations = [
        # First, clear all existing donations
        migrations.RunPython(clear_donations),
        
        # Remove old fields
        migrations.RemoveField(
            model_name='donation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='paid',
        ),
        
        # Add new fields
        migrations.AddField(
            model_name='donation',
            name='donor_name',
            field=models.CharField(default='', max_length=100, verbose_name='Donor Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_email',
            field=models.EmailField(default='', max_length=254, verbose_name='Donor Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Donor Phone'),
        ),
        migrations.AddField(
            model_name='donation',
            name='razorpay_order_id',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Razorpay Order ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, verbose_name='Payment ID'),
        ),
        migrations.AddField(
            model_name='donation',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=255, verbose_name='Razorpay Signature'),
        ),
        migrations.AddField(
            model_name='donation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='donation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        
        # Alter amount field to DecimalField
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount in INR', max_digits=10),
        ),
    ]
