from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField


class Group(Document):
    name = StringField(required=True, unique=True)
    members = ListField(ReferenceField('User'))
    creator = ReferenceField('User', required=True)

    def add_member(self, user):
        """rajoute un membre dans un groupe"""
        if user not in self.members:
            self.members.append(user)
            self.save()

    def calculate_balances(self):
        from .expense import Expense

        balances = {member.username: 0.0 for member in self.members}

        expenses = Expense.objects.filter(group=self)
        if not expenses:
            print("Aucune dépense trouvée pour ce groupe.")

        for expense in expenses:
            if expense.involved_members:
                amount_per_person = expense.amount / len(expense.involved_members)
                for member in expense.involved_members:
                    if member.username in balances:
                        balances[member.username] -= amount_per_person
                    else:
                        print(
                            f"Le membre {member.username} n'est pas reconnu comme faisant partie du groupe.")  # Pour débogage
            else:
                print(f"La dépense {expense.title} n'a aucun membre impliqué.")

            if expense.payer and expense.payer.username in balances:
                balances[expense.payer.username] += expense.amount
            else:
                print(
                    f"Le payeur {expense.payer.username} de la dépense {expense.title} n'est pas dans le groupe ou n'est pas défini.")

        return balances
