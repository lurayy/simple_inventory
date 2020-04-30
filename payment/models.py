from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import signals

class GiftCardCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class GiftCard(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    category = models.ForeignKey(GiftCardCategory, on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=50)

    count_used = models.PositiveIntegerField(default=0)
    count_limit = models.PositiveIntegerField(blank=True, null=True)

    is_limited = models.BooleanField(default=True)
    has_unique_codes = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}  {self.code}'
    
    def is_used_out(self):
        if count_limit == count_used:
            return True
        else:
            return False


class UniqueCard(models.Model):
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} {self.gift_card.name}'


@receiver(pre_save, sender=GiftCard)
def pre_save_handler_gift_card(sender, instance, *args, **kwargs):
    if not instance.id:
       pass
    else:
        old_card = GiftCard.objects.get(id=instance.id)
        if old_card.has_unique_codes != instance.has_unique_codes:
            if old_card.count_used > 0:
                raise Exception('Cannot Edit Gift card if it is already has been used.')
            if instance.has_unique_codes:
                create_unique_cards(instance, instance.count_limit)
        else:
            if instance.has_unique_codes:
                if old_card.count_limit != instance.count_limit:
                    if old_card.count_limit < instance.count_limit:
                        create_unique_cards(instance, (instance.count_limit - old_card.count_limit))
                    if old_card.count_limit > instance.count_limit:
                        delete_unique_cards(instance,(old_card.count_limit - instance.count_limit))

@receiver(post_save, sender=GiftCard)
def post_save_handler_gift_card(sender, instance, created, **kwargs):
    if created:
        if instance.has_unique_codes:
            create_unique_cards(instance, instance.count_limit)

@receiver(pre_save, sender=UniqueCard)
def pre_save_handler_unique_card(sender, instance, *args, **kwargs):
    if not instance.id:
        if instance.is_used:
            instance.gift_card.count_used = instance.gift_card.count_used + 1
            instance.gift_card.save()
    else:
        old_card = UniqueCard.objects.get(id=instance.id)
        if old_card.is_used != instance.is_used:
            if instance.is_used:
                instance.gift_card.count_used = instance.gift_card.count_used + 1
            else:
                instance.gift_card.count_used = instance.gift_card.count_used - 1
            instance.gift_card.save()

def create_unique_cards(gift_card, count):
    if gift_card.is_limited:
        for _ in range(count):
            code = str(gift_card.code)[0:2] + str(uuid.uuid4().hex.upper()[0:8])
            card = UniqueCard.objects.create(
                gift_card = gift_card,
                code = code
            )
            card.save()
    else:
        raise Exception("Limit must be set to generate unique gift codes for the gift card.")

def delete_unique_cards(gift_card,count):
    cards = UniqueCard.objects.filter(gift_card = gift_card, is_used = False)
    if len(cards) < count:
        raise Exception('Number of gift cards used is greater than the limit you are trying to assign.')
    for i in range(count):
        card = cards[i]
        card.delete()
