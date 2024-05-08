from ..models.reimbursement import Reimbursement
from ..models.user import User


def calculate_optimal_reimbursements(balances):
    """
    Calcule les remboursements optimaux à partir des soldes des membres.
    """
    sorted_balances = sorted(balances.items(), key=lambda x: x[1])
    reimbursements = []
    i, j = 0, len(sorted_balances) - 1

    while i < j:
        sender, sender_balance = sorted_balances[i]
        recipient, recipient_balance = sorted_balances[j]
        amount = min(-sender_balance, recipient_balance)
        reimbursements.append({"sender": sender, "recipient": recipient, "amount": amount})
        sorted_balances[i] = (sender, sender_balance + amount)
        sorted_balances[j] = (recipient, recipient_balance - amount)
        if sorted_balances[i][1] == 0: i += 1
        if sorted_balances[j][1] == 0: j -= 1

    return reimbursements

def save_reimbursements(group_id, reimbursements):
    for sender, recipient, amount in reimbursements:
        sender_user = User.objects.get(username=sender)
        recipient_user = User.objects.get(username=recipient)
        Reimbursement(sender=sender_user, recipient=recipient_user, amount=amount).save()