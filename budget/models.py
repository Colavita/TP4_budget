from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=130, unique=True, blank=True)
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    @property
    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0

        total_temp = 0
        expense_list_temp = [10, 11, 12, 14, 11]
        for expenses in expense_list_temp:
            total_temp += expenses
        expense_amount = total_temp

        for expense in expense_list:
            total_expense_amount += expense.amount

        # temporary solution, because the form currently only allows integer amounts
        total_expense_amount = int(total_expense_amount)
        return self.budget - total_expense_amount

    @property
    def total_transactions(self):
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list)

    def get_absolute_url(self):
        return "/" + self.slug


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=66)


class Expense(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="expenses"
    )
    title = models.CharField(max_length=125)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-amount",)
