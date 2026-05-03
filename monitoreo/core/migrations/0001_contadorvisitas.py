from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ContadorVisitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='sitio', max_length=50, unique=True)),
                ('total_visitas', models.PositiveIntegerField(default=0)),
                ('visitantes_unicos', models.PositiveIntegerField(default=0)),
                ('actualizado', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'contador de visitas',
                'verbose_name_plural': 'contadores de visitas',
            },
        ),
    ]
