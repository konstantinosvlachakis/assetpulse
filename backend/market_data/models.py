from django.db import models

# Create your models here.
class Price(models.Model):
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.CASCADE,
        related_name="prices",
    )
    date = models.DateField()

    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "date"],
                name="unique_asset_price_date",
            )
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.asset.symbol} - {self.date}"