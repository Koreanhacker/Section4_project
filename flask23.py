from flask import Flask, render_template, request, redirect
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')




     
@app.route('/submit', methods=['POST'])
def submit():

    Q1 = request.form['Q1']
    Q2 = request.form['Q2']
    Q3 = request.form['Q3']
    Q4 = request.form['Q4']
    Q5 = request.form['Q5']
    Q6 = request.form['Q6']
    Q7 = request.form['Q7']
    Q8 = request.form['Q8']
    Q9 = request.form['Q9']
    Q10 = request.form['Q10']
    Q11 = request.form['Q11']
    Q12 = request.form['Q12']
    Q13 = request.form['Q13']
    Q14 = request.form['Q14']
    Q15 = request.form['Q15']
    Q16 = request.form['Q16']
    Q17 = request.form['Q17']

    return redirect(f'''/result?Q1={Q1}&Q2={Q2}&Q3={Q3}&Q4={Q4}&Q5={Q5}&Q6={Q6}&Q7={Q7}&Q8={Q8}&Q9={Q9}&Q10={Q10}&Q11={Q11}
                            &Q12={Q12}&Q13={Q13}&Q14={Q14}&Q15={Q15}&Q16={Q16}&Q17={Q17}''')

@app.route('/result')
def result():
    Q1 = request.args.get('Q1')
    Q2 = request.args.get('Q2')
    Q3 = request.args.get('Q3')
    Q4 = request.args.get('Q4')
    Q5 = request.args.get('Q5')
    Q6 = request.args.get('Q6')
    Q7 = request.args.get('Q7')
    Q8 = request.args.get('Q8')
    Q9 = request.args.get('Q9')
    Q10 = request.args.get('Q10')
    Q11 = request.args.get('Q11')
    Q12 = request.args.get('Q12')
    Q13 = request.args.get('Q13')
    Q14 = request.args.get('Q14')
    Q15 = request.args.get('Q15')
    Q16 = request.args.get('Q16')
    Q17 = request.args.get('Q17')

    est=[Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16,Q17]

    with open('model.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file)

    X_test = est
    X_test2 = pd.DataFrame(X_test).T
    y_pred = model.predict(X_test2)

    stre=str()

    if y_pred == 1:
        stre=  '당신은 심장 질환에 걸릴 확률이 높습니다.'
    else:
        stre=  '당신은 심장 질환에 걸릴 확률이 낮습니다.'


    return render_template('result.html',stre=stre)



if __name__ == '__main__':
    app.run()


# app = Flask(__name__)



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':

#         Q1 = request.form['Q1']
#         Q2 = request.form['Q2']
#         Q3 = request.form['Q3']
#         Q4 = request.form['Q4']
#         Q5 = request.form['Q5']
#         Q6 = request.form['Q6']
#         Q7 = request.form['Q7']
#         Q8 = request.form['Q8']
#         Q9 = request.form['Q9']
#         Q10 = request.form['Q10']
#         Q11 = request.form['Q11']
#         Q12 = request.form['Q12']
#         Q13 = request.form['Q13']
#         Q14 = request.form['Q14']
#         Q15 = request.form['Q15']
#         Q16 = request.form['Q16']
#         Q17 = request.form['Q17']
        

#         input_values = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17]

#         result = process_input(input_values)


#         return render_template('result.html',result=result )
    
#     return render_template('Index.html')



# def process_input(input_values):

#     model = None
    
#     with open('model.pkl','rb') as pickle_file:
#         model = pickle.load(pickle_file)

#     if request.method == 'GET':

#         X_test = request.form(input_values)
#         X_test2 = pd.DataFrame(X_test)
#         y_pred = model.predict(X_test2)

#         a=str()

#         if y_pred == 1:
#             a='높'
#         else :
#             a='낮'
    
#     result = print(f'당신은 심장 질환에 걸릴 확률이 {a}습니다.')

#     return result



# if __name__ == '__main__':
#     app.run()

