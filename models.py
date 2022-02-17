from tortoise import fields, models


class blacklist(models.Model):
  user_id = fields.BigIntField(pk=True)