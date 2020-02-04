import os
from app import gateway
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.image import Image
from models.payment import Payment
from models.user import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



payments_blueprint = Blueprint('payments',
                            __name__,
                            template_folder='templates')

@payments_blueprint.route('/', methods=['GET'])
def index():
    return "payments index"

@payments_blueprint.route('/new/<image_id>', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_by_id(image_id)
    token = gateway.client_token.generate()
    return render_template('payments/new.html', aws_domain=os.getenv('AWS_DOMAIN'), image=image, token=token)


@payments_blueprint.route('/create/<image_id>', methods=['POST'])
@login_required
def create(image_id):  
    nonce = request.form.get('nonce')
    moneyleft = request.form.get('money-left')
    moneyright = request.form.get('money-right')

    image = Image.get_by_id(image_id)
    recipient = User.get_by_id(image.user_id)

    try:
        if int(moneyleft) > -1 and int(moneyright) >-1 and int(moneyright) < 100:
            amount = f'{moneyleft}.{moneyright}'
            result = gateway.transaction.sale({
                "amount": amount,
                "payment_method_nonce": nonce,
                "options": {
                "submit_for_settlement": True
                }
            })

            if result.is_success:

                payment = Payment(user_id=current_user.id, image_id=image_id, amount=amount)
                payment.save()


                message = Mail(
                    from_email= 'nextagram@email.com',
                    to_emails=recipient.email,
                    subject='Donation Received',
                    html_content=f'Donation received for {image.id}')
                
                sg = SendGridAPIClient('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')
                sg.send(message)

                flash('Donation Success')
                return redirect(url_for('users.show', username = recipient.name ))
    except:
        flash('Payment failed. Try again', "Danger")
        return redirect(url_for('payments.new', image_id=image_id))
    return f'{nonce}'  

       
