from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)

# Rota para exibir o formulário
@app.route('/')
def index():
    return render_template('form.html')

# Rota para lidar com o envio do formulário
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = request.form['Colaborador']
        agente = request.form['Agente']
        cnpj_razao = request.form['area']
        status = request.form['Setor']
        ligar_novamente = request.form['ligar_novamente']

        # Salvar os dados no arquivo CSV
        csv_filename = os.path.join(os.getcwd(), 'Atendimento.csv')
        new_entry = pd.DataFrame({
            'Data': [data],
            'Agente': [agente],
            'CNPJ ou Razão': [cnpj_razao],
            'Status': [status],
            'Ligar Novamente': [ligar_novamente]
        })

        # Verificar se o arquivo CSV já existe
        if os.path.exists(csv_filename):
            new_entry.to_csv(csv_filename, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(csv_filename, index=False)

        return redirect(url_for('index'))

# Rota para unir os arquivos CSVs
@app.route('/merge_csv', methods=['GET'])
def merge_csv():
    # Listar todos os arquivos CSV no diretório
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    # Ler todos os arquivos CSV e concatená-los em um DataFrame único
    combined_df = pd.concat((pd.read_csv(file) for file in csv_files), ignore_index=True)

    # Salvar o DataFrame combinado como um novo arquivo CSV
    combined_df.to_csv('combined.csv', index=False)

    # Enviar o arquivo combinado como resposta
    return send_file('combined.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=3000)