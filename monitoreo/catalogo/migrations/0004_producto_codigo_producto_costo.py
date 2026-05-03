from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_alter_producto_precio_alter_producto_stock_actual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='costo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
