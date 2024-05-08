from flask import Blueprint, Response, stream_with_context
from ..models.expense import Expense

export_blueprint = Blueprint('export_blueprint', __name__)

@export_blueprint.route('/group/<group_id>/export/csv', methods=['GET'])
def export_group_data_csv(group_id):
    def generate():
        data = Expense.objects(group=group_id)  
        yield ','.join(['Title', 'Amount', 'Date', 'Payer', 'Category']) + '\n'
        for expense in data:
            yield ','.join([expense.title, str(expense.amount), expense.date.strftime('%Y-%m-%d'), expense.payer.username, expense.category]) + '\n'


    return Response(stream_with_context(generate()), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=group_expenses.csv"})
