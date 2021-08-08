import psycopg2
from flask import Flask, render_template, jsonify

def get_stat(connection, show_by):
    cmd = '''DO $$
    DECLARE
      _query text;
      _name text;
    BEGIN
      _name := 'prepared_query';
      _query := '
        SELECT  DATE(''1970-01-01''::date + (time_started * interval ''1 second'')) as start_date
            '||(SELECT ', '||string_agg(DISTINCT 
                        ' sum(case when {column} ='||quote_literal({column})||' then 1 else 0 end) AS '||quote_ident({column}),',') 
                FROM jobs)||'
        FROM jobs
        GROUP BY start_date
        ';

        BEGIN
            EXECUTE 'DEALLOCATE '||_name;
        EXCEPTION
            WHEN invalid_sql_statement_name THEN
        END;

        EXECUTE 'PREPARE '||_name||' AS '||_query;
    END
    $$;

    EXECUTE prepared_query;'''.format(column=show_by)
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        # coldata = cursor.fetchall()
        # colnames = [desc[0] for desc in cursor.description]
        return [desc[0] for desc in cursor.description], cursor.fetchall()



def chartify_data(colnames, coldata):
    def gen_color():
        from random import randint
        d = (0, 255) # diapazon
        return (randint(*d), randint(*d), randint(*d), 1)



    # reorganize columns
    organized_data = {}
    for colindex in range (len (colnames)):  # first one is data
        organized_data[colnames[colindex]] = [i[colindex] for i in coldata]
    # generate datasets
    datasets = []
    for key in organized_data:
        if key=='start_date':
            continue
        print(gen_color())
        datasets.append({
                        "label": key ,
                        "data": organized_data[key],
                        "borderColor": "rgba{}".format(gen_color()),
                        "backgroundColor": "rgba(255, 255, 255, 0.0)"
                    })

    data = {
        "labels": organized_data['start_date'] ,
        "datasets": datasets,
        "borderColor": "rgba(255, 99, 132, 1)",
        "backgroundColor": "rgba(255, 255, 255, 0.0)"
    }
    return data



app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
def index():
    metadata = {'server ip':'127.0.0.1'}
    return render_template('index.html', meta = metadata)


@app.route('/data/<variable>')
def config(variable):
    if variable=='service':
        colnames , data = get_stat(conn, 'service')
        return jsonify(chartify_data (colnames , data))

    elif variable == 'username':
        colnames , data = get_stat (conn , 'username')
        return jsonify (chartify_data (colnames , data))

    else:
        pass

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/stat')
def stat():
    return  render_template('stat.html')

if __name__=='__main__':
    conn = psycopg2.connect (dbname='afanasy' , user='afadmin' ,
                             password='AfPassword' , host='10.2.67.101')
    app.run()