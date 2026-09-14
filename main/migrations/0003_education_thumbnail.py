# ada penambahan thumbnail pada model education 

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_education"),
    ]

    operations = [
        migrations.AddField(
            model_name="education",
            name="thumbnail",
            field=models.URLField(blank=True, null=True),
        ),
    ]

