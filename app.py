from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database import engine, Goods

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    'user': 'letmein'
}


@app.route('/')
def hello():
    return "HELLO\n"


@auth.get_password
def get_pw(id):
    if id in users:
        return users.get(id)
    return None


@app.route('/basic/')
@auth.login_required
def secret():
    return "Authorized!\n"


@app.route('/eval')
def calc_request():
    try:
        ans = request.query_string
        return str(eval(ans.decode())) + '\n'
    except Exception:
        return 'ERROR\n'


@app.route('/database')
def crud():
    try:
        function = request.args.get('function', '')
        name = request.args.get('name', '')
        amount = request.args.get('amount', 1)
        price = request.args.get('price', 0)

        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        if function == 'add' and name:
            assert int(amount) == float(amount)
            try:
                st = session.query(Goods).filter_by(name=name).one()
                st.amount += int(amount)
            except NoResultFound:
                st = Goods(name=name, amount=amount)
            session.add(st)
            session.commit()
            return 'INSERTED\n'
        elif function == 'select':
            if name:
                st = session.query(Goods).filter_by(name=name).one()
                return str(st)
            else:
                sts = session.query(Goods).filter(
                    Goods.name != 'sales').order_by(Goods.name.asc()).all()
                return ''.join(str(st) for st in sts)
        elif function == 'sell' and name:
            sales = session.query(Goods).filter_by(name='sales').one()
            assert int(amount) == float(amount)
            sales.amount += int(price) * int(amount)
            session.add(sales)
            st = session.query(Goods).filter_by(name=name).one()
            assert st.amount >= int(amount)
            st.amount -= int(amount)
            session.add(st)
            session.commit()
            return 'UPDATED\n'
        elif function == 'sales':
            sales = session.query(Goods).filter_by(name='sales').one()
            return str(sales)
        elif function == 'deleteall':
            session.query(Goods).delete()
            sales = Goods(name="sales", amount='0')
            session.add(sales)
            session.commit()
            return 'DELETED'
        else:
            return 'ERROR\n'
        session.close()
    except Exception as e:
        print(e)
        return 'ERROR\n'


if __name__ == "__main__":
    app.run(debug=True)
